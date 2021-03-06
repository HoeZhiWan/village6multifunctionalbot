import discord
from discord.ext import commands
import os

#cogs
from music import Music

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

client = commands.Bot(command_prefix=".", intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    await client.wait_until_ready()
    client.add_cog(Music(client))

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return
#
#    await client.process_commands(message)

#cogs
client.load_extension("cogs.info")
client.load_extension("cogs.misc")
client.load_extension("cogs.fun")
client.load_extension("cogs.moderation")
client.load_extension("cogs.greetings")

client.run(os.environ['DISCORD_TOKEN'])
