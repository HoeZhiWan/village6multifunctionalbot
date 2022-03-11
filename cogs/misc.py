from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup

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
        self._last_member = None

    @commands.command()
    async def movie(self, ctx, *, title=None):
        """Get the summary of a specific movie"""
        if title:
            await ctx.reply(embed=movie_(title))
            await ctx.message.add_reaction("🟢")
        else:
            await ctx.reply("Title can't be empty")
            await ctx.message.add_reaction("🔴")
        
def setup(bot):
    bot.add_cog(Misc(bot))