from .message_client import MessageClient


def send_message(to, body):
    mc = MessageClient()
    mc.send_message(to, body) # Sending from client since it checks for STOP message
