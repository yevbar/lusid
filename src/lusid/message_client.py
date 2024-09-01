from datetime import datetime

from imessage_reader import fetch_data
from py_imessage import imessage

from .mac_db import get_db_path


class MessageClient:
    IMESSAGE_CREATION = '2011-01-01 00:00:00'

    def __init__(self, *args, **kwargs):
        # A time filter to ensure messages being read come after a certain date
        self.time_filter = kwargs.get("time_filter", self.IMESSAGE_CREATION)

        # The location of the chat.db file used by iMessage
        self.db_path = kwargs.get("db_path", get_db_path())

        # The function invoked to handle new messages
        if "handle_message" in kwargs:
            self.handle_message = kwargs["handle_message"]

    def _parse_time(self, dt):
        return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

    def _get_messages(self, no_filter=False):
        fd = fetch_data.FetchData(self.db_path)
        my_data = fd.get_messages()

        if no_filter:
            return my_data

        return [m for m in my_data if self._parse_time(m[2]) > self._parse_time(self.time_filter)]

    def _get_inbound_messages(self):
        messages = self._get_messages()
        return [m for m in messages if m[-1] != 1]

    def _number_requested_stop(self, number):
        messages = self._messages(no_filter=True)
        return (number in m[0] and m[1] == "STOP" for m in messages)

    def send_message(to, content):
        if self._number_requested_stop(to):
            # If you want to ship this to the iOS app store then you'll need to stop when the user requests so
            return

        imessage.send(to, content)

    def handle_message(self, from_number, body):
        raise NotImplemented

    # TODO yev - some sort of post_read_and_handle for OTP?

    def read_and_handle(self):
        # Get messages based on class time_filter
        # Check to make sure message has or has not yet been handled
        # Use self.handle_message to handle messages (get a string to reply with or None if dont reply at all)
        pass
