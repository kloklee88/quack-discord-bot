import discord
import os
import quack_service
import aiocron
import replit_db_crud 
from keep_alive import keep_alive

#Flask Server to keep repl.it alive
keep_alive()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

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

  if message.content.startswith('!alert'):
    print(full_command)
    if len(full_command) == 3:
      first_command = full_command[1]
      second_command = full_command[2]
      if first_command == 'gme' and (second_command == 'True' or second_command == 'False'):
        save_alert_enabled('gme', eval(second_command))
        await message.channel.send("Alert for GME updated")

  if message.content.startswith('!shouldisellgme'):
    await message.channel.send(shouldisellgme())

  if message.content.startswith('!jorgegenshin'):
    result = ''
    guild = client.get_guild(int(os.getenv('GUILD')))
    jorge = guild.get_member(int(os.getenv('JORGE')))
    print(jorge.activity)
    if jorge.activity == 'Genshin Impact':
      result = 'yes'
    else:
      result = 'no'
    await message.channel.send(result)

  if message.content.startswith('garbage bot') or message.content.startswith('trash bot'):
    await message.channel.send("Well, why don't you do it yourself, you lazy ass useless human! :angry:")

#@aiocron.crontab('*/2 * * * *')
#@aiocron.crontab('* * * * *')
async def gme_short_alert():
  print('Checking GME borrow')
  data = quack_service.check_gme_borrow()
  borrow_info = f'Fee ({data[0]}) | Available ({data[1]}) | Updated ({data[2]})'
  channel = discord.utils.get(client.get_all_channels(), guild__name='Confucius Private', name='misc')
  jorge = await client.fetch_user(int(os.getenv('JORGE')))
  #print(jorge)
  is_alert_enabled = replit_db_crud.get_alert_enabled("gme")
  borrow_latest = replit_db_crud.get_alert_enabled("borrow_latest")
  print(f'Last: {borrow_latest} vs Recent: {data[2]}')
  print(f'Alert enabled: {is_alert_enabled}')
  if is_alert_enabled and borrow_latest != data[2]:
    await channel.send(borrow_info)
    await jorge.send(borrow_info)

def inhouse(mentions, option):
  return quack_service.balance(mentions, option)

def personalized_message(mentions):
  return quack_service.get_personalized_message(mentions)

def about():
  return "A dedicated Discord bot for He's a Quack! server for everything, anything, and nothing :smile:"

def shouldisellgme():
  return quack_service.shouldisellgme()

def help():
  return quack_service.get_help()

def check_all_quack(full_command):
  print('Checking quacks')
  all_quack = True
  for command in full_command:
    if 'quack' not in command.lower():
      all_quack = False
  return all_quack

def save_alert_enabled(alert,is_enabled):
  return quack_service.save_alert_enabled(alert,is_enabled)

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