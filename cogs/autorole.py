import sqlite3

import discord
from discord.ext import commands

from utils.emb import *

c = discord.Color.from_rgb(250,171,5)

# SQLITE3 FUNCTIONS:
conn = sqlite3.connect("data/ar.db")
cursor = conn.cursor()

async def set_ar(guild_id, role_id):
    conn.execute("INSERT INTO ar VALUES (?, ?)", (guild_id, role_id))
    conn.commit()

def get_all_ar():
    """Get all ar data"""
    cursor.execute("SELECT * FROM ar")
    return cursor.fetchall()

def get_ar(guild_id):
    """Get a specific ar's data"""
    cursor.execute("SELECT * FROM ar WHERE guild_id = ?", (guild_id,))
    return cursor.fetchall()

def check_ar(guild_id):
    """Check if a ar is registered in the database"""
    cursor.execute("SELECT 1 FROM ar WHERE guild_id = ? LIMIT 1", (guild_id,))
    data = cursor.fetchone()
    return data is not None

class AutoRole(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.tick = '<:tick:879670104000954400>'
        self.cross = '<:Cross:879670127707193364>'

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} is ready!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Add the role to the member"""
        if member.bot:
            return

        rr_check = check_ar(member.guild.id)

        if rr_check == False:
            return

        data = get_ar(member.guild.id)
        data = data[0]

        try:
            role = discord.utils.get(member.guild.roles, id = data[1])
        except:
            for channel in member.guild.text_channels:
                if channel.permissions_for(member.guild.me).send_messages:
                    fail_emb_maker(channel, "Auto Role Fail", "The role you have set for this server does not exist anymore.", c, "Auto Role by Bolt", "Bolt", "Role not found")
                break
            return
        try:
            await member.add_roles(role, reason = "Reaction Roles")
        except:
            for channel in member.guild.text_channels:
                if channel.permissions_for(member.guild.me).send_messages:
                    fail_emb_maker(channel, "Auto Role Fail", f"I am not high enough in role hierarchy to add {role.name} to someone.\nDrag my role above \"{role.name}\" role to make this work.", c, "Auto Role by Bolt", "Bolt", "Role Hierarchy Issue")
                break
            return

    @commands.command()
    @commands.is_owner()
    async def ar_table(self, ctx):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS ar (guild_id INT, role_id INT)"""
            )

        await ctx.reply("Created table `ar`.")

    @commands.group(aliases=['ar'])
    async def autorole(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Autorole related commands", color = c)
            embed.add_field(name='`(check/c)`', value='Check on what is the autorole for the server', inline = False)
            embed.add_field(name='`(set/s)`', value='Set the autorole for the server', inline=False)

            await ctx.reply(embed=embed)

    @autorole.command(aliases=['c'])
    async def check(self, ctx):
        rr_check = check_ar(ctx.guild.id)

        if not rr_check:
            return await ctx.reply(f"{self.cross} This server has no autorole set.\nTo set an autorole for your server, run `b.(autorole/ar) (set/s) [role_mention/role_id]`")

        data = get_ar(ctx.guild.id)
        data = data[0]
        role = discord.utils.get(ctx.guild.roles, id = data[1])

        em = discord.Embed(title=f"{self.tick} **{ctx.guild.name}**'s autorole role", description=f'The autorole for this server is {role.mention}.', color = c)

        return await ctx.reply(embed=em)

    @autorole.command(aliases=['s'])
    @commands.has_permissions(manage_roles=True)
    async def set(self, ctx, role : discord.Role = None):
        if not role:
            return await ctx.reply(f"{self.cross} You didn't mention a role.\n`b.(autorole/ar) (set/s) [role_mention/role_id]`")

        await set_ar(ctx.guild.id, role.id)

        success_emb_maker(ctx.channel, "Auto Role Set", f"The autorole for this server has been set to {role.mention}", c, "Auto Role by Bolt", "Bolt", "Auto Role Set")

def setup(client):
    client.add_cog(AutoRole(client))
