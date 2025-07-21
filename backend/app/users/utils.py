from flask import current_app as app
import requests

def verify_recaptcha(token):
    secret_key = app.config['RECAPTCHA_SECRET_KEY']
    url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {'secret': secret_key, 'response': token}
    response = requests.post(url, data=payload)
    result = response.json()

    return result.get('success', False)
