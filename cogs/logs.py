import discord
from discord.ext import commands
import json
import datetime
import asyncio

c = discord.Color.from_rgb(250,171,5)

def getchannel(guild):
    with open('data/logs.json', 'r') as f:
        file = json.load(f)
    if str(guild.id) in file:
        return file[str(guild.id)]

class ModLogs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} is ready!')

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        channel = getchannel(guild)
        main_channel = self.client.get_channel(channel)
        if not main_channel:
            return
        await asyncio.sleep(0.5)
        found_entry = None
        async for entry in guild.audit_logs(limit=50,
                                            action=discord.AuditLogAction.ban,
                                            after=datetime.datetime.utcnow() -
                                            datetime.timedelta(seconds=15),
                                            oldest_first=False):
            if entry.created_at < datetime.datetime.utcnow(
            ) - datetime.timedelta(seconds=10):
                continue
            if entry.target.id == user.id:
                found_entry = entry
                break
        if not found_entry:
            return

        logem = discord.Embed(
            title="Member Banned",
            description=
            f"```Member Banned : {user.name}#{user.discriminator}\nBanned by : {found_entry.user}\nTime : {found_entry.created_at}\nReason : {found_entry.reason}```",
            color=c)

        await main_channel.send(embed=logem)

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        channel = getchannel(guild)
        main_channel = self.client.get_channel(channel)
        if not main_channel:
            return
        found_entry = None
        await asyncio.sleep(0.5)
        async for entry in guild.audit_logs(
                limit=50,
                action=discord.AuditLogAction.unban,
                after=datetime.datetime.utcnow() -
                datetime.timedelta(seconds=15),
                oldest_first=False):
            if entry.created_at < datetime.datetime.utcnow(
            ) - datetime.timedelta(seconds=10):
                continue
            if entry.target.id == user.id:
                found_entry = entry
                break
        if not found_entry:
            return

        logem = discord.Embed(
            title="Member Unbanned",
            description=
            f"```Member Unbanned : {user.name}#{user.discriminator}\nTime : {datetime.datetime.now()}```",
            color=c)

        await main_channel.send(embed=logem)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = getchannel(member.guild)
        main_channel = self.client.get_channel(channel)
        found_entry = None
        await asyncio.sleep(0.5)
        try:
            async for entry in member.guild.audit_logs(
                    limit=50,
                    action=discord.AuditLogAction.kick,
                    after=datetime.datetime.utcnow() -
                    datetime.timedelta(seconds=15),
                    oldest_first=False):
                if entry.created_at < datetime.datetime.utcnow(
                ) - datetime.timedelta(seconds=10):
                    continue
                if entry.target.id == member.id:
                    found_entry = entry
                    break
            if not found_entry:
                return
        except: return

        logem = discord.Embed(
            title="Member Removed/Left",
            description=
            f"```Member : {member.name}#{member.discriminator}\nTime : {datetime.datetime.now()}\nRemoved By : {found_entry.user}\nReason : {found_entry.reason}```",
            color = c)

        if not main_channel:
            return

        await main_channel.send(embed=logem)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            if message.author.bot:
                return
            channel = getchannel(message.guild)
            main_channel = self.client.get_channel(channel)
            if not main_channel:
                return
            logem = discord.Embed(
                title="Message Deleted",
                description=
                f"```Message Deleted : {message.content}\nAuthor : {message.author.name}#{message.author.discriminator}\nDeleted in : {message.channel.name}```",
                color=c)

            await main_channel.send(embed=logem)
        except:
            return

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            if len(before.roles) < len(after.roles):
                new_role = next(role for role in after.roles
                                if role not in before.roles)
                channel = getchannel(before.guild)
                main_channel = self.client.get_channel(channel)
                if not main_channel:
                    return
                logem = discord.Embed(
                    title="Role Added",
                    description=
                    f"```Role Added : {new_role.name} (id:{new_role.id})\nAdded To : {before.name}#{before.discriminator}```",
                    color=c)

                await main_channel.send(embed=logem)
            if len(before.roles) > len(after.roles):
                new_role = next(role for role in before.roles
                                if role not in after.roles)
                channel = getchannel(before.guild)
                main_channel = self.client.get_channel(channel)
                if not main_channel:
                    return
                logem = discord.Embed(
                    title="Role Removed",
                    description=
                    f"```Role Removed : {new_role.name} (id:{new_role.id})\nRemoved From : {before.name}#{before.discriminator}```",
                    color=c)

                await main_channel.send(embed=logem)
            else:
                return
        except AttributeError:
            return
    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        channel_ = getchannel(channel.guild)
        main_channel = self.client.get_channel(channel_)
        if not main_channel:
            return
        logem = discord.Embed(
            title="Channel Created",
            description=
            f"```Channel Name: {channel.name} (id:{channel.id})\nCategory: {channel.category}```",
            color=c)

        await main_channel.send(embed=logem)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        channel_ = getchannel(channel.guild)
        main_channel = self.client.get_channel(channel_)
        if not main_channel:
            return
        logem = discord.Embed(
            title="Channel Deleted",
            description=
            f"```Channel Name: {channel.name} (id:{channel.id})\nCategory: {channel.category}```",
            color=c)

        await main_channel.send(embed=logem)

def setup(client):
    client.add_cog(ModLogs(client))
