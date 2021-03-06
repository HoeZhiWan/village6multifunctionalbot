from discord.ext import commands
import pyjokes
import discord
import random
import asyncio
import giphy_client
from giphy_client.rest import ApiException

emoji_list = [letter for letter in "๐๐๐๐คฃ๐๐๐๐๐๐ฅฐ๐๐๐๐๐๐๐โบ๐๐๐ค๐คฉ๐ค๐คจ๐ฎ๐ฃ๐ฅ๐๐๐ถ๐๐๐ค๐ฏ๐ช๐ซ๐ฅฑ๐ด๐๐๐๐๐๐๐๐คค๐๐๐ค๐ฒโน๐๐๐๐๐ค๐ฌ๐คฏ๐ฉ๐จ๐ง๐ฆ๐ญ๐ข๐ฐ๐ฑ๐ฅต๐ฅถ๐ณ๐คช๐ต๐ฅด๐คฎ๐คข๐ค๐ค๐ท๐ก๐คฌ๐ โค๐งก๐๐๐๐๐ค๐ค๐๐๐๐๐โฃ๐๐ค๐๐๐๐๐ข๐ฅ๐ค๐ฆ๐จ๐ซ๐ณ๐๐๐ฒ๐ฆผ๐๐๐๐ฆผ๐๐๐นโฐ๐งญ๐บ๐๐๐๐๐๐๐๐โบ๐๐๐งณ๐ฉ๐ฆโ๐๐ฌ๐ก๐๐๐๐๐โ๐๐๐โโโโกโฑ๐ฅ๐ง๐โ๐ โ๐ก๐ฌ๐จโ๐ฉโ๐ฆโ๐ฆ๐ฉโโค๏ธโ๐ฉ๐จโโค๏ธโ๐จ๐๐ฆฟ๐ฆพ๐ง โท๐ฆด๐๐๐ฅ๐ค๐ฉ๐ฝโ๐คโ๐ง๐ฟ๐๐๐๐๐ญ๐๐ช๐จ๐งถ๐๐๐ก๐ ๐๐๐๐โ๐๐คโ๐ฆ๐๐ฌ๐๐๐๐โ๐๐๐โโฑ๐ฅ ๐ฅ๐๐๐ง๐ฅ๐ฎ๐ฑ๐ค๐ถ๐ฅ๐ฅ๐บ๐ด๐ฝ๐ง๐จ๐ต๐ถ๐ฏ๐พ๐ป๐ฅ๐๐ฟ๐ด๐๐ณ๐๐๐ฒ"]

def generate_gif(q,limit):
    api_instance = giphy_client.DefaultApi()
    api_key = 'dc6zaTOxFJmzC'

    offset = 0 
    rating = 'g' 
    lang = 'en'
    fmt = 'json'

    try:
        api_response = api_instance.gifs_search_get(api_key, q, limit=limit, offset=offset, lang=lang,
                                                    fmt=fmt)
        api_response = repr(api_response)
        lst = list()
        url = eval(api_response)
        for i in url['data']:
            lst.append(i['images']['downsized']['url'])
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
    try:
      return random.choice(lst)
    except:
        return"https://media4.giphy.com/media/zLCiUWVfex7ji/giphy.gif?cid=e1bb72ff1iuai32kxryjxrkiuvm7v8koh2jn8c2n4hj7i3x1&rid=giphy.gif&ct=g"

def generate_emoji():
  return random.choice(emoji_list)

def generate_embed_gif(topic):
  embed = discord.Embed(title="Gifs Function ON", description=f"Sending GIF:\n", color=discord.Color.from_rgb(r(), r(), r()))
  embed.set_image(url=generate_gif(topic,100))
  embed.set_footer(text='--- Successful ---')

  return embed

def ball_gen(question):
    responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
                "Donโt count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
                "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
                "Yes.", "Yes โ definitely.", "You may rely on it."]
    return f"Question: {question}\nAnswer: {random.choice(responses)}"
    
def r():
  return random.randint(0,255)

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def emoji(self, ctx):
        """Give a random emoji"""
        await ctx.message.channel.send(generate_emoji())

    @commands.command()
    async def joke(self, ctx):
        """A random nerdy joke"""
        joke = pyjokes.get_joke(language='en', category= 'neutral')
        await ctx.reply(f"{joke}")

    @commands.command()
    async def rps(self, ctx):
        """Play a Rock Paper Scissors game with the bot"""

        await ctx.message.add_reaction("๐ข")

        msg = await ctx.send("Choose :rock: for Rock, :roll_of_paper: for Paper, and :scissors: for Scissors")

        for emoji in ['๐ชจ',"๐งป", "โ๏ธ"]:
            await msg.add_reaction(emoji)

        check = lambda r, u: u == ctx.author and str(r.emoji) in "๐ชจโ๏ธ๐งป" and r.message.id == msg.id # r=reaction, u=user, m=message

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

        comp_choice = random.choice(["๐ชจ","๐งป","โ๏ธ"])
        if str(reaction.emoji) == comp_choice:
            await msg.edit(content=draw())
        elif str(reaction.emoji) == "๐ชจ":
            if comp_choice == "โ๏ธ":
                await msg.edit(content=win())
                await ctx.message.add_reaction("๐")
                await msg.add_reaction("๐ฅ")
            elif comp_choice == "๐งป":
                await msg.edit(content=lose())
                await msg.add_reaction("๐")
                await ctx.message.add_reaction("๐ฅ")
        elif str(reaction.emoji) == "๐งป":
            if comp_choice == "๐ชจ":
                await msg.edit(content=win())
                await ctx.message.add_reaction("๐")
                await msg.add_reaction("๐ฅ")
            elif comp_choice == "โ๏ธ":
                await msg.edit(content=lose())
                await msg.add_reaction("๐")
                await ctx.message.add_reaction("๐ฅ")
        elif str(reaction.emoji) == "โ๏ธ":
            if comp_choice == "๐งป":
                await msg.edit(content=win())
                await ctx.message.add_reaction("๐")
                await msg.add_reaction("๐ฅ")
            elif comp_choice == "๐ชจ":
                await msg.edit(content=lose())
                await msg.add_reaction("๐")
                await ctx.message.add_reaction("๐ฅ")
        else:
            await msg.edit(content="Game cancelled!")
        for emoji in ['๐ชจ',"๐งป", "โ๏ธ"]:
            await msg.clear_reaction(emoji)
        await ctx.message.clear_reaction("๐ข")
        
    @commands.command()
    async def start_game():
        """Start a game of Tic Tac Toe!"""
        return

    @commands.command(aliases=['8ball','eightball'])
    async def _8ball(self, ctx,*,question):
        """Ask a yes/no question, get a lifechanging answer"""
        await ctx.send(ball_gen(question))

    @commands.command()
    async def gif(self, ctx, topic='cute', *args):
        """Shows a random GIF regarding the topicโ"""
        for i in args:
            topic += ' ' + i
        await ctx.send(embed=generate_embed_gif(topic))

        
def setup(bot):
    bot.add_cog(Fun(bot))