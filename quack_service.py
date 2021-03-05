import random

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