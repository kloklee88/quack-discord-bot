import discord
import os
import quack_service
from keep_alive import keep_alive

#Flask Server to keep repl.it alive
keep_alive()

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
      return

  #Process message commands
  if message.content.startswith('!quack'):
    full_command = message.content.strip().split(' ')
    if len(full_command) == 2:
      first_command = full_command[1]
      if first_command.startswith('<@!'):
        await message.channel.send(personalized_message(message))
      elif first_command == 'about':
        await message.channel.send(about(message))
      elif first_command == 'help':
        await message.channel.send(help(message))
    else:
      await message.channel.send(help(message))

def personalized_message(message):
  return quack_service.get_personalized_message(message.mentions[0])

def about(message):
  return "A dedicated Discord bot for He's a Quack! server, for everything, anything, and nothing :smile:"

def help(message):
  return 'Commands:\n**!quack about** -- bot description\n**!quack @mention** -- where @mention is anybody in the server to receive a customized message (maybe)'

client.run(os.getenv('TOKEN'))