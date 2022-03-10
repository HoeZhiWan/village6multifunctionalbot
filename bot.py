import discord
from discord.ext import commands
from profanity_filter import ProfanityFilter
import spacy
import pyjokes
import os
        
client = commands.Bot(command_prefix=".")

try:
    nlp = spacy.load("en")
except: # If not present, we download
    spacy.cli.download("en")
    nlp = spacy.load("en")
pf = ProfanityFilter()
pf.censor_char = '@'

joke = pyjokes.get_joke(language='en', category= 'neutral')
print(joke)
        
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
        
@client.event
async def on_message(message):
    if pf.is_profane(message.content):
        await message.delete()
        msg = pf.censor(message.content)
        embed = discord.Embed(title="Profanity Detected!",description=msg, color=discord.Color.red())
        embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
        await message.channel.send(embed=embed)
        
@client.command(help="A random nerdy joke")
async def joke(ctx):
    joke = pyjokes.get_joke(language='en', category= 'neutral')
    print(joke)
    await ctx.reply(joke)
        
client.run(os.environ['DISCORD_TOKEN'])