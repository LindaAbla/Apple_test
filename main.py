from flask import Flask, render_template, request
import os
import jwt
import datetime
from dotenv import load_dotenv 
import requests

load_dotenv()
app = Flask(__name__)

@app.route("/about")
def about():
    return "HELLO and WELCOME"

@app.route("/")
def generate_secret_key():
    f="https://apple-sign-bucket.s3.fr-par.scw.cloud/AuthKey_WR7AQBJ53M.p8"
    private_key = requests.get(f).content

    team_id = 'GDY52HN4HA'
    client_id = 'com.abla.captcha'
    key_id = 'WR7AQBJ53M'

    timestamp_now = datetime.datetime.now().timestamp()
    timestamp_exp = timestamp_now + (86400 * 180) # 6 months

    headers={"kid": str(key_id)}
    data = {
            "iss": team_id,
            "iat": timestamp_now,
            "exp": timestamp_exp,
            "aud": "https://appleid.apple.com",
            "sub": client_id
        }

    secret_key = jwt.encode(payload=data, key=private_key, algorithm="ES256", headers=headers)

    auth_request = {
        "client_id": "com.abla.captcha",
        "redirect_uri": "https://captcha-apple.vercel.app/about",
        "response_type": "code",
        "scope": "name email",
        "state": "12345",
        "response_mode": "form_post",
        "nonce": "67890",
        "client_secret": secret_key # la clé secrète est déjà une chaîne de caractères
    }

    response = requests.get("https://appleid.apple.com/auth/authorize", params=auth_request)
    print('response', response)

    return render_template('signIn.html')


if __name__ == '__main__':
    app.run(debug=True)
