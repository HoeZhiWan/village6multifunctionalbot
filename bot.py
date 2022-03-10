import discord
from discord.ext import commands
from profanity_filter import ProfanityFilter
import spacy
import pyjokes
import os
        
try:
    nlp = spacy.load("en")
except: # If not present, we download
    spacy.cli.download("en")
    nlp = spacy.load("en")
pf = ProfanityFilter()
pf.censor_char = '@'

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
        
    await client.process_commands(message)
        
@client.command()
async def ping(ctx):
    await ctx.reply(f"Pong! {round(client.latency * 1000)}ms latency.")
        
@client.command(help="A random nerdy joke")
async def joke(ctx):
    joke = pyjokes.get_joke(language='en', category= 'neutral')
    await ctx.reply(f"{joke}")
    
class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member
        
client.run(os.environ['DISCORD_TOKEN'])