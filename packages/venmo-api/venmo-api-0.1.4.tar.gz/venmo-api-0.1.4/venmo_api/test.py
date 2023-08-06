from venmo_api import Client


token = "Bearer bb4c6b17581cf6b53faf103afd311ada3e383ca4a61faaace64cb54033b07ea7"

# TODO: This is mark mohades token dude careful
token = "3c2d0adc59b9c771ba45e09bc784ad95a0dba05e9bd16c42c9e95a996cb45233"
client = Client(token)
user = client.user.get_my_profile()
print(user)
trans = client.user.get_user_transactions(user_id=user.id)
print(trans)
