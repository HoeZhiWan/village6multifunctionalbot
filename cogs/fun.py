from discord.ext import commands
import pyjokes
import discord
import random
import asyncio

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joke(self, ctx):
        """A random nerdy joke"""
        joke = pyjokes.get_joke(language='en', category= 'neutral')
        await ctx.reply(f"{joke}")
        
    @commands.command()
    async def rps(self, ctx):
        """Play a Rock Paper Scissors game with the bot"""
        
        await ctx.message.add_reaction("🟢")
  
        msg = await ctx.send("Choose :rock: for Rock, :roll_of_paper: for Paper, and :scissors: for Scissors")
  
        for emoji in ['🪨',"🧻", "✂️"]:
            await msg.add_reaction(emoji)
      
        check = lambda r, u: u == ctx.author and str(r.emoji) in "🪨✂️🧻" and r.message.id == msg.id # r=reaction, u=user, m=message
  
        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30)
        except asyncio.TimeoutError:
            await msg.edit(content="Game cancelled.")
            return

        win_response = ["You win this time!", "I will get you next time!", "Gosh darn it!", 'Thank you for winning...', "Do you like the trophy?"]
        lose_response = ["Hah, good luck next time!", "I am the best!", "Tough luck!", "Try and try again... to fail.", "The champion is me!"]
        draw_response = ["Keep in mind that I will win", "Another round?", "Let's go another round!"]

        def win():
            return f"You picked {str(reaction.emoji)} and I picked {comp_choice}. {random.choice(win_response)}"
        def lose():
            return f"You picked {str(reaction.emoji)} and I picked {comp_choice}. {random.choice(lose_response)}"
        def draw():
            return f"You and I picked {comp_choice}. {random.choice(draw_response)}"
  
        comp_choice = random.choice(["🪨","🧻","✂️"])
        if str(reaction.emoji) == comp_choice:
            await msg.edit(content=draw())
        elif str(reaction.emoji) == "🪨":
            if comp_choice == "✂️":
                await msg.edit(content=win())
                await ctx.message.add_reaction("👑")
                await msg.add_reaction("🥉")
            elif comp_choice == "🧻":
                await msg.edit(content=lose())
                await msg.add_reaction("👑")
                await ctx.message.add_reaction("🥉")
        elif str(reaction.emoji) == "🧻":
            if comp_choice == "🪨":
                await msg.edit(content=win())
                await ctx.message.add_reaction("👑")
                await msg.add_reaction("🥉")
            elif comp_choice == "✂️":
                await msg.edit(content=lose())
                await msg.add_reaction("👑")
                await ctx.message.add_reaction("🥉")
        elif str(reaction.emoji) == "✂️":
            if comp_choice == "🧻":
                await msg.edit(content=win())
                await ctx.message.add_reaction("👑")
                await msg.add_reaction("🥉")
            elif comp_choice == "🪨":
                await msg.edit(content=lose())
                await msg.add_reaction("👑")
                await ctx.message.add_reaction("🥉")
        else:
            await msg.edit(content="Game cancelled!")
        for emoji in ['🪨',"🧻", "✂️"]:
            await msg.clear_reaction(emoji)
        await ctx.message.clear_reaction("🟢")
        
def setup(bot):
    bot.add_cog(Fun(bot))