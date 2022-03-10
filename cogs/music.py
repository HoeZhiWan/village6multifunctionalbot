import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
from time import sleep
 
rpgmusicpath = r"path\to\music.mp3"
 
class Music(commands.Cog):
    def __init__(self, client):
        self.bot = client
 
    @commands.Cog.listener()
    async def on_ready(self):
        print('Music cog successfully loaded.')
       
       
    @commands.command(pass_context=True)
    async def rpgmusic(ctx, self):
        await self.join(ctx)
        await ctx.send(f'Playing some RPG music in {ctx.message.author.voice.channel}.')
        sleep(3)
        voice.play(discord.FFmpegPCMAudio('rpgmusic.mp3'), after=lambda e: print(f'RPG music in {ctx.message.author.voice.channel} has finished playing.'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.05
 
   
    @commands.command(pass_context=True)
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
 
        if voice and voice.is_connected():
            await voice.move_to(channel)
 
        else:
            voice = await channel.connect()
            print(f'Bot connected to voice channel {channel}\n')
 
        await ctx.send(f'I joined {channel}.')
   
 
    @commands.command(pass_context=True)
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
   
        if voice and voice.is_connected():
            await voice.disconnect()
            print(f'Bot disconnected from channel {channel}.')
       
        else:
            print('Not able to disconnect to a voice channel because bot wasn\'t in one.')
       
    @commands.command(pass_context=True)
    async def play(self, ctx, url: str):
        song_there = os.path.isfile('song.mp3')
        try:
            if song_there:
                os.remove('song.mp3')
                print('Removed current song.')
        except PermissionError:
            print('Error in deleting song file. (Song in use.)')
            await ctx.send('Unable to request song. (Song already in use.)')
            return
   
        await ctx.send('Preparing song. Please wait.')
        voice = get(self.bot.voice_clients, guild=ctx.guild)
 
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading audio now.\n')
            ydl.download([url])
 
        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                name = file
                print(f'Renamed File: {file}.')
                os.rename(file, 'song.mp3')
 
        voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print(f'{name} has finished playing.'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.06
 
        name = name.rsplit('-', 2)
        await ctx.send(f'Now playing {name}.')
        print('Now playing.\n')
 
 
def setup(bot):
    bot.add_cog(Music(bot))