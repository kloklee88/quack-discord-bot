from replit import db

def get_personalized_message(username):
  messages = db[username]
  messages = messages.split(';')
  return messages

def save_personalized_message(username,message):
  db[username] = message

def save_alert_enabled(alert,is_enabled):
  db[alert] = is_enabled

def get_alert_enabled(alert):
  is_enabled = db[alert]
  return is_enabled
