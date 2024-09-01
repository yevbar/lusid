from .message_client import MessageClient


def send_message(to, body, ignore_stop=False):
    mc = MessageClient()
    mc.send_message(to, body, ignore_stop)
