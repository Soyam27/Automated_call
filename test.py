
import os
from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

call = client.calls.create(
    url="https://zenobia-sublunated-eighthly.ngrok-free.dev/voice",
    to="+918585056098",
    from_="+12186169902",
)

print("Call Initiated!")