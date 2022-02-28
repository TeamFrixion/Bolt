import asyncio
import os
import pymongo

import discord
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.bans = True
intents.typing = True
intents.emojis = True
intents.voice_states = True
intents.reactions = True

cluster = pymongo.MongoClient("mongodb+srv://team_frixion:K68aPkZDhwkCw6h@cluster0.h68nl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["bolt"]
collection = db["prefix"]

async def get_prefix(client, message):
    prefix = db.collection.find_one({"_id": message.guild.id})
    if not prefix:
        return 'b.'
    return prefix["prefix"]


client = commands.Bot(command_prefix=get_prefix, owner_ids=[822730830027816960, 718712985371148309, 733650965269446666, 784287488697040896], intents=intents)
client.remove_command("help")

@tasks.loop(seconds=10)
async def ch_pr():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Helping in {len(client.guilds)} servers with {sum(g.member_count for g in client.guilds)} users."))
    await asyncio.sleep(5)
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name='@Bolt'
        )
    )
    await asyncio.sleep(5)

@client.event
async def on_ready():
    ch_pr.start()
    print(f"Logged in | {client.user.id}")
    await client.change_presence(status = discord.Status.online,activity = discord.Game(name = f'Helping maintain {len(client.guilds)} servers!'))

@client.event
async def on_guild_join(guild):
    if find := db.collection.find_one({"_id": guild.id}):
        db.collection.update_one({ "_id" : guild.id }, { "$inc" : { 'prefix':'b.' } })
    else:
        post = {
            '_id': guild.id,
            'prefix': 'b.'
        }
        db.collection.insert_one(post)

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(title = 'Thank you for adding me!',description = 'Thank you for adding Bolt to your server! Bolt is the discord bot to keep your server safe and active. Bolt has many Moderation and Utility commands. Use `b.help` to know about Bolt\'s commands and use `b.config` to configure Bolt.',colour = discord.Color.random())
            embed.set_image(url='https://cdn.discordapp.com/attachments/866687057001447434/892677381951742022/standard_3.gif')
            embed.set_footer(text='Support server - https://discord.gg/mfVKyxbkRn')
            await channel.send(embed = embed)
        break

@client.event
async def on_message(message):
    try:
        for i in message.mentions:
            if i == client.user:
                prefix_ = db.collection.find_one({"_id": message.guild.id})
                prefix = 'b.' if not prefix_ else prefix_["prefix"]
                await message.channel.send(f"Hey there! I am Bolt - A lightning fast moderation bot!\nMy prefix in this server is `{prefix}`")
    except:
        pass

    await client.process_commands(message)

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Loaded the extension")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("Unloaded the extension")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("Unloaded the extension")
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Loaded the extension")

for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run("ODgxMDgxMjU0NTU1MDI5NTE1.YSno3A.kWtaarSeTT3rbWDbNaPTarnHPGs")
