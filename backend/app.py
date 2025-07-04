from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
CORS(app)
jwt = JWTManager(app)

from auth import *
from funcs import *

if __name__ == '__main__':
    app.run()
