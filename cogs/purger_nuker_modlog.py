import discord
import datetime
from discord.ext import commands
import json

c = discord.Color.from_rgb(250,171,5)

def getchannel(guild):
	with open('data/logs.json','r') as f:
		file = json.load(f)
	return file[str(guild.id)]

class Purge_Nuke(commands.Cog):
  def __init__(self,client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print(f'{self.__class__.__name__} is ready!')
    
  @commands.command(aliases=['n'])
  @commands.has_permissions(manage_channels=True)
  async def nuke(self,ctx):
      pos = ctx.channel.position
      embed = discord.Embed(
        title='Nuked Channel :boom:',
        description=f"Nuked by: `{ctx.author.name}#{ctx.author.discriminator}`",
        color=c,
        timestamp=datetime.datetime.now(),
      )
      now = datetime.datetime.now()
      current_time = now.strftime("%d/%m/%y at %I:%M %p")
      embed.set_footer(text=f"{ctx.guild.name}  •  {current_time}")
      embed.set_image(url="https://media.discordapp.net/attachments/832980836659494944/833749914336493638/boom.gif")
      await ctx.channel.delete(reason=f"Old channel nuked by {ctx.author}")
      channel = await ctx.channel.clone(reason=f"Old channel nuked by {ctx.author}")
      await channel.edit(position=pos)
      await channel.send(embed=embed)

      channel = getchannel(ctx.guild)

      main_channel = self.client.get_channel(channel)

      logem = discord.Embed(title="Channel Nuked", description=f"```\nModerator : {ctx.author.name}#{ctx.author.discriminator}\nNuked : {ctx.channel.name}```", color = c)

      await main_channel.send(embed=logem)

  @commands.command(aliases = ['clear', 'p'])
  @commands.has_permissions(manage_messages = True,administrator = True)
  async def purge(self,ctx,amount:int=5):
    await ctx.channel.purge(limit = amount)
    embed = discord.Embed(title = 'Purged :broom:',description = f'```\nPurged By: {ctx.author.name}\nPurged: {amount} messages.```',colour = c,timestamp=datetime.datetime.utcnow())
    await ctx.send(embed = embed,delete_after = 10)
    
    try:
      channel = getchannel(ctx.guild)

      main_channel = self.client.get_channel(channel)

      logem = discord.Embed(title="Messages Purged", description=f"```\nAuthor : {ctx.author.name}#{ctx.author.discriminator}\nDeleted in : {ctx.channel.name}```", color = c)

      await main_channel.send(embed=logem)
    except:
      return
    
  @commands.command()
  async def modlog(self,ctx,channel:discord.TextChannel):
    with open('data/logs.json','r') as f:
      channe = json.load(f)
    channe[str(ctx.guild.id)] = channel.id
    with open('data/logs.json','w') as f:
      json.dump(channe,f)
    return await ctx.reply(f"Set {channel.mention} as the modlogs channel.")

def setup(client):
	client.add_cog(Purge_Nuke(client))