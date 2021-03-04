import os

class Config:
    SECRET_KEY = 'pitch'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringaaccess:messi@localhost/pitch'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    
# simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
#  email configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    SENDER_EMAIL ='zefmesssi77@gmail.com'



class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringaaccess:messi@localhost/pitches_test'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringaaccess:messi@localhost/pitch' 
    DEVELOPMENT = True
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}