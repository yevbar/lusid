# Lusid

If you have the following:

* Macbook
* Python

You can programatically control iMessage, here's how

## Installing

Use pip or whichever python package manager you're working with

```bash
$ pip install lusid
```

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

In short, like how React components have lifecycle methods, the message client features a `handle_post_read` method that can be specified at instantiation

```diff
# app.py

from requests import get
from lusid import create_simple_message_client

def handle_message(from_number, body):
  print(f"Handling the message [{body}] from [{from_number}]")
  return "Some funny autoreply here" # Or None to not reply at all

+def handle_post_read(cls):
+  facts = get("https://cat-fact.herokuapp.com/facts").json()
+  fact = facts[0]["text"]
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

from requests import get
from lusid import create_simple_message_client

def handle_message(from_number, body):
  print(f"Handling the message [{body}] from [{from_number}]")
  return "Some funny autoreply here" # Or None to not reply at all

def handle_post_read(cls):
  facts = get("https://cat-fact.herokuapp.com/facts").json()
  fact = facts[0]["text"]

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
