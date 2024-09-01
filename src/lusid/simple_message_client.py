from datetime import datetime
from time import sleep

from .message_client import MessageClient


def create_simple_message_client(message_handler, interval=1):
    time_of_run = datetime.now()
    
    mc = MessageClient(
        handle_message=message_handler,
        time_filter=time_of_run,
    )

    while True:
        sleep(interval)

        try:
            mc.read_and_handle()
        except Exception as e: # Very failure tolerant
            print("Exception!")
            print(e)
