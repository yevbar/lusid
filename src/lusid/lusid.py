from datetime import datetime
from requests import post
from time import sleep

from py_imessage import imessage
import mac_imessage
from imessage_reader import fetch_data

from .mac_db import get_db_path


DB_PATH = get_db_path()
UNREAD_STRING = '2000-12-31 19:00:00'
TODAY = '2024-08-13 22:00:00'

def parse_time(dt):
  return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

def read_messages(time_filter):
  global DB_PATH
  global UNREAD_STRING
  global TODAY

  fd = fetch_data.FetchData(DB_PATH)
  my_data = fd.get_messages()

  current_time = datetime.now()
  return [m for m in my_data if parse_time(m[2]) > time_filter]

def has_messaged_previously_target(to, target):
  all_messages = read_messages(parse_time(TODAY))
  return any(to in message[0] and message[1] == target for message in all_messages)

def has_messaged_previously(to):
  all_messages = read_messages(parse_time(TODAY))
  return any(to in message[0] for message in all_messages)

def send_message(to, content):
  if to != "4158667579" and has_messaged_previously_target(to, "STOP"):
    print("We are not going to send a message because said to stop")
    return # Someone doesn't want to receive messages
  imessage.send(to, content)

def foo():
    print("Hello world")

if __name__ == "__main__":
    foo()
