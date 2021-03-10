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
  full_command = message.content.strip().split(' ')
  if message.content.startswith('!stock'):
    if len(full_command) == 2:
      first_command = full_command[1]
      await message.channel.send(check_stock(first_command))

  if message.content.startswith('!quack') or message.content.startswith('!quak'):
    print(full_command)
    if len(full_command) == 2:
      first_command = full_command[1]
      if first_command.startswith('<@!'):
        await message.channel.send(personalized_message(message.mentions[0]))
      elif first_command == 'about':
        await message.channel.send(about())
      elif first_command == 'help':
        await message.channel.send(help())
      elif first_command == 'quack':
        await message.channel.send(quack(2))
    elif len(full_command) >= 3:
      all_quack = check_all_quack(full_command)
      if all_quack == True:
        await message.channel.send(quack(len(full_command)))
    else:
      await message.channel.send(quack(1))

  if message.content.startswith('!food'):
    print(full_command)
    if len(full_command) == 2:
      first_command = full_command[1]
      try:
        number = int(first_command)
        await message.channel.send(food(number))
      except:
        await message.channel.send('Invalid command')
    else:
      await message.channel.send(food(1))

  if message.content.startswith('!gme'):
    print(full_command)
    await message.channel.send(gme())

  if message.content.startswith('!inhouse'):
    print(full_command)
    if len(full_command) > 2:
      first_command = full_command[1]
      if first_command.startswith('<@!'):
        print(len(message.mentions))
        if len(message.mentions) != 10:
          await message.channel.send("Inhouse feature requires exactly 10 players")
        else:
          await message.channel.send(inhouse(message.mentions, None))
    else:
      await message.channel.send(available_players())

  if message.content.startswith('garbage bot') or message.content.startswith('trash bot'):
    await message.channel.send("Well, why don't you do it yourself, you lazy ass useless human! :angry:")

def inhouse(mentions, option):
  return quack_service.balance(mentions, option)

def personalized_message(mentions):
  return quack_service.get_personalized_message(mentions)

def about():
  return "A dedicated Discord bot for He's a Quack! server for everything, anything, and nothing :smile:"

def help():
  return 'Commands:\n**!quack about** -- bot description\n**!quack @mention** -- where @mention is anybody in the server to receive a random customized message (maybe). People may have more than one message too. Keep using this command to find all of your messages.\n**!quack quack quack...** -- quacks?\n**!gme** -- checks if we are going to the moon\n**!stock symbol** -- checks stock price with the symbol provided\n**!food #** -- randomnly suggests # (optional value, default is 1) food places to eat\n**!inhouse** -- view all the available players in the system with a MMR\n**!inhouse @mentions** -- where @mentions are all 10 players participating in the inhouse. This will balance players accordingly into two balanced team using MMR (this functionality is currently in progress)'

def check_all_quack(full_command):
  print('Checking quacks')
  all_quack = True
  for command in full_command:
    if 'quack' not in command.lower():
      all_quack = False
  return all_quack

def food(number):
  return quack_service.random_food(number)

def quack(number):
  return quack_service.print_quack(number)

def gme():
  return quack_service.check_gme()

def check_stock(stock):
  return quack_service.check_stock(stock)

def available_players():
  return ', '.join(quack_service.get_all_players())

client.run(os.getenv('TOKEN'))