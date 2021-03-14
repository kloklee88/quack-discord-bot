import random
import replit_db_crud
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

def check_gme_borrow():
  try:
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    print('Getting driver...')
    driver = None
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://iborrowdesk.com/report/GME")
    fee = driver.find_element_by_xpath('/html/body/div/div/div[1]/div/div[2]/div[5]/div/table/tbody/tr[1]/td[1]').text
    available = driver.find_element_by_xpath('/html/body/div/div/div[1]/div/div[2]/div[5]/div/table/tbody/tr[1]/td[2]').text
    updated = driver.find_element_by_xpath('/html/body/div/div/div[1]/div/div[2]/div[5]/div/table/tbody/tr[1]/td[3]').text
    replit_db_crud.save_alert_enabled('borrow_latest', updated)
    data = [fee, available, updated]
  finally:
    if driver is not None:
       driver.quit()
  return data

def save_alert_enabled(alert,is_enabled):
  replit_db_crud.save_alert_enabled(alert,is_enabled)

def shouldisellgme():
  stock_value = si.get_live_price("gme")
  if stock_value > 500:
    return 'yes'
  elif stock_value > 400:
    return 'probably'
  elif stock_value > 300:
    return 'maybe'
  else:
    return 'no'

def check_stock(stock):
  print(stock)
  try:
    stock_value = '{:.2f}'.format(si.get_live_price(stock))
    return f'{stock.upper()} live price (not after hours): {stock_value}'
  except:
    return f'{stock.upper()} symbol could not be found'

def check_gme():
  stock_value = '{:.2f}'.format(si.get_live_price("gme"))
  return f':rocket: GME :rocket: -- {stock_value}'

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

##JORGE Services
def get_jorge_help():
  f = open('jorge.txt')
  help = f.readlines()
  return ''.join(help)

def get_jorge_website():
  return 'https://jorgecapital.tk'