# -*- coding: utf-8 -*-
import os

os_env = os.environ

class Config(object):
    SECRET_KEY = '3nF3Rn0'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    UPLOAD_FOLDER = '/static/img/uploads'
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    BROKER_URL = 'redis://redistogo:926e2ebd7e411547ded094aeb1939e0a@lab.redistogo.com:9464/'
    CELERY_RESULT_BACKEND = 'redis://redistogo:926e2ebd7e411547ded094aeb1939e0a@lab.redistogo.com:9464/'
    ENFERNO_ENV = 'dev'
    MONGODB_SETTINGS = {


        'db': 'heroku_r6gzx0bj',
        'host': 'mongodb://heroku_r6gzx0bj:52u7db1p5vasmg68iqpuk42niu@ds015730.mlab.com:15730/heroku_r6gzx0bj'

    }

    #security
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_CHANGEABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = '3nF3Rn0'

    SECURITY_POST_LOGIN_VIEW = '/resident?m=l'
    SECURITY_POST_CONFIRM_VIEW = '/resident?m=l'
    SECURITY_POST_REGISTER_VIEW = '/township'
    SECURITY_POST_CHANGE_VIEW = '/profile'
    SECURITY_UNAUTHORIZED_VIEW = '/profile'

    #flask mail settings - Mailgun
    MAIL_SERVER = 'smtp.mailgun.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'postmaster@sandbox915ad276f504436e85698563f521a724.mailgun.org'
    MAIL_PASSWORD = 'davajvmasd12345'
    MAIL_DEFAULT_SENDER = 'info@nikitph.com'
    SECURITY_EMAIL_SENDER = 'info@nikitph.com'



class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = False
    DEBUG_TB_ENABLED = False
    ASSETS_DEBUG = False  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    BROKER_URL = 'redis://localhost:6379/10'
    REDIS_URL = 'redis://localhost:6379/10'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/10'
    MONGODB_SETTINGS = {
        'db': 'houzee'
    }


