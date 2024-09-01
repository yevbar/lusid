from .message_client import MessageClient


def read_messages(since_time=None, inbound_only=True):
    mc = MessageClient(
        time_filter=since_time
    )

    if inbound_only:
        return mc._get_inbound_messages()

    return mc._get_messages()
