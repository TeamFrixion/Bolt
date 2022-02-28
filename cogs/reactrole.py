import asyncio
import sqlite3

import discord
from discord.ext import commands

c = discord.Color.from_rgb(250, 171, 5)

# ! SQLITE3 FUNCTIONS:
conn = sqlite3.connect("data/rr.db")
cursor = conn.cursor()


async def set_rr(msg_id, emoji, role_id):
    conn.execute("INSERT INTO rr VALUES (?, ?, ?)", (msg_id, emoji, role_id))
    conn.commit()


def get_all_rr():
    """Get all rr data"""
    cursor.execute("SELECT * FROM rr")
    return cursor.fetchall()


def get_rr(msg_id, emoji):
    """Get a specific rr's data"""
    cursor.execute(
        "SELECT * FROM rr WHERE msg_id = ? AND emoji = ?", (msg_id, emoji))
    return cursor.fetchall()


def check_rr(msg_id):
    """Check if a rr is registered in the database"""
    cursor.execute("SELECT 1 FROM rr WHERE msg_id = ? LIMIT 1", (msg_id,))
    data = cursor.fetchone()
    return data is not None


class RR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} is ready!')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        msgid = payload.message_id
        if payload.member.bot:
            return

        rr_check = check_rr(msgid)

        if rr_check == False:
            return

        data = get_rr(int(msgid), str(payload.emoji))
        data = data[0]

        global role
        guild = self.bot.get_guild(payload.guild_id)
        channel = self.bot.get_channel(payload.channel_id)

        try:
            role = discord.utils.get(guild.roles, id=data[2])
        except:
            em = discord.Embed(
                description="I am unable to fetch the role.", color=c)
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            return await msg.reply(embed=em)

        try:
            await payload.member.add_roles(role, reason="Reaction Roles")
            role = discord.utils.get(guild.roles, id=data[2])
            await payload.member.send(f"I have added the role `{role.name}` to you in {guild.name}")
        except:
            em = discord.Embed(description=f"""I am not high enough in role hierarchy to add {role.mention} to someone.
                \nDrag my role above \"{role.name}\" role to make this work.""", color=c)
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            return await msg.reply(embed=em)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        msgid = payload.message_id

        rr_check = check_rr(msgid)

        if rr_check == False:
            print("NOPE")
            return

        data = get_rr(msgid, str(payload.emoji))
        data = data[0]

        global role
        guild = self.bot.get_guild(payload.guild_id)
        channel = self.bot.get_channel(payload.channel_id)
        member = guild.get_member(payload.user_id)

        try:
            role = discord.utils.get(guild.roles, id=data[2])
        except:
            em = discord.Embed(
                description="I am unable to fetch the role.", color=c)
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            return await msg.reply(embed=em)

        try:
            await member.remove_roles(role, reason="Reaction Roles")
            role = discord.utils.get(guild.roles, id=data[2])
            await member.send(f"I have removed the role `{role.name}` from you in {guild.name}")
        except:
            em = discord.Embed(description=f"""I am not high enough in role hierarchy to remove {role.mention} from someone.
            \nDrag my role above \"{role.name}\" role to make this work.""", color=c)
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            return await msg.reply(embed=em)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if not isinstance(channel, discord.TextChannel):
            return

        cursor.execute("SELECT * FROM rr WHERE msg_id = ?", (channel.id,))
        data = cursor.fetchall()

        if not data:
            return

        cursor.execute("DELETE FROM rr WHERE msg_id = ?", (channel.id,))
        conn.commit()

    @commands.Cog.listener()
    async def on_message_delete(self, message:discord.Message):
        cursor.execute("SELECT * FROM rr WHERE msg_id = ?", (message.id,))
        data = cursor.fetchall()

        if not data:
            return

        cursor.execute("DELETE FROM rr WHERE msg_id = ?", (message.id,))
        conn.commit()

    @commands.command(aliases=['rrt'])
    @commands.is_owner()
    async def rr_table(self, ctx):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS rr (msg_id INT, emoji TEXT, role_id INT)"""
        )

        await ctx.reply("Created table `rr`.")

    @commands.command(aliases=['rr'])
    @commands.has_permissions(manage_roles=True)
    async def reactionrole(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel
            await ctx.send("Reaction Role will be sent in this channel, as you didn't mention a channel.", delete_after=5)

        if not channel.id in [c.id for c in ctx.guild.channels]:
            return await ctx.send("This channel does not exist in this server.", delete_after=5)

        questions = ['Enter Title For Embed: ', 'Enter Description For Embed: ',
                     'Enter Emoji(s): ', 'Enter Role(s) ID(s): ', 'Confirmation: Type `yes` (case sensitive) if you want to proceed,\nType anything else to cancel.']
        answers = []

        def check(user):
            return user.author == ctx.author and user.channel == ctx.channel

        for q in questions:
            q_em = discord.Embed(description=q, color=c)
            await ctx.send(embed=q_em)

            try:
                msg = await self.bot.wait_for('message', check=check)
            except asyncio.TimeoutError:
                await ctx.send("You took too long answer, so I am cancelling.")
                return
            else:
                answers.append(msg.content)

        try:
            if answers[4].lower() == 'yes':
                pass
            else:
                return await ctx.send("Cancelled.")
        except:
            return

        title = answers[0]
        desc = answers[1]
        emojis = answers[2].split(" ")
        roles = answers[3].split(" ")

        field_l = []

        rr_em = discord.Embed(title=title, description=desc, color=c)

        for i, r in enumerate(roles):
            try:
                field_l.append(
                f'{emojis[i]}: {discord.utils.get(ctx.guild.roles, id=int(r)).mention}\n')
            except:
                field_l.append(
                    f'{emojis[i]}: {r}\n'
                )

        i = " ".join(field_l)
        rr_em.add_field(
            name="React to the following emojis to get the respective roles.", value=i)
        rr_em.set_footer(text='Unreact to remove the role')

        send = await channel.send(embed=rr_em)
        for i, r in enumerate(roles):
            try:
                await set_rr(int(send.id), emojis[i], int(r))
                await send.add_reaction(emojis[i])
            except:
                a1 = r.replace("<@&", "")
                a2 = a1.replace(">", "")
                await set_rr(int(send.id), emojis[i], int(a2))
                await send.add_reaction(emojis[i])

    @reactionrole.error
    async def rr_error(self, ctx, error):
        raise error

    @commands.command(aliases=['rrr'])
    @commands.has_permissions(manage_roles=True)
    async def rr_remove(self, ctx, msg_id: int = None, channel: discord.TextChannel = None):
        if not msg_id:
            return await ctx.send(f"You didn't mention a message ID.\nUsage: `{ctx.prefix}(rrr/rr_remove) <msg_id>`")

        if not channel:
            channel = ctx.channel
            await ctx.send("As you have not mentioned a channel, I assume this is the channel where the reaction role is located.", delete_after=5)

        cursor.execute("SELECT * FROM rr WHERE msg_id = ?", (msg_id,))
        data = cursor.fetchall()

        if not data:
            return await ctx.send("There is no reaction role with this ID.")

        try:
            msg = await channel.fetch_message(msg_id)
            await msg.delete()
        except discord.Forbidden:
            await ctx.send("I do not have the required permissions to delete this message, but I have deleted the reaction role from the database.")
        except discord.HTTPException:
            await ctx.send("Something went wrong while trying to delete the message OR fetching the message (channel mentioned was not right), but I have removed the reaction role from the database.")

        cursor.execute("DELETE FROM rr WHERE msg_id = ?", (msg_id,))
        conn.commit()

        await ctx.send("Reaction Role removed.")

    @rr_remove.error
    async def rr_remove_error(self, ctx, error):
        raise error

def setup(bot):
    bot.add_cog(RR(bot))
