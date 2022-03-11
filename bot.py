import discord
from discord.ext import commands
from profanity_filter import ProfanityFilter
import spacy
import pyjokes
import os
from music import Player
import discordantispam 
        
try:
    nlp = spacy.load("en")
except: # If not present, we download
    spacy.cli.download("en")
    nlp = spacy.load("en")
pf = ProfanityFilter()
pf.censor_char = '@'

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

client = commands.Bot(command_prefix=".", intents=intents)
client.handler = discordantispam.AntiSpamHandler(client)
        
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
    await client.wait_until_ready()
    client.add_cog(Player(client))
        
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
        
    await client.handler.propagate(message)
    await client.process_commands(message)
        
    await client.process_commands(message)
        
@client.command()
async def ping(ctx):
    await ctx.reply(f"Pong! {round(client.latency * 1000)}ms latency.")
        
@client.command(help="A random nerdy joke")
async def joke(ctx):
    joke = pyjokes.get_joke(language='en', category= 'neutral')
    await ctx.reply(f"{joke}")
    
client.load_extension("cogs.greetings")

#something
    
client.run(os.environ['DISCORD_TOKEN'])