# requires pyjwt (https://pyjwt.readthedocs.io/en/latest/)
# pip install pyjwt


import datetime
import jwt
from secrets import apple_key_ID, apple_team_ID, apple_private_key


alg = 'ES256'

time_now = datetime.datetime.now()
time_expired = datetime.datetime.now() + datetime.timedelta(hours=12)

headers = {
    "alg": alg,
    "kid": apple_key_ID
}

payload = {
    "iss": apple_team_ID,
    "exp": int(time_expired.strftime("%S")),
    "iat": int(time_now.strftime("%S"))
}


if __name__ == "__main__":
    """Create an auth token"""
    token = jwt.encode(payload, apple_private_key,
                       algorithm=alg, headers=headers)

    print("----TOKEN----")
    print(token)

    print("----CURL----")
    print("curl -v -H 'Authorization: Bearer %s' \"https://api.music.apple.com/v1/catalog/us/artists/36954\" " % (token))
