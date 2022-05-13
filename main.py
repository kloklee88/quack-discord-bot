import discord
import os
import quack_service
from keep_alive import keep_alive

#Flask Server to keep repl.it alive
keep_alive()

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  activity = discord.Game(name="!quack help")
  await client.change_presence(activity=activity)
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
      return

  #Process message commands
  full_command = message.content.strip().split(' ')

  if message.content.startswith('!quack') or message.content.startswith('!quak'):
    print(full_command)
    if len(full_command) == 2:
      first_command = full_command[1]
      if first_command.startswith('<@!'):
        await message.channel.send(quack_service.get_personalized_message(message.mentions[0]))
      elif first_command == 'about':
        await message.channel.send(about())
      elif first_command == 'help':
        await message.channel.send(quack_service.get_help())
      elif first_command == 'quack':
        await message.channel.send(quack_service.print_quack(2))
    elif len(full_command) >= 3:
      all_quack = quack_service.check_all_quack(full_command)
      if all_quack == True:
        await message.channel.send(quack_service.print_quack(len(full_command)))
    else:
      await message.channel.send(quack_service.print_quack(1))

  if message.content.startswith('!food'):
    print(full_command)
    if len(full_command) == 2:
      first_command = full_command[1]
      try:
        number = int(first_command)
        await message.channel.send(quack_service.random_food(number))
      except:
        await message.channel.send('Invalid command')
    else:
      await message.channel.send(quack_service.random_food(1))

  # if message.content.startswith('!stock'):
  #   if len(full_command) == 2:
  #     first_command = full_command[1]
  #     await message.channel.send(quack_service.check_stock(first_command))

  # if message.content.startswith('!gme'):
  #   print(full_command)
  #   await message.channel.send(quack_service.check_gme())

  if message.content.startswith('!whiskey'):
    await message.channel.send(quack_service.get_whiskey())

  if message.content.startswith('!inhouse'):
    print(full_command)
    if len(full_command) > 2:
      first_command = full_command[1]
      if first_command.startswith('<@!'):
        print(len(message.mentions))
        if len(message.mentions) != 10:
          await message.channel.send("Inhouse feature requires exactly 10 players")
        else:
          await message.channel.send(quack_service.balance(message.mentions, None))
      if first_command.startswith('lookup'):
        if len(message.mentions) != 1:
          await message.channel.send("Inhouse lookup feature requires only 1 mention")
        else:
          await message.channel.send(quack_service.lookup(message.mentions))
    else:
      await message.channel.send(', '.join(quack_service.get_all_players()))

  if message.content.startswith('!alert'):
    print(full_command)
    if len(full_command) == 3:
      first_command = full_command[1]
      second_command = full_command[2]
      if first_command == 'gme' and (second_command == 'True' or second_command == 'False'):
        quack_service.save_alert_enabled('gme', eval(second_command))
        await message.channel.send("Alert for GME updated")

  if message.content.startswith('!slime'):
    await message.channel.send(quack_service.slime())

  if message.content.startswith('!randomizer'):
    if len(full_command) == 2:
      first_command = full_command[1]
      await message.channel.send(quack_service.random_item(first_command))
    else: 
      await message.channel.send('Please add a list of values separated by commas. Ex: heads,tails,gordon,jorge')

  if message.content.startswith('!jorge'):
    if len(full_command) == 2:
      first_command = full_command[1]
      if first_command.startswith('genshin'):
        result = ''
        guild = client.get_guild(int(os.getenv('GUILD')))
        jorge = guild.get_member(int(os.getenv('JORGE')))
        print(jorge.activity)
        if 'Genshin Impact' in str(jorge.activity):
          result = 'of course he is'
        else:
          result = 'no'
        await message.channel.send(result)
      elif first_command.startswith('site'):
        await message.channel.send(quack_service.get_jorge_site())
      elif first_command.startswith('rocks'):
        await message.channel.send(quack_service.get_jorge_rocks())
    else:
      await message.channel.send(quack_service.get_jorge_help())

  if message.content.startswith('garbage bot') or message.content.startswith('trash bot') or message.content.startswith('quack bot sucks'):
    await message.channel.send("Well, why don't you do it yourself, you lazy ass useless human! :angry:")

def about():
  return "A dedicated Discord bot for He's a Quack! server for everything, anything, and nothing :smile:"

client.run(os.getenv('TOKEN'))