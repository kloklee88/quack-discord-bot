import random
import binpacking
import tabulate
from player import Player

def get_personalized_message(user):
  all_user_messages = []
  with open('personalized_message.txt') as message_text:
    for line in message_text:
      user_message = line.replace("\n", " ").strip()
      username = user_message.split(';')[0]
      message = user_message.split(';')[1]
      if username in user.name:
        all_user_messages.append(message)
  print(all_user_messages)
  if not all_user_messages:
    return ':smiley:'
  return random.choice(all_user_messages)

def check_all_quack(full_command):
  print('Checking quacks')
  all_quack = True
  for command in full_command:
    if 'quack' not in command.lower():
      all_quack = False
  return all_quack

def print_quack(number):
  result = 'Quack'
  if number >= 2:
    i = 1
    while number > i:
      if i > 10:
        break
      result += ' quack'
      i += 1
  result += '!'
  return result

def random_item(user_list):
  items = user_list.split(',')
  return random.choice(items)

def random_food(number):
  foods = []
  with open('foods.txt') as message_text:
    for line in message_text:
      food_places = line.replace("\n", " ").strip()
      foods.append(food_places)
  if number > len(foods):
    return ', '.join(random.sample(foods,len(foods)-1))
  elif number > 1:
    return ', '.join(random.sample(foods,number))
  else:
    return random.choice(foods)

def slime():
  slimes = []
  with open('slimes.txt') as message_text:
    for line in message_text:
      slime = line.replace("\n", " ").strip()
      slimes.append(slime)
  return random.choice(slimes)

# def check_stock(stock):
#   print(stock)
#   try:
#     stock = yf.Ticker(stock)
#     stock_value = stock.info['regularMarketPrice']
#     return f'{stock.upper()} live price (not after hours): {stock_value}'
#   except:
#     return f'{stock.upper()} symbol could not be found'

# def check_gme():
#   stock = yf.Ticker("GME")
#   stock_value = stock.info['regularMarketPrice']
#   return f':rocket: GME :rocket: -- {stock_value}'

def get_all_players():
  players = []
  with open('players.txt') as message_text:
    for line in message_text:
      player_info = line.replace("\n", " ").strip()
      username = player_info.split(';')[0]
      #mmr = player_info.split(';')[1]
      players.append(username)
  print(players)
  return players

def get_help():
  f = open('help.txt')
  help = f.readlines()
  return ''.join(help)

def get_whiskey():
  f = open('whiskey.txt')
  help = f.readlines()
  return ''.join(help)

##Inhouse functions
def lookup(player):
  target = Player(player)
  target.getPrimaryRole()
  if not target.exists:
    player_lookup = f'Summoner does not exist.'
  else:
    player_lookup = \
    f'Summoner name: {player}\n\
    Rank: {target.rank} {target.division} {target.lp}LP\n\
    Primary Role: {target.role}\n\
    Win Rate: {int(target.winrate*100)}%\n\
                      '
  return player_lookup
  
  
  
  # player_lookup = None
  # with open('players.txt') as message_text:
  #   for line in message_text:
  #     player_info = line.replace("\n", " ").strip()
  #     username = player_info.split(';')[0]
  #     mmr = player_info.split(';')[1]
  #     if player[0].name == username:
  #       player_lookup = f'{username} - {mmr}'
  # if player_lookup == None:
  #   return f'{player[0].name} was not found'
  # return player_lookup
    
  
def shuffle_balance(users):
  print("Shuffling")
  players = []
  for user in users:
    players.append(user.name)
  print(players)
  random.shuffle(players)
  team_one = players[0:5]
  team_two = players[5:10]
  team_one.sort()
  team_two.sort()
  balanced_team = [team_one, team_two]
  return balanced_team

def get_winrate(player):
  target = Player(player)
  if target is None:
    winrate = .5 #TODO: temporary just set to a 50% winrate
  else:
    winrate = target.winrate
  return winrate

def balance(users, option):
  players = {}
  for user in users:
      players[user] = get_winrate(user)
  balanced_team = binpacking.to_constant_bin_number(players,2)
  team_one_sum = 0
  team_two_sum = 0
  table_one = []
  table_two = []
  result = '**Team One:**\n'
  for player, mmr in balanced_team[0].items():
      mmr = mmr*100
      table_one.append([player,round(mmr,2)])
      team_one_sum += mmr
  result += tabulate(table_one)
  result += '\n**Team Two:**\n'
  for player, mmr in balanced_team[1].items():
      mmr = mmr*100
      table_two.append([player,round(mmr,2)])
      team_two_sum += mmr
  result += tabulate(table_two)
  difference = round(abs(team_one_sum-team_two_sum),2)
  result += f'\n**Team Difference**: {difference}%'
  return result

##JORGE Services
def get_jorge_help():
  f = open('jorge.txt')
  help = f.readlines()
  return ''.join(help)

def get_jorge_site():
  return 'https://jorgecapital.tk'

def get_jorge_rocks():
  return 'https://clips.twitch.tv/OptimisticInventiveHabaneroResidentSleeper'