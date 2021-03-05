from replit import db

def get_personalized_message(username):
  messages = db[username]
  messages = messages.split(';')
  return messages

def save_personalized_message(username,message):
  db[username] = message