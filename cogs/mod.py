import discord
import datetime
import json

from discord.ext import commands

c = discord.Color.from_rgb(45, 214, 254)

def getchannel(guild):
	with open('data/logs.json','r') as f:
		file = json.load(f)
	return file[str(guild.id)]

def gettoxiclevel(guild):
    with open('data/toxic.json','r') as f:
        file = json.load(f)
    return file[str(guild.id)]

class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.tick = '<:tick:879670104000954400>'
        self.cross = '<:Cross:879670127707193364>'
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} is ready!')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.client.get_channel(871422223913721876)
        icon = guild.icon
        owner = guild.owner

        embed = discord.Embed(title="New server joined!", description=f"`{guild.name}` | `{guild.id}`", color = discord.Color.purple())
        try:
            embed.set_thumbnail(url=icon)
        except:
            pass
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Members:", value=f"{len(guild.members)}", inline=False)

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        channel = self.client.get_channel(871422223913721876)
        icon = guild.icon
        owner = guild.owner

        embed = discord.Embed(title="Server Left", description=f"`{guild.name}` | `{guild.id}`", color = discord.Color.purple())
        try:
            embed.set_thumbnail(url=icon)
        except:
            pass
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Members:", value=f"{len(guild.members)}", inline=False)

        await channel.send(embed=embed)

    @commands.command(aliases=["lockdown"])
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def lock(self,ctx, channel : discord.TextChannel=None):
        if channel is None:
            channel = ctx.channel
        channel = channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(description = f'Successfully locked {channel} | Only Admins will be able to type in a locked channel',colour = discord.Color.blue(),timestamp = datetime.datetime.now())
        await channel.send(embed = embed)
        report_embed = discord.Embed(title = 'Channel locked',description = 'A channel has been locked.',colour = discord.Color.blue())
        report_embed.add_field(name = 'Moderator:',value = ctx.author.mention)
        report_embed.add_field(name = 'Channel',value = channel)
        channel = getchannel(ctx.guild)
        main_chan = self.client.get_channel(channel)
        await main_chan.send(embed = report_embed)
        

    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(description=f"❌ **{ctx.message.author.name}**,  You don't have permission to use this command.", color=c)
            await ctx.send()
        elif isinstance(error, commands.BadArgument):
            em = discord.Embed(description=f'❌ **{ctx.message.author.name}**, I could not find a channel with that name.', color=c)
            return await ctx.reply(embed=em)
        else:
          raise error


		
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self,ctx, channel : discord.TextChannel=None):
        if channel is None:
            channel = ctx.channel
        channel = channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f'Channel {channel.mention} is now unlocked.')

    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            em = discord.Embed(description=f'❌ **{ctx.message.author.name}**, I could not find a channel with that name.', color=c)
            await ctx.reply(embed=em)
        elif isinstance(error, commands.MissingPermissions):
            em = discord.Embed(description=f"❌ **{ctx.message.author.name}**, You don't have permission to use this command.", color=c)
            await ctx.reply(embed=em)
        else:
          raise error
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def createdb(self,ctx):
        with open('data/swears.json','r') as f:
            file = json.load(f)
            file[str(ctx.guild.id)] = []
        with open('data/swears.json','w') as f:
            json.dump(file,f,indent = 4)

    @commands.command()
    async def addword(self,ctx,*,word):
        with open('data/swears.json','r') as f:
            file = json.load(f)
        with open('data/swears.json','w') as f:
            file[str(ctx.guild.id)] = [].append(word)
            json.dump(file,f,indent = 4)

    # KICK COMMAND
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, member: discord.Member, *, reason=None):
        try:
            embed = discord.Embed(description=f"You have been kicked from {ctx.author.guild}.\nReason : {reason}")
            await member.send(embed = embed)
        except:
            embed = discord.Embed(description = "The member has their dms closed, so I couldn't inform them that they were kicked.")
            await ctx.send(embed = embed)

        try:
            await member.kick(reason=reason)
            embed = discord.Embed(description = f'User {member} has been kicked by moderator {ctx.author.mention}.\nReason : {reason}')
            await ctx.send(embed = embed)
        except:
            embed = discord.Embed(description = "Something went wrong. I may not have higher perms than the person you want to kick.\nTo resolve this issue drag my role above all roles.")
            await ctx.send(embed = embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(description=f"❌ **{ctx.message.author.name}**, you need to mention someone to kick.", color=c)
            await ctx.reply(embed=em)
        elif isinstance(error, commands.BadArgument):
            em = discord.Embed(description=f"❌ **{ctx.message.author.name}**, I could not find a user with that name.", color=c)
            await ctx.reply(embed=em)
        elif isinstance(error, commands.MissingPermissions):
            em = discord.Embed(description=f"❌ **{ctx.message.author.name}**,  You don't have permission to kick members.", color=c)
            await ctx.reply(embed=em)
        elif isinstance(error,discord.Forbidden):
          embed = discord.Embed(title = 'An error occurred.',description = 'I dont have the required permissions to ban that specific user')
          await ctx.send(embed = embed)
        else:
          raise error

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, member: discord.Member, *, reason=None):
        try:
            embed = discord.Embed(description = f"You have been banned from {ctx.author.guild}.\nReason : {reason}")
            await member.send(embed = embed)
        except:
            embed = discord.Embed(description = "The member has their dms closed, so I couldn't inform them that they were kicked.")
            await ctx.reply(embed = embed)

        try:
            await member.ban(reason=reason)
            embed = discord.Embed(description = f'User {member} has been banned by moderator {ctx.author.mention}.\nReason : {reason}')
            await ctx.reply(embed = embed)
        except:
            embed = discord.Embed(title = 'Error',description = "Something went wrong. I may not have higher perms than the person you want to ban.\nTo resolve this issue drag my role above all roles.")
            await ctx.reply(embed = embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(description=f'❌ **{ctx.message.author.name}**, you need to mention someone to ban.', color=c)
            await ctx.reply(embed=em)
        elif isinstance(error, commands.BadArgument):
            em = discord.Embed(description=f'❌ **{ctx.message.author.name}**, I could not find a user with that name.', color=c)
            await ctx.reply(embed=em)
        elif isinstance(error, commands.MissingPermissions):
            em = discord.Embed(description=f"❌ **{ctx.message.author.name}**, You don't have permission to ban members.", color=c)
            await ctx.reply(embed=em)
        else:
          raise error

    @commands.command(aliases=['sm', 'slowmode', 'sd'])
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setdelay(self,ctx, seconds: int, channel : discord.TextChannel=None):
        if not channel:
            channel = ctx.message.channel
        await channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(description = f'The new slowmode for this channel is {seconds}s.',colour = c,timestamp = datetime.datetime.now())
        await ctx.reply(embed=embed)

    @setdelay.error
    async def sm_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(description=f'❌ **{ctx.message.author.name}**, you need to mention the slowmode time.', color=c)
            await ctx.reply(embed=em)
        elif isinstance(error, commands.MissingPermissions):
            em = discord.Embed(description=f"❌ **{ctx.message.author.name}**, You don't have permission to set slowmodes.", color=c)
            await ctx.reply(embed=em)
        else:
          raise error

    @commands.command(aliases=['ub'])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            try:
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f'Unbanned {user.mention}')
                    return
            except:
                await ctx.send("Something went wrong. Recheck all arguements and make sure I have permissions to unban.\n")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send(f'❌ **{ctx.message.author.name}**, you need to mention someone to unban.')
        elif isinstance(error, commands.BadArgument):
          await ctx.send(f'❌ **{ctx.message.author.name}**, I could not find a user with that name.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"❌ **{ctx.message.author.name}**,  You don't have permission to unban members.")
        else:
          raise error

def setup(client):
	client.add_cog(Mod(client))