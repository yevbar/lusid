import os


def get_db_path():
    """
    Returns path to the chat.db file iMessage uses under the hood
    """
    return os.expanduser("~") + "/Library/Messages/chat.db"
