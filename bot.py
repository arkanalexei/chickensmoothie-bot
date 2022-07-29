from pydoc import cli
import sched
import time
import discord
import script
import os

TOKEN = os.getenv('TOKEN')

client = discord.Client()
default_channels = dict()
current_guild_id = 0

@client.event
async def on_ready():
    for guild in client.guilds:
        for channel in guild.text_channels: #getting only text channels
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(f'{client.user} is now online!')
                print(f'{client.user} is now online!')
                default_channels[guild.id] = channel.id
                loop_timer(guild.id)
                break

@client.event
async def on_message(message):
    if message.author == client.user: # if message author is the bot itself
        return

    if message.content.startswith('$$'):
        channel = message.channel
        current_guild_id = message.guild.id
        default_channels[current_guild_id] = channel
        
        command = message.content.split(" ")[0][2:]
        
        if command == "timer":
            await channel.send(script.get_msg())
            
        elif command == "default":
            await channel.send("This is the default channel.")
            
        elif command == "z":
            await channel.send("z")
            
        else:
            await channel.send("i dont know what you're asking me to do lol")
    
        
@client.event
async def on_command(command):
    guild = client.get_guild(current_guild_id)
    channel = default_channels[guild.id]
    await channel.send('Command detected')
    
def loop_timer(g_id=None):
    print("@@@@@@@@@@@@@@@ Timer is running @@@@@@@@@@@@@@@")
    loop = sched.scheduler(time.time, time.sleep)
    loop.enter(script.DELAY_IN_MINUTES * 60, 1, await_timer, (g_id,))
    loop.run()

def await_timer(g_id=None):
    timer(g_id)
    
async def timer(g_id=None):
    if g_id == None:
        guild = client.get_guild(current_guild_id)
        channel_id = default_channels[guild.id]
    else:
        channel_id = default_channels[g_id]
    
    channel = client.get_channel(channel_id)
    await channel.send(script.get_msg())
        
client.run(TOKEN)
