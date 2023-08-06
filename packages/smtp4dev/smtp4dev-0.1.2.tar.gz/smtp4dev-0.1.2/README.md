# SMTP4DEV

An abstraction library to access the messages captured by an
[SMTP4dev](https://github.com/rnwood/smtp4dev/) instance.


## Installation

Install with pip:

```
pip install smtp4dev
```

## Usage

Example usage:

```py
from smtp4dev import Smtp4Dev
client = Smtp4Dev('http://localhost:8080')
messages = client.list_messages()
email = client.get_message(next(messages))
print(email)
"[From: romeo@email.com To: juliet@email.com Subject: Meeting Friday night]"
```
