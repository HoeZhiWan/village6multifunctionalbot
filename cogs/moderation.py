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
        self.bot.handler = AntiSpamHandler(self.bot)

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
        
        await self.bot.handler.propagate(message)
        
    @commands.command()
    async def clear(self, ctx, amount=None):
        """Clear a specified amount of message"""
        amount = amount or 10
        try:
            int(amount)
        except:
            return await ctx.reply("Please provide a valid number")
        amount += 1
        await ctx.channel.purge(limit=amount)
        
def setup(bot):
    bot.add_cog(Moderation(bot))