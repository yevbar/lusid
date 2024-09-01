import os
from pathlib import Path


def get_db_path():
    """
    Returns path to the chat.db file iMessage uses under the hood
    """
    cwd = Path(os.getcwd()).parts # https://stackoverflow.com/a/38741379

    # Attempt to get /Users/<username>/Library/Messages/chat.db from current working directory
    while len(cwd) > 1:
        if cwd[-2] == "Users":
            return "/" + "/".join(list(cwd[:len(cwd) - 1]) + ["Library", "Messages", "chat.db"])
        cwd = list(cwd[:len(cwd) - 1])

    # Attempt to get /Users/<username>/Library/Messages/chat.db by looking through /Users/ directory
    for user_directory in next(os.walk('/Users/'))[1]:
        possible_path = os.path.join("Users", user_directory, "Library", "Messages", "chat.db")
        if os.path.exists(possible_path):
            return possible_path

    # Otherwise assume the user is running as non-root
    return os.expanduser("~") + "/Library/Messages/chat.db"
