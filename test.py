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
    
    if message.content.startswith("Hello"):
        await message.channel.send("World")
        
@client.command()
async def ping(ctx):
    await ctx.reply(f"Pong! {round(client.latency * 1000)}ms latency.")
        
client.run(os.environ['DISCORD_TOKEN'])