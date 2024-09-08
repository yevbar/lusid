# Lusid

Self-hosted Python interface for iMessage (similar to Twilio) that supports both green and blue bubbles. 

Think this is cool? Check out what we're building at [lsd.so](https://lsd.so)

**Important:** Before use, please ensure you are compliant with telecommunications laws in your area and in some cases your recipient's area, including quiet hours, express consent, and other spam prevention laws. Lusid includes support, by default, for users to opt out by texting 'STOP', which is required in many countries including the US.

## Requirements

* Mac running macOS 10.11 or later
* Python
* iPhone with SIM (optional, adds SMS/green bubble support)

## Installing

Use pip or whichever python package manager you're working with

```bash
$ pip install lusid
```

You'll need to allow your Terminal application (or whichever terminal emulator you're running) to have full disk access in order to view the `chat.db` file containing your iMessages as well as "Accessibility" permissions via the Security & Privacy settings on your Mac.

Additionally, you'll need to disable System Integrity Protection on your Mac by running this terminal command in recovery mode:

```bash
$ csrutil disable
```

**Please note:** System Integrity Protection prevents malware from accessing and altering system-level files, and disabling leaves your computer vulnerable to malicious code. We recommend going through the below article and ensuring you understand the risks before disabling.

For additional information on how to disable System Integrity Protection, the risks associated, and how to re-enable it, refer to this [Apple Developer Article](https://developer.apple.com/documentation/security/disabling-and-enabling-system-integrity-protection).

## Quickstart

### Sending Messages

If you're just interested in sending a message, import the `send_message` function and voila

```python
from lusid import send_message

to = "123-456-7890"
body = "Yeehaw"

send_message(to, body)
```

### Reading Messages

If you're just interested in getting iMessage data

```python
from lusid import read_messages

print(read_messages())
```

If you're interested in not only received but all messages and only ones that were sent in the past 24 hours

```python
from datetime import datetime, timedelta

from lusid import read_messages

print(read_messages(
  since_time=datetime.now() + timedelta(days=-1),
  inbound_only=False,
))
```

### SMS Support

If you're interested in supporting SMS (green bubbles), follow these steps:

* Ensure your iPhone has an active SIM card and is updated to the latest iOS software.
* In Settings > Apple ID, sign into the same Apple ID used on your Mac running Lusid.
* In Settings > Apps > Messages > Text Message Forwarding, enable the Mac running Lusid.

SMS/MMS messages can now be sent by running Lusid normally, provided both your Mac and iPhone are powered on and connected to the internet. To ensure best performance, keep both devices connected to the same network.

## Example Usage

### Basic

If you're interested in something replying to received messages

1. Create a "client" to repeatedly read your inbox (the rest of this quickstart assumes you're writing to a file named `app.py` but feel free to replace that later on with whatever you named your to)

```python
# app.py

from lusid import create_simple_message_client

def start_client():
  create_simple_message_client(
    message_handler=lambda to, body: None,
  )

if __name__ == "__main__":
  start_client()
```

2. Define a function for handling messages:

```python
# Snippet

def handle_message(from_number, body):
  print(f"Handling the message [{body}] from [{from_number}]")
  return "Some funny autoreply here" # Or None to not reply at all
```

3. Next we're going to include the function we defined earlier

```diff
# app.py

from lusid import create_simple_message_client

+def handle_message(from_number, body):
+  print(f"Handling the message [{body}] from [{from_number}]")
+  return "Some funny autoreply here" # Or None to not reply at all

def start_client():
  create_simple_message_client(
    message_handler=lambda to, body: None,
  )

if __name__ == "__main__":
  start_client()
```

Then actually use it as our message handler

```diff
# app.py

from lusid import create_simple_message_client

def handle_message(from_number, body):
  print(f"Handling the message [{body}] from [{from_number}]")
  return "Some funny autoreply here" # Or None to not reply at all

def start_client():
  create_simple_message_client(
-    message_handler=lambda to, body: None,
+    message_handler=handle_message
  )

if __name__ == "__main__":
  start_client()
```

If you'd like to just copy/paste the resulting code

```python
# app.py

from lusid import create_simple_message_client

def handle_message(from_number, body):
  print(f"Handling the message [{body}] from [{from_number}]")
  return "Some funny autoreply here" # Or None to not reply at all

def start_client():
  create_simple_message_client(
    message_handler=handle_message
  )

if __name__ == "__main__":
  start_client()
```

4. Now your script is set up to automatically reply to every received message with "Some funny autoreply here"

```bash
$ python app.py
Handling the message [Hello word!] from [+11234567890]
```

### Complex

Suppose you wanted to be able to share cat facts with a specific friend while also having message interaction, here's how you can accomplish that. We'll be adding to the **Basic example** above

For this particular example we'll be using the python package `requests` to make a simple API request

```bash
$ pip install requests
```

In short, like how React components have lifecycle methods, the message client features a `handle_post_read` method that can be specified at instantiation. 

```diff
# app.py

+import random
+from requests import get
from lusid import create_simple_message_client

def handle_message(from_number, body):
  print(f"Handling the message [{body}] from [{from_number}]")
  return "Some funny autoreply here" # Or None to not reply at all

+def handle_post_read(cls):
+  facts = get("https://cat-fact.herokuapp.com/facts").json()
+  fact = random.choice(facts)["text"]
+
+  print(f"Telling kevin that {fact}")
+
+  kevin = "123-456-7890"
+  cls.send_message(kevin, fact)

def start_client():
  create_simple_message_client(
    message_handler=handle_message,
+    handle_post_read=handle_post_read
  )

if __name__ == "__main__":
  start_client()
```

Or, if you'd like to just copy and paste

```python
# app.py

import random
from requests import get
from lusid import create_simple_message_client

def handle_message(from_number, body):
  print(f"Handling the message [{body}] from [{from_number}]")
  return "Some funny autoreply here" # Or None to not reply at all

def handle_post_read(cls):
  facts = get("https://cat-fact.herokuapp.com/facts").json()
  fact = random.choice(facts)["text"]

  print(f"Telling kevin that {fact}")

  kevin = "123-456-7890"
  cls.send_message(kevin, fact)

def start_client():
  create_simple_message_client(
    message_handler=handle_message,
    handle_post_read=handle_post_read
  )

if __name__ == "__main__":
  start_client()
```

**And here's what it looks like when run**

```bash
$ python app.py
Telling kevin that Cats are the most popular pet in the United States: There are 88 million pet cats and 74 million dogs.
Telling kevin that Most cats are lactose intolerant, and milk can cause painful stomach cramps and diarrhea. It's best to forego the milk and just give your cat the standard: clean, cool drinking water.
Telling kevin that Owning a cat can reduce the risk of stroke and heart attack by a third.
```
