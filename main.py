from flask import Flask, render_template, request
import os
import jwt
import datetime
from dotenv import load_dotenv 
import requests

load_dotenv()
app = Flask(__name__)

# @app.route("/")
# def home():
# 	return render_template('signIn.html')

@app.route("/about")
def about():
	return "HELLO and WELCOME"

@app.route("/")
def generate_secret_key():

        with open(os.environ.get('SOCIAL_AUTH_APPLE_PRIVATE_KEY'), "r") as f:
            private_key = f.read()

        team_id = os.environ.get('team_id')
        client_id = os.environ.get('client_id')
        key_id = os.environ.get('key_id')

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
        # return secret_key

        # client_secret_key = generate_secret_key()
        print('client_secret_key', secret_key)

        auth_request = {
            "client_id": "com.abla.captcha",
            "redirect_uri": "https://tableau.abla.io/signin",
            "response_type": "code",
            "scope": "name email",
            "state": "12345",
            "response_mode": "form_post",
            "nonce": "67890",
            "client_secret": secret_key # Convertir le client_secret en chaîne de caractères pour l'utiliser dans la demande
        }

        response = requests.get("https://appleid.apple.com/auth/authorize", params=auth_request)
        print('response', response)

        return render_template('signIn.html')





if __name__ == '__main__':
      app.run(debug=True)

