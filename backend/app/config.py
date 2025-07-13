from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # App
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    
    # DB
    DB_ENGINE = 'mysql+mysqlconnector'
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    SQLALCHEMY_DATABASE_URI = f'{DB_ENGINE}://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_BLACKLIST_ENABLED = True
    JWT_TOKEN_LOCATION = ['headers']
    JWT_COOKIE_SECURE = True
    JWT_BLACKLIST_TOKEN_CHECKS=['access','refresh']

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    #JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
    #JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=2)

class ProductionConfig(Config):
    DEBUG = False
    PROPAGATE_EXCEPTIONS = True

config_dict = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}