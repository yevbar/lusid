# Lusid

Automate iMessage with Python. If you have the following:

* Macbook
* Python

You can programatically control iMessage with a self-hosted solution, here's how:

## Installing

Use pip or whichever python package manager you're working with

```bash
$ pip install lusid
```

**Author note:** The below will not just change behavior to unlock iMessage  but also affect [a system-level functionality](https://support.apple.com/en-us/102149). Do not set this up if you're working on a computer that tends to install sketchy software from safe-for-work websites

You'll need to allow your Terminal application (or whichever terminal emulator you're running) to have full disk access in order to view the `chat.db` file containing your iMessages as well as "Accessibility" permissions via the Security & Privacy settings on your Mac

Additionally, you'll need to disable certain permissions

```bash
$ csrutil disable
```

If running `csrutil disable` doesn't work, try this [stackoverflow post](https://apple.stackexchange.com/questions/208478/how-do-i-disable-system-integrity-protection-sip-aka-rootless-on-macos-os-x)

## Quickstart (sending messages)

If you're just interested in sending a message, import the `send_message` function and voila

```python
from lusid import send_message

to = "123-456-7890"
body = "Yeehaw"

send_message(to, body)
```

## Quickstart (reading messages)

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

## Basic example

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

## Complex example

Suppose you wanted to be able to share cat facts with a specific friend while also having message interaction, here's how you can accomplish that. We'll be adding to the **Basic example** above

For this particular example we'll be using the python package `requests` to make a simple API request

```bash
$ pip install requests
```

In short, like how React components have lifecycle methods, the message client features a `handle_post_read` method that can be specified at instantiation. 

```diff
# app.py

+import random
from requests import get
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

## Shameless plug

Think this is cool? Check out what we're actually building @ [https://lsd.so](https://lsd.so)
