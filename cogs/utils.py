import discord
import psutil
import aiohttp
import random
import randfacts
import datetime
from discord.ext import commands
import haversine as hv

utilc = c = discord.Color.from_rgb(250,171,5)

class Utils(commands.Cog):
    def __init__(self,client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} is ready!')

    @commands.command()
    async def vote(self,ctx):
      embed = discord.Embed(description = '[Vote now!](https://top.gg/bot/881081254555029515/vote)', color = utilc)
      await ctx.send(embed = embed)

    @commands.command()
    async def invite(self,ctx):
      embed = discord.Embed(description = '[Invite me](https://discord.com/api/oauth2/authorize?client_id=881081254555029515&permissions=1644972473847&scope=bot%20applications.commands)', color = utilc)
      await ctx.send(embed = embed)
    @commands.command()
    async def support(self,ctx):
      embed = discord.Embed(description = '[Support server](https://discord.gg/mfVKyxbkRn)', color = utilc)
      await ctx.send(embed = embed)

    @commands.command()
    async def avatar(self,ctx,member:discord.Member=None):
        if member is None:
            avatar = ctx.author.avatar_url
            avatar = member.avatar_url
            embed = discord.Embed(description = f'[{ctx.author}\'s]({avatar})', color = utilc)
            embed.set_image(url = avatar)
            embed = embed
        else:
            avatar = member.avatar_url
            embed = discord.Embed(description = f'[**{member}**]({avatar})', color = utilc)
            embed.set_image(url = avatar)
            await ctx.send(embed = embed)

    @commands.command()
    async def facts(self,ctx):
      x = randfacts.getFact()
      embed = discord.Embed(description = x,colour = utilc)
      embed.set_author(name = ctx.author,icon_url = ctx.author.avatar_url)
      await ctx.send(embed = embed)

    @commands.command()
    async def pokemon(self,ctx,*,pokemon):
        async with aiohttp.ClientSession() as session:
            message0 = await ctx.send("I am looking for that Pokemon. Please be patient.")
            await ctx.channel.trigger_typing()
            response = await session.get(f'https://some-random-api.ml/pokedex?pokemon={pokemon}')
            await ctx.channel.trigger_typing()
            if str(response.status) == "404":
                embed = discord.Embed(description = 'I couldn\'t find that pokemon. Please try again.',colour = utilc)
                embed.set_author(name = ctx.author,icon_url=ctx.author.avatar_url)
            else:
                rj = await response.json()
                name = (rj['name']).capitalize()
                pid = (rj['id'])
                ptype = (rj['type'])
                desc = (rj['description'])
                species = (rj['species'])
                stats = (rj['stats'])
                evolfam = (rj['family'])
                evs = (evolfam['evolutionLine'])
                evs=str(evs)
                evs=evs.replace("'","")
                evs=evs.replace("]","")
                evs=evs.replace("[","")
                hp = (stats['hp'])
                attack = (stats['attack'])
                defense = (stats['defense'])
                speed = (stats['speed'])
                spattack = (stats['sp_atk'])
                spdef = (stats['sp_def'])
                abilities = (rj['abilities'])
                abilities = str(abilities)
                abilities=abilities.replace("'","")
                abilities=abilities.replace("[","")
                abilities=abilities.replace("]","")
                weight = (rj['weight'])
                height = (rj['height'])
                weight = weight.replace(u'\xa0', u' ')
                height = height.replace(u'\xa0', u' ')
                species = str(species)
                species=species.replace("'","")
                species=species.replace("[","")
                species=species.replace("]","")
                species=species.replace(",","")
                ptype = str(ptype)
                ptype=ptype.replace("'","")
                ptype=ptype.replace("[","")
                ptype=ptype.replace("]","")
                imgs=(rj['sprites'])
                img = imgs['animated'] if int(rj['generation']) < 6 else imgs['normal']
                url = (imgs['normal'])
                try:
                    idx = await session.get(url)
                    idx = await idx.read()
                    #await url.save(f'{pokemon}av.png',seek_begin = True)
                    embed=discord.Embed(title=name,description=desc,color=random.randint(0, 0xFFFFFF))
                except:
                    embed=discord.Embed(title=name,description=desc)
                embed.set_thumbnail(url=img)
                embed.add_field(name="Information",value=f"Pokedex Entry: {pid}\nFirst introduced in generation {(rj['generation'])}\nType(s): {ptype}\nAbilities: {abilities}",inline=True)
                embed.add_field(name="Base Stats",value=f"HP: {hp}\nDefense: {defense}\nSpeed: {speed}\nAttack: {attack}\nSpecial Attack: {spattack}\nSpecial Defense: {spdef}",inline=True)
                if len(evs) != 0:
                    embed.add_field(name="Evolution Line",value=evs,inline=True)
                await ctx.channel.trigger_typing()
                await message0.delete()

            await ctx.send(embed = embed)
    @commands.command()
    async def ping(self,ctx):
        embed = discord.Embed(title = 'Ping',description = f'```\nPing: {round(self.client.latency*1000)}```',color = utilc,timestamp = datetime.datetime.now())
        await ctx.send(embed = embed)

    @commands.command()
    async def stats(self,ctx):
        embed = discord.Embed(title = 'Stats',description = f'```\nServers: {len(self.client.guilds)}\nUsers:{sum(g.member_count for g in self.client.guilds)}\nCPU:{psutil.cpu_percent()}%\nLibrary: Dpy```',colour = utilc,timestamp = datetime.datetime.now())
        await ctx.send(embed = embed)

    @commands.command(aliases = ["si", "guildinfo", 'gi'])
    async def serverinfo(self, ctx):
        findbots = sum(1 for member in ctx.guild.members if member.bot)
        roles = sum(1 for role in ctx.guild.roles)

        embed = discord.Embed(title = 'Infomation about ' + ctx.guild.name + '.', colour = utilc)
        embed.set_thumbnail(url = str(ctx.guild.icon_url))
        embed.add_field(name = "Guild's name: ", value = ctx.guild.name,inline = False)
        embed.add_field(name = "Guild's owner: ", value = f'{str(ctx.guild.owner.mention)}', inline = False)
        embed.add_field(name = "Guild's verification level: ", value = str(ctx.guild.verification_level),inline = False)
        embed.add_field(name = "Guild's id: ", value = f"{ctx.guild.id}",inline = False)
        embed.add_field(name = "Guild's member count: ", value = f"{ctx.guild.member_count}",inline = False)
        embed.add_field(name="Bots", value=f"{findbots}",inline = False)
        embed.add_field(name = "Guild created at: ", value = str(ctx.guild.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC")),inline = False)
        embed.add_field(name = "Number of Roles:", value = f"{roles}",inline = False)
        embed.add_field(name = 'Total Channels:',value = len(ctx.guild.text_channels) + len(ctx.guild.voice_channels),inline = False)
        embed.set_footer(text='Bot Made by Team Frixion')
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed =  embed)

    @commands.command(aliases = ["ci"])
    async def channelinfo(self, ctx, channel : discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        em = discord.Embed(title = f"Info about {channel.name}", color = utilc, description = f"Here is an insight into {channel.mention}")
        em.add_field(name = "ID:", value = f"`{channel.id}`")
        em.add_field(name = "Name:", value = f"`{channel.name}`")
        em.add_field(name = "Server it belongs to:", value = f"{channel.guild.name}", inline = True)

        try:
            em.add_field(name = "Category ID:", value = f"`{channel.category_id}`", inline = False)
        except:
            pass
        em.add_field(name = "Topic:", value = f"`{channel.topic}`")
        em.add_field(name = "Slowmode:", value = f"`{channel.slowmode_delay}`", inline = True)

        em.add_field(name = "People who can see the channel:", value = f"`{len(channel.members)}`", inline = False)
        em.add_field(name = "Is NSFW:", value = f"`{channel.is_nsfw()}`")
        em.add_field(name = "Is News:", value = f"`{channel.is_news()}`", inline = True)

        em.set_footer(text = "invite me ;)", icon_url = ctx.author.avatar_url)
        em.set_thumbnail(url = str(ctx.guild.icon_url))
        em.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed = em)

    @commands.command(aliases=['ui'])
    async def userinfo(self, ctx, member :discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title = "👤 Info", color = utilc, description = f"Information about:**{member.name}**")
        embed.add_field(name = "Nickname", value = member.nick or None,inline = False)
        embed.add_field(name = "Verification Pending", value = member.pending,inline = False)
        embed.add_field(name = "Status:", value = member.raw_status,inline = False)
        embed.add_field(name = "Color", value = member.color,inline = False)
        embed.add_field(name = "Mention:", value = member.mention,inline = False)
        embed.add_field(name = "Top Role:", value = member.top_role.mention,inline = False)

        embed.set_thumbnail(url = member.avatar_url)
        embed.set_footer(icon_url=member.avatar_url, text=f'Requested By: {ctx.author.name}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['members'])
    async def membercount(self,ctx):
        embed = discord.Embed(title = 'Membercount',description = f'```{(ctx.guild.member_count)}```',colour = discord.Color.random(),timestamp = datetime.datetime.now())
        await ctx.send(embed = embed)

    @commands.command()
    async def distance(self,ctx,latitude1:float,longitude1:float,latitude2:float,long2:float):
        cord1 = (latitude1,longitude1)
        cord2 = (latitude2,long2)
        a = hv.haversine(cord1,cord2)

        embed = discord.Embed(title = 'Distance',description = f'```Lat1/lon1: {latitude1},{longitude1}\nLat2/Lon2: {latitude2}:{long2}\n{round(a)} kilometers```',color = discord.Color.random(),timestamp = datetime.datetime.now())
        await ctx.reply(embed = embed)

    @distance.error
    async def diserror(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
          embed = discord.Embed(title = 'Error',description = 'The required Arguments were missing.\n```{prefix}distance [latitude1] [longitude1] [latitude2] [longitude2]```')
          await ctx.reply(embed = embed)

    @commands.command()
    async def banner(self,ctx,member:discord.Member=None):
        if member is None:
            member = ctx.author
        
        user_ = await self.client.fetch_user(int(member.id))
        banner = user_.banner.url
        embed = discord.Embed(description = f'[**{member}**]({banner})')
        embed.set_image(url = banner)
        await ctx.send(embed = embed)

def setup(client):
	client.add_cog(Utils(client))