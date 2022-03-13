from discord.ext import commands
import pyjokes
import discord
import random
import asyncio
import giphy_client
from giphy_client.rest import ApiException

emoji_list = [letter for letter in "😀😁😂🤣😃😄😅😆😗🥰😘😍😎😋😊😉😙☺😚🙂🤗🤩🤔🤨😮😣😥😏🙄😶😑😐🤐😯😪😫🥱😴😌😛🙃😕😔😓😒🤤😝😜🤑😲☹🙁😖😞😟😤😬🤯😩😨😧😦😭😢😰😱🥵🥶😳🤪😵🥴🤮🤢🤕🤒😷😡🤬😠❤🧡💛💚💙💜🤎🖤💖💗💓💞💕❣💔🤍💘💝💟💌💢💥💤💦💨💫🕳🚛🚜🚲🦼🚕🚗🚑🦼🚜🚙🛹⛰🧭🗺🌏🏗🏘🌆🌅🌄🌃🌁⛺💈🛎🧳🌩🌦☁🌀🌬🌡🌚🌔🌖🌟🌞☀🌜🌛🌙⛄☃❄⚡⛱🔥💧🌊☔🌠☄🌡🌬👨‍👩‍👦‍👦👩‍❤️‍👩👨‍❤️‍👨💑🦿🦾🧠⛷🦴👀👁👥👤👩🏽‍🤝‍🧑🏿🎏🎎🎍🎗🎭🎁🎪🎨🧶🎑🎊👡👠🖊🖋📂📁✏🗒📤✒📦🖊📬🖌📆📍📋✂📐📇🖇⌚⏱🥠🥙🍚🍗🧇🥙🌮🍱🍤🍶🥂🥄🍺🍴🍽🧃🍨🍵🍶🍯🍾🍻🥃🍍🌿🌴🍃🌳🍁🍂🌲"]

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
                "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
                "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
                "Yes.", "Yes – definitely.", "You may rely on it."]
    return f"Question: {question}\nAnswer: {random.choice(responses)}"

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
        """Shows a random GIF regarding the topic​"""
        for i in args:
            topic += ' ' + i
        await ctx.send(embed=generate_embed_gif(topic))

        
def setup(bot):
    bot.add_cog(Fun(bot))