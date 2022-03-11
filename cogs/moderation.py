from discord.ext import commands
import discord
from antispam import AntiSpamHandler
from profanity_filter import ProfanityFilter
import spacy

try:
    nlp = spacy.load("en")
except: # If not present, we download
    spacy.cli.download("en")
    nlp = spacy.load("en")
pf = ProfanityFilter()
pf.censor_char = '@'

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        if pf.is_profane(message.content):
            await message.delete()
            msg = pf.censor(message.content)
            embed = discord.Embed(title="Profanity Detected!",description=msg, color=discord.Color.red())
            embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
            await message.channel.send(embed=embed)
    
        if message.content.startswith("Hello"):
            await message.channel.send("World")
        
        await self.bot.handler.propagate(message)

        
def setup(bot):
    bot.add_cog(Moderation(bot))