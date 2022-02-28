import discord
from discord.ext import commands

class Nick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tick = '<:tick:879670104000954400>'
        self.cross = '<:Cross:879670127707193364>'

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} is ready!')

    @commands.command(aliases=['sn'])
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def setnick(self, ctx, member:discord.Member=None, *, newnick=None):
        if member is None or newnick is None:
            return await ctx.send("Please provide a user/new nickname.")
        try:
            await member.edit(nick = newnick)
        except discord.Forbidden:
            return await ctx.send(f"{self.cross} **I don't have permission to do so!**")
        except discord.HTTPException:
            return await ctx.send(f"{self.cross} **Something went wrong!**")
        embed = discord.Embed(
            title = "Nickname changed",
            description = f'{ctx.author.mention} changed {member.mention}\'s nick name',
            color = discord.Color.yellow()
        )
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Nick(bot))
