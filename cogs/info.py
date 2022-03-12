from discord.ext import commands
import discord
from bs4 import BeautifulSoup
import requests
from string import ascii_letters
import re

def find_paragraph(url):
    r = requests.get(url)
    doc = BeautifulSoup(r.text,'html.parser')

    all = doc.find_all('p')
    if all:
        for i in all:
            if len(i.text) != 0:
                if len([y for y in ascii_letters if y in i.text]):
                    return i.text
    else:
      return doc.find('body').text
  
def scrape_rates():
    url = 'https://mtradeasia.com/main/daily-exchange-rates/'
    r = requests.get(url)
    doc = BeautifulSoup(r.text,'html.parser')
    exchange_rate = doc.find('tr',attrs={'class':'MY0100083'})
    rates = exchange_rate.find_all('td',attrs={'class':'text-center'})
    we_buy = rates[0].text
    we_sell = rates[1].text
    return we_buy.replace('\n',''), we_sell.replace('\n','')

def quotes_():
  r = requests.get("https://zenquotes.io/api/random", timeout=10)

  data = r.json()[0]

  author = data['a']
  quote = data['q']

  url = requests.get("https://zenquotes.io/authors", timeout=10).text
  soup = BeautifulSoup(url, 'lxml')

  img = soup.findAll('img', alt=re.compile(f"^{author}$", re.I))
  author_url = f"https://zenquotes.io{img[0].parent['href'].strip('..')}"

  embed = discord.Embed(title=quote, color=discord.Color.purple())
  embed.set_author(name=author,icon_url=img[0]['src'],url=author_url)
  
  return embed


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def scrape(self, ctx, url=None):
        """Scrapes the first paragraph of a website"""
        if url:
            await ctx.send(find_paragraph(url))
        else:
            await ctx.reply("URL can't leave blank")
        
    @commands.command(aliases=['currency'])
    async def rates(self, ctx):
        """Shows exchange rate between Ringgit Malaysia and US Dollar​"""  
        await ctx.send('Processing.... (This might take a while) ')
        rates = scrape_rates()
        string = f'We buy: {rates[0]}\nWe sell: {rates[1]}'
        await ctx.send(string)
        
    @commands.command()
    async def quotes(self, ctx):
        """Random Quotes from Famous People"""
        await ctx.reply(embed=quotes_())
        await ctx.message.add_reaction("🟢")
        
def setup(bot):
    bot.add_cog(Info(bot))