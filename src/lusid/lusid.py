from datetime import datetime
from requests import post
from time import sleep

from .py_imessage import imessage
from .mac_imessage import * as mac_message
from .imessage_reader import fetch_data

from .mac_db import get_db_path

def foo():
    print("Hello world")

if __name__ == "__main__":
    foo()
