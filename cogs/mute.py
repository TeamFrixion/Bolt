import sqlite3

import discord
from discord.ext import commands
from discord.utils import get

from utils.emb import *

conn = sqlite3.connect('data/mute.db')
cursor = conn.cursor()

c = discord.Color.from_rgb(250, 171, 5)

def check_role(guild):
    """Check if muterole is registered in the database"""
    cursor.execute("SELECT * FROM mute WHERE guild_id = ?", (guild.id,))
    return bool(cursor.fetchone())

def fetch_muterole(guild):
    """Fetch the muterole of a guild, return None if not found"""
    cursor.execute("SELECT * FROM mute WHERE guild_id = ?", (guild.id,))
    if role_id := cursor.fetchone():
        return get(guild.roles, id=role_id[1])
    return None

def remove_muterole(guild):
    cursor.execute("DELETE FROM mute WHERE guild_id = ?", (guild.id,))
    conn.commit()

def create_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS mute (guild_id INT, role_id INT)")
    conn.commit()

def convert_time(time_to_convert):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600 * 24}

    unit = time_to_convert[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time_to_convert[:-1])
    except:
        return -2

    return val * time_dict[unit]

class MuteUnmute(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.tick = '<:tick:879670104000954400>'
        self.cross = '<:Cross:879670127707193364>'

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} is ready!')


    @commands.group(aliases=['mr'])
    @commands.has_permissions(manage_roles=True)
    async def muterole(self, ctx):
        if ctx.invoked_subcommand is None:
            emb = discord.Embed(
                title="Mute Role Commands",
                description=f"Current muterole of the server is None.\nTo set a muterole, use `{ctx.prefix}(mr/muterole) (set/s)`",
                color = c
            )

            check = check_role(ctx.guild)
            if check:
                emb.description = f"Current muterole of the server is {fetch_muterole(ctx.guild).mention}.\nTo set a muterole, use `{ctx.prefix}(mr/muterole) (set/s)`"

            emb.add_field(
                name="(set/s) [role_mention/role_id]",
                value="Sets the muterole of the server | `15s` cooldown.",
                inline=False
            )

            emb.add_field(
                name="(remove/r)",
                value="Remove the muterole of the server | `30s` cooldown.",
                inline=False
            )

            await ctx.send(embed=emb)

    @muterole.command(aliases=['s'])
    @commands.has_permissions(manage_roles = True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def set(self, ctx, role : discord.Role = None):
        if not role:
            return await ctx.send(f"{self.cross} **Please provide a role to set as muterole!**\nCorrect usage: {ctx.prefix}(set/s) [role_mention/role_id]")

        if role.id == ctx.guild.default_role.id:
            return await ctx.send(f"{self.cross} **You can't set the default role as muterole!**")

        if role.position >= ctx.author.top_role.position:
            return await ctx.send(f"{self.cross} **You can't set a role that is higher than your highest role!**")

        if role.position >= ctx.guild.me.top_role.position:
            return await ctx.send(f"{self.cross} **I can't set a role that is higher than my highest role!**")

        check = check_role(ctx.guild)

        if check:
            cursor.execute("UPDATE mute SET role_id = ? WHERE guild_id = ?", (role.id, ctx.guild.id))
        else:
            cursor.execute("INSERT INTO mute VALUES (?, ?)", (ctx.guild.id, role.id))

        await success_emb_maker(
            ctx.channel,
            '**Muterole set successfully!**',
            f"Muterole set to {role.mention}",
            c,
            "Mute System by Bolt",
            f"{ctx.author.name}#{ctx.author.discriminator} & Bolt",
            "Muterole set",
        )

    @muterole.command(aliases=['r'])
    @commands.has_permissions(manage_roles = True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def remove(self, ctx):
        check = check_role(ctx.guild)

        if not check:
            return await ctx.send(f"{self.cross} **There is no muterole to remove!**")

        remove_muterole(ctx.guild)

        await success_emb_maker(
            ctx.channel,
            "**Muterole removed successfully!**",
            'Muterole removed',
            c,
            "Mute System by Bolt",
            f"{ctx.author.name}#{ctx.author.discriminator} & Bolt",
            "Muterole removed",
        )

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def mute(self, ctx, member : discord.Member = None):
        if not member:
            return await ctx.send(f"{self.cross} **Please provide a member to mute!**\nCorrect usage: {ctx.prefix}mute [member]")

        if not check_role(ctx.guild):
            return await ctx.send(f"{self.cross} **There is no muterole set!**")

        if member.id == ctx.author.id:
            return await ctx.send(f"{self.cross} **You can't mute yourself!**")

        if member.id == ctx.guild.me.id:
            return await ctx.send(f"{self.cross} **I can't mute myself!**")

        if member.id == ctx.guild.owner.id:
            return await ctx.send(f"{self.cross} **I can't mute the server owner!**")

        if member.top_role.position >= ctx.guild.me.top_role.position:
            return await ctx.send(f"{self.cross} **I can't mute a member that is higher than my highest role!**")

        if member.top_role.position >= ctx.guild.owner.top_role.position:
            return await ctx.send(f"{self.cross} **I can't mute a member that is higher than the server owner!**")

        role = fetch_muterole(ctx.guild)

        if role in member.roles:
            return await ctx.send(f"{self.cross} **This member is already muted!**")

        try:
            await member.add_roles(role, reason=f"Muted by {ctx.author.name}#{ctx.author.discriminator} using Bolt")
        except discord.Forbidden:
            return await ctx.send(f"{self.cross} **I can't mute this member!**")
        except discord.HTTPException:
            return await ctx.send(f"{self.cross} **Something went wrong! Maybe try the command again.**")

        success_emb_maker(
            ctx.channel,
            "**Member muted successfully!**",
            f"{member.mention} has been muted",
            c,
            "Mute System by Bolt",
            f"{ctx.author.name}#{ctx.author.discriminator} & Bolt",
            "Muted member"
        )

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def unmute(self, ctx, member : discord.Member = None):
        if not member:
            return await ctx.send(f"{self.cross} **Please provide a member to unmute!**\nCorrect usage: {ctx.prefix}unmute [member]")

        if not check_role(ctx.guild):
            return await ctx.send(f"{self.cross} **There is no muterole set!**")

        if member.id == ctx.author.id:
            return await ctx.send(f"{self.cross} **You can't unmute yourself!**")

        if member.id == ctx.guild.me.id:
            return await ctx.send(f"{self.cross} **I can't unmute myself!**")

        if member.id == ctx.guild.owner.id:
            return await ctx.send(f"{self.cross} **I can't unmute the server owner!**")

        if member.top_role.position >= ctx.guild.me.top_role.position:
            return await ctx.send(f"{self.cross} **I can't unmute a member that is higher than my highest role!**")

        if member.top_role.position >= ctx.guild.owner.top_role.position:
            return await ctx.send(f"{self.cross} **I can't unmute a member that is higher than the server owner!**")

        role = fetch_muterole(ctx.guild)

        if role not in member.roles:
            return await ctx.send(f"{self.cross} **This member is not muted!**")

        try:
            await member.remove_roles(role, reason=f"Unmuted by {ctx.author.name}#{ctx.author.discriminator} using Bolt")
        except discord.Forbidden:
            return await ctx.send(f"{self.cross} **I can't unmute this member!**")
        except discord.HTTPException:
            return await ctx.send(f"{self.cross} **Something went wrong! Mabye try the command again.**")

    @commands.command()
    async def create_mute_table(self, ctx):
        create_table()
        await ctx.reply("Successfully created the mute table!")

def setup(client):
    client.add_cog(MuteUnmute(client))
