from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'iauar'

@app.route('/api/ping')
def ping():
    return {"message": "pong"}


if __name__ == '__main__':
    app.run()