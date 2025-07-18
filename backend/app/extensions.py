from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
#from redis import Redis # descomentar essa linha no Deploy
#import os # descomentar essa linha no Deploy

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
limiter = Limiter(
    key_func=get_remote_address
    #storage_uri=os.getenv("REDIS_URL", "memory://") # descomentar essa linha no Deploy
    )
mail = Mail()
