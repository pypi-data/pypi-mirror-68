# Thr
A small Threema Gateway library that focuses on easy usage.

![Python package](https://github.com/coffeemakr/python-thr/workflows/Python%20package/badge.svg)

## Functionality

 - [x] Send text messages
 - [x] Send files
 - [x] Lookup contacts
 - [ ] Receive messages

## Usage
First, initialize the API without own API secrets.
```py
threema = thr.Threema(
    identity="*MYIDENT", 
    key='717b1fb0f3e6888454f21a012cec6be6181a308ce89f4a733869848fd6ed74bb', 
    secret='w2kdj25yh1Ep81oP')
```

### Lookup Contacts
In order to send end-to-end encrypted messages, you need the public key of the recipient. If you don't have it you can look-up the public key using the threema ID:
```py
contact = threema.lookup("FMD1R5RX")
```

### Send a Text Message
There is a shorthand function to send text messages:
```py
threema.send_text_message(recipient=contact, content="Hello!")
```

The more verbose way would be to first, create a TextMessage and afterwards send it:
```py
message = TextMessage("Hello!")
threema.send_message(recipient=contact, message=message)
```

### Send a File
If you want to send a file with a thumbnail attached, you have to upload the thumbnail as well.
The key must be the same, as the one for the file.

```py
# Upload the file
message = threema.upload_file(filename="image.jpg")

# Optionally upload a thumbnail
with open("thumbnail.jpg", "rb") as thumnail_file:
    thumbnail_content = thumnail_file.read()
message.thumbnail_blob_id = threema.upload_thumbnail(thumbnail_content, key=message.key)

# Send the message
threema.send_message(
    message=message, 
    recipient=contact)
```
