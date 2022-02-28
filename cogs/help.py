import discord
from discord.ext import commands
import datetime

c = discord.Color.from_rgb(250,171,5)

class Help(commands.Cog):
	def __init__(self,client):
		self.client = client
  
	@commands.Cog.listener()
	async def on_ready(self):
		print(f'{self.__class__.__name__} is ready!')

	@commands.group(invoke_without_command = True)
	async def help(self,ctx):
		embed = discord.Embed(
		    title='Help has arrived!',
		    description='The prefix for this server is `b.`',
		    colour=c,
		)
		embed.add_field(name = '🛡️ Mod', value='```b.help mod```')
		embed.add_field(name=':gear: Utility', value='```b.help misc```', inline=False)
		embed.add_field(name=':flying_disc: Reaction Roles', value='```b.help rr```', inline=False)
		embed.add_field(name='🔧 Config', value='```b.help config```', inline=False)
		embed.add_field(name='📑 Role Management', value='```b.help roles```', inline=False)
		embed.add_field(
            name = 'Simon says..',
            value = '[Invite me](https://discord.com/api/oauth2/authorize?client_id=881081254555029515&permissions=536870911991&scope=bot)  •  [Support server](https://discord.gg/bPqN4eCfTf)  •  [Vote for me!](https://top.gg/bot/881081254555029515/vote)',
            inline = False)
		await ctx.reply(embed = embed)

	@help.command(aliases = ['moderation'])
	async def mod(self,ctx):
		embed = discord.Embed(title = 'Moderation commands',description = 'Bolt was designed to keep your server safe and secure from malicious users.',colour = c,timestamp = datetime.datetime.now())
		embed.add_field(
		    name=f'`{ctx.prefix}(purge/p) [number]`',
		    value='Purge messages in a channel.',
		    inline=False,
		)
		embed.add_field(
		    name=f'`{ctx.prefix}(ban/b) [@member] [reason]`', value='Ban a user.', inline=False)
		embed.add_field(
		    name=f'`{ctx.prefix}(unban/ub) [member_username_and_discriminator]`',
		    value='Unban a user.',
		    inline=False,
		)
		embed.add_field(
		    name=f'`{ctx.prefix}(kick/k) [@member] [reason]`',
		    value='Kick a user.',
		    inline=False)
		embed.add_field(name=f'`{ctx.prefix}nuke/n)`', value = 'Nuke a channel.', inline = False)
		embed.add_field(
		    name=f'`{ctx.prefix}nick [@member] [nickname]`',
		    value='Change someone\'s nickname.',
		    inline=False,
		)
		embed.add_field(
		    name=f'`{ctx.prefix}lock <channel>`',
		    value='Lock a channel so people can\'t send messages.',
		    inline=False,
		)
		embed.add_field(
		    name=f'`{ctx.prefix}unlock <channel>`',
		    value='Unlock a channel so people can talk.',
		    inline=False,
		)
		embed.add_field(
		    name=f'`{ctx.prefix}modlog [channel_mention/channel_id]`',
		    value='Set a Mod logs channel.',
		    inline=False,
		)
		embed.add_field(
		    name=f'`{ctx.prefix}(autoroleset/as) [role]`',
		    value='Gives the role automatically to anyone who joins the server.',
		    inline=False,
		)
		embed.add_field(
		    name=
		    f'`{ctx.prefix}(vmute/vm) [member_mention/member_id] [time_in_seconds, inf value for infinite] <reason>`',
		    value='VC Mute someone so they can\'t talk in VCs.',
		    inline=False,
		)
		embed.add_field(
		    name=f'`{ctx.prefix}(unvmute/unvm/uvm) [member_mention/member_id] <reason>`',
		    value='VC Unmute someone so they can talk in VCs if they\'re muted.',
		    inline=False,
		)
		embed.set_author(name = ctx.author,icon_url = ctx.author.avatar.url)
		embed.set_footer(
		    text="Don't literally use `[]` and `<>` and `()` in the command usage!",
		    icon_url=ctx.author.avatar.url,
		)
		await ctx.reply(embed = embed)

	@help.command(aliases = ['utility', 'Utility', 'UTILITY', 'Util', 'UTIL','misc'])
	async def util(self,ctx):
		embed = discord.Embed(title = 'Utility commands',description = 'Bolt also has a few utility commands which will help you out!',colour = c)
		embed.add_field(
		    name=f'`{ctx.prefix}iss`',
		    value='Gives the current location of the International Space Station!',
		    inline=False,
		)
		embed.add_field(
		    name=f'`{ctx.prefix}distance [latitude_1] [longitude_1] [latitude_2] [longitude_2]`',
		    value='Exact distance between two locations.',
		    inline=False,
		)
		embed.add_field(
		    name=f'`{ctx.prefix}(serverinfo/si/guildinfo)`',
		    value='Info on the guild.',
		    inline=False,
		)
		embed.add_field(
		    name=f'`{ctx.prefix}(channelinfo/ci)`', value='Info on any channel.', inline=False)
		embed.add_field(name=f'`{ctx.prefix}ping`', value = 'What is my latency?', inline = False)
		embed.add_field(
		    name=f'`{ctx.prefix}youtube`', value='Watch YouTube in a discord VC.', inline=False)
		await ctx.reply(embed = embed)

	@help.command(aliases=['reactionroles', 'rr'])
	async def reactionrole(self, ctx):
		embed = discord.Embed(title = 'Reaction Role commands',description = 'Bolt also has awesome unlimited reaction roles!',colour = c)
		embed.add_field(
		    name=f'`{ctx.prefix}(rr/reactionrole) [emoji] [role_mention/role_id] [channel_for_rr] (message_for_embed)`',
		    value='Make a new reaction-role!',
		    inline=False,
		)
		embed.add_field(
		    name=f'`{ctx.prefix}(rrr/rr_remove) <msg_id>`',
		    value='Remove a reaction role using the message ID.',
		    inline=False,
		)
		embed.set_footer(text="DON'T ADD `[]` OR `<>` OR `()` IN YOUR COMMANDS!")
		await ctx.reply(embed = embed)

	@help.command(aliases=['configure'])
	async def config(self, ctx):
		embed = discord.Embed(title = 'Config commands',description = 'Bolt also has configurable settings!',colour = c)
		embed.add_field(
		    name=f'`{ctx.prefix}(prefix) [set/default] [new_prefix(if mode is set)]`',
		    value='Set the prefix to a new one, or restore to default!',
		    inline=False,
		)

		await ctx.send(embed=embed)

	@help.command(aliases=['roles'])
	async def role(self, ctx):
		embed = discord.Embed(title = 'Role-related commands',description = 'Bolt also has role-related commands!',colour = c)
		embed.add_field(
		    name=f'`{ctx.prefix}(ar/autorole)`',
		    value='Returns the list of autorole-related commands. Use this command to know all autorole-related commands!',
		    inline=False,
		)
		embed.add_field(
		    name=f'`{ctx.prefix}(newrole/newr) [hex_code] [role_name]`',
		    value='Create a new role!',
		    inline=False,
		)
		embed.add_field(
			name=f'`{ctx.prefix}(delrole/delr) [role_name]`',
			value='Get info on a role!',
			inline=False,
		)
		embed.add_field(
			name=f'`{ctx.prefix}(giverole/giver) [role_name] [member_mention/member_id]`',
			value='Give someone a role!',
			inline=False,
		)
		embed.add_field(
			name=f'`{ctx.prefix}(removerole/remover) [role_name] [member_mention/member_id]`',
			value='Remove a role from someone!',
			inline=False,
		)
		embed.add_field(
			name=f'`{ctx.prefix}(allroles/allr)`',
			value='Get a list of all roles in the server!',
			inline=False,
		)
		embed.add_field(
			name=f'`{ctx.prefix}(memroles/memr) [member_mention/member_id]`',
			value='Get a list of all roles a member has!',
			inline=False,
		)

		await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Help(client))