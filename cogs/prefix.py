import discord
from discord.ext import commands
import pymongo

cluster = pymongo.MongoClient(
    "mongodb+srv://team_frixion:K68aPkZDhwkCw6h@cluster0.h68nl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["bolt"]
collection = db["prefix"]

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tick = '<:tick:879670104000954400>'
        self.cross = '<:Cross:879670127707193364>'

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} is ready!')

    @commands.command()
    async def prefix(self, ctx, mode=None, prefix=None):
        if not mode:
            return await ctx.send(f"{self.cross} **Please specify a mode!\nFor ex: `set`, `reset`**\n\n**Usage:** `{ctx.prefix}prefix <mode> [new_prefix]`")

        if mode.lower() != 'set':
            return await ctx.reply(f"{self.cross} **Please specify a proper mode!\nFor ex: `set`, `default`**")
        if mode.lower() == 'reset':
            db.collection.update_one(
                {"_id": ctx.guild.id},
                {"$set": {"prefix": 'b.'}}
            )
        if not prefix:
            return await ctx.send(f"{self.cross} **Please specify a prefix!\nFor ex: `{ctx.prefix}prefix set <new_prefix>`**")
        try:
            db.collection.update_one(
                {"_id": ctx.guild.id},
                {"$set": {"prefix": str(prefix)}}
            )
        except Exception as e:
            print(f"There was an error!\n{e}")

        await ctx.send(f"{self.tick} **Prefix set to `{prefix}`**")

def setup(bot):
    bot.add_cog(Prefix(bot))
