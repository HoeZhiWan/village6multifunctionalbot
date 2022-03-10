import discord
        
client = discord.Client()
        
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
        
@client.event
async def on_message(message):
    if message.content == "Hello":
        await message.channel.send("World")
        
client.run("OTUwNjgxNzc2NDEyNTg2MDM0.YicdZg.BdENafnuhq19ghAETUu0n4XRriQ")