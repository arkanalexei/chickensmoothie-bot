import discord
import script
import os

# Discord Bot token
TOKEN = os.getenv('TOKEN')

# Logging into the discord client with minimal intents required.
bot_intent = discord.Intents.default()
bot_intent.messages = True
bot_intent.message_content = True
bot_intent.members = True

client = discord.Client(intents=bot_intent)
default_channels = dict()
current_guild_id = 0

# Variables
CMD_PREFIX = '$$'

@client.event
async def on_ready():
    ''' The function that runs first thing once bot is running. '''
    for guild in client.guilds:
        for channel in guild.text_channels: #getting only text channels
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(f'{client.user} is now online!')
                print(f'{client.user} is now up and running.')
                default_channels[guild.id] = channel.id
                break

@client.event
async def on_message(message):
    ''' The function that runs upon detecting a message.'''
    # if message author is the bot itself, do nothing
    if message.author == client.user:
        return

    # if message begins with bot's prefix, detect for instructions
    if message.content.startswith(CMD_PREFIX):
        channel = message.channel
        current_guild_id = message.guild.id
        default_channels[current_guild_id] = channel
        
        command = message.content.split(" ")[0][2:]
        
        if command == "timer":
            await channel.send(script.get_msg())
        elif command == "setprefix":
            # TODO
            await channel.send(" ")
        else:
            await channel.send("Unknown command.")
    
        
@client.event
async def on_command(command):
    ''' The function that runs when a user executes a slash command.'''
    guild = client.get_guild(current_guild_id)
    channel = default_channels[guild.id]
    await channel.send('Command detected')
    
    
# # --------------- Non-Async Functions ---------------
# def loop_timer(g_id=None):
#     print("@@@@@@@@@@@@@@@ Timer is running @@@@@@@@@@@@@@@")
#     loop = sched.scheduler(time.time, time.sleep)
#     loop.enter(script.DELAY_IN_MINUTES * 60, 1, await_timer, (g_id,))
#     loop.run()

# def await_timer(g_id=None):
#     timer(g_id)
    
# async def timer(g_id=None):
#     if g_id == None:
#         guild = client.get_guild(current_guild_id)
#         channel_id = default_channels[guild.id]
#     else:
#         channel_id = default_channels[g_id]
    
#     channel = client.get_channel(channel_id)
#     await channel.send(script.get_msg())
        
if __name__ == '__main__':
    client.run(TOKEN)
