import random
from yahoo_fin import stock_info as si

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

def random_food(number):
  foods = []
  with open('foods.txt') as message_text:
    for line in message_text:
      food_places = line.replace("\n", " ").strip()
      foods.append(food_places)
  if(number) > 1:
    return ', '.join(random.sample(foods,number))
  else:
    return random.choice(foods)

def check_gme():
  print('GME stock check')
  return si.get_live_price("gme")

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

def balance(users, option):
  balanced_team = shuffle_balance(users)
  result = '**Team One:**\n'
  for player in balanced_team[0]:
      result += player + '\n'
  result += '\n**Team Two:**\n'
  for player in balanced_team[1]:
      result += player + '\n'
  return result