import os


def get_db_path():
    """
    Returns path to the chat.db file iMessage uses under the hood
    """
    return os.path.expanduser("~") + "/Library/Messages/chat.db"
