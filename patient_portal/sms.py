# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


account_sid = "ACc319ba45a57855df8b48288ff7f8bf55"
auth_token = "26f308193c3bfd9ffe5ce4459e0b7965"

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+254718908494',
                     to='+15558675310'
                 )

print(message.sid)
