import discord

async def mod_emb_maker(channel, title, desc, color, footer, moderator, reason):
    embed = discord.Embed(title = title, description = desc, colour = color)
    embed.add_field(name="Moderator:", value="```{}```".format(moderator))
    embed.add_field(name="Reason:", value="```{}```".format(reason))
    embed.set_footer(text = footer)
    await channel.send(embed = embed)

async def success_emb_maker(channel, title, desc, color, footer, moderator, reason):
    embed = discord.Embed(title = f"<:tick:879670104000954400> {title}", description = desc, colour = color)
    embed.add_field(name="Moderator:", value="```{}```".format(moderator))
    embed.add_field(name="Reason:", value="```{}```".format(reason))
    embed.set_footer(text = footer)
    await channel.send(embed = embed)

async def fail_emb_maker(channel, title, desc, color, footer, moderator, reason):
    embed = discord.Embed(title = f"<:Cross:879670127707193364> {title}", description = desc, colour = color)
    embed.add_field(name="Moderator:", value="```{}```".format(moderator))
    embed.add_field(name="Reason for fail:", value="```{}```".format(reason))
    embed.set_footer(text = footer)
    await channel.send(embed = embed)