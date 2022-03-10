import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix=".")
        
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if pf.is_profane(message.content):
        await message.delete()
        msg = pf.censor(message.content)
        embed = discord.Embed(title="Profanity Detected!",description=msg, color=discord.Color.red())
        embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
        await message.channel.send(embed=embed)
    
    if message.content.startswith("Hello"):
        await message.channel.send("World")
        
@client.command()
async def ping(ctx):
    await ctx.reply(f"Pong! {round(client.latency * 1000)}ms latency.")
        
client.run(os.environ['DISCORD_TOKEN'])