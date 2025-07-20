from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from authlib.integrations.flask_client import OAuth
#from redis import Redis # uncomment for deploy
#import os # uncomment for deploy

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
    #storage_uri=os.getenv("REDIS_URL", "memory://") # uncomment for deploy
    )
mail = Mail()
oauth = OAuth()
