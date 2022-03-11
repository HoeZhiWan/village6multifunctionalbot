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

    url = requests.get(movie_url).text
    soup = BeautifulSoup(url, 'lxml')

    plot = soup.find('ul', id="plot-summaries-content")
    if plot:
      summary = plot.p.text
    else:
      summary = f"No summary found for {title}"

    if soup.find("img", class_='poster'):
      img = soup.find("img", class_='poster')['src']
    title_block = soup.find('h3', itemprop="name")

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
  embed.set_thumbnail(url=img)
  return embed

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
    async def img(self, ctx *, tag="Programmer"):
        """Getting a random image and output"""
        embed = discord.Embed(title="Image!",colour=discord.Colour.blue())
        embed.set_image(url=random.choice(gis_function(tag)))
        await ctx.reply(embed=embed)
        await ctx.message.add_reaction("🟢")
        

def setup(bot):
    bot.add_cog(Misc(bot))