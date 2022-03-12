from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup
import random
import os
from google_images_search import GoogleImagesSearch

google_api_key = os.getenv('google_api_key')
cse_code = "6ed98d73beaf19a75"
gis= GoogleImagesSearch(google_api_key, cse_code)
def gis_function(tag):
  _search_params= {
  'q': tag,
  'num': 10,
  'fileType': 'jpg|png',
  'safe': 'medium', ##
  'imgType': 'stock', ##
  'imgSize': 'medium', ##
  }
  gis.search(search_params=_search_params)
  print("Did a Google Image Search!")
  return [link.url for link in gis.results()]

def movie_(title):
  url = requests.get(f'https://www.imdb.com/find?q={title}&s=tt&ttype=ft&ref_').text
  soup = BeautifulSoup(url, 'lxml')

  movie_result = soup.find('td', class_='result_text')

  movie = f'https://www.imdb.com/find?q={title.replace(" ", "%20")}&s=tt&ttype=ft&ref_'
  img = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png"

  if movie_result:
    
    movie_url = f"https://www.imdb.com/{movie_result.a['href']}plotsummary/"
    movie = f"https://www.imdb.com/{movie_result.a['href']}"

    url2 = requests.get(movie_url).text
    soup2 = BeautifulSoup(url2, 'lxml')

    plot = soup2.find('ul', id="plot-summaries-content")
    if plot:
      summary = plot.p.text
    else:
      summary = "No summary found"

    try:
      url3 = requests.get(movie).text
      soup3 = BeautifulSoup(url3, 'lxml')

      mediaviewer = soup3.find('a', class_="ipc-lockup-overlay ipc-focusable")['href']

      url4 = requests.get(f"https://www.imdb.com{mediaviewer}").text
      soup4 = BeautifulSoup(url4, 'lxml')

      imageid = mediaviewer.split("/")[4]
      image_tag = f"{imageid}-curr"
      img = soup4.find("img", attrs={'data-image-id': image_tag})["src"]

    except:
      img = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png"
    
    title_block = soup2.find('h3', itemprop="name")

    name = title_block.a.text
    year = title_block.span.text.strip()

    if year:
      title_ = f'{name} {year}'
    else:
      title_ = name
      
  else:
    title_ = "No Results"
    summary = f'No result found for **"{title}"**'
  
  embed = discord.Embed(title=title_, color=0xFFFF00, url=movie, description=summary)
  if img == "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png":
    embed.set_thumbnail(url=img)
  else:
    embed.set_image(url=img)
  return embed

emoji_list = [letter for letter in "😀😁😂🤣😃😄😅😆😗🥰😘😍😎😋😊😉😙☺😚🙂🤗🤩🤔🤨😮😣😥😏🙄😶😑😐🤐😯😪😫🥱😴😌😛🙃😕😔😓😒🤤😝😜🤑😲☹🙁😖😞😟😤😬🤯😩😨😧😦😭😢😰😱🥵🥶😳🤪😵🥴🤮🤢🤕🤒😷😡🤬😠❤🧡💛💚💙💜🤎🖤💖💗💓💞💕❣💔🤍💘💝💟💌💢💥💤💦💨💫🕳🚛🚜🚲🦼🚕🚗🚑🦼🚜🚙🛹⛰🧭🗺🌏🏗🏘🌆🌅🌄🌃🌁⛺💈🛎🧳🌩🌦☁🌀🌬🌡🌚🌔🌖🌟🌞☀🌜🌛🌙⛄☃❄⚡⛱🔥💧🌊☔🌠☄🌡🌬👨‍👩‍👦‍👦👩‍❤️‍👩👨‍❤️‍👨💑🦿🦾🧠⛷🦴👀👁👥👤👩🏽‍🤝‍🧑🏿🎏🎎🎍🎗🎭🎁🎪🎨🧶🎑🎊👡👠🖊🖋📂📁✏🗒📤✒📦🖊📬🖌📆📍📋✂📐📇🖇⌚⏱🥠🥙🍚🍗🧇🥙🌮🍱🍤🍶🥂🥄🍺🍴🍽🧃🍨🍵🍶🍯🍾🍻🥃🍍🌿🌴🍃🌳🍁🍂🌲"]

def generate_emoji():
  return random.choice(emoji_list)

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def movie(self, ctx, *, title=None):
        """Get the summary of a specific movie"""
        if title:
            await ctx.reply(embed=movie_(title))
            await ctx.message.add_reaction("🟢")
        else:
            await ctx.reply("Title can't be empty")
            await ctx.message.add_reaction("🔴")
            
    @commands.command()
    async def img(self, ctx, *, tag=None):
        """Getting a random image and output"""
        tag = tag or "forest"
        embed = discord.Embed(title="Image!",colour=discord.Colour.blue())
        embed.set_image(url=random.choice(gis_function(tag)))
        await ctx.reply(embed=embed)
        await ctx.message.add_reaction("🟢")
        
    @commands.command()
    async def ping(self, ctx):
        """Ping with latency"""
        await ctx.reply(f"Pong! {round(self.bot.latency * 1000)}ms latency.")
        await ctx.message.add_reaction("🟢")
        
    @commands.command()
    async def emoji(self, ctx):
        """Give a random emoji"""
        await ctx.message.channel.send(generate_emoji())
        

def setup(bot):
    bot.add_cog(Misc(bot))