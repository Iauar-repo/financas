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
    #RATELIMIT_STORAGE_URL = os.getenv("REDIS_URL") # uncomment for deploy
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_BLACKLIST_ENABLED = True
    JWT_TOKEN_LOCATION = ['headers']
    JWT_COOKIE_SECURE = True
    JWT_BLACKLIST_TOKEN_CHECKS=['access','refresh']

    # MAIL
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # Google
    RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")
    RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")
    GOOGLE_CLIENT_ID = "540997724283-ist5ne58nrpq3o2mbc7k8hilb9o3ferp.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "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"

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