# config.py
# File: config.py
import logging
import os, genny


LOG_LEVEL=logging.ERROR

class Config(object):
    ''' Application Base Configuration
    '''

    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True

    PORT = 9711 #rate 72 61 74 65 
    HOST = '0.0.0.0'
    PLATFORM_OWNER = 'Construction Software Inc.'
    PLATFORM_USER = 'CentryPlan Building Services'
    
    SECRET_KEY = genny.genid('key')

    SSL_REDIRECT = False

    CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = genny.genid('key')

    # Application Onboard Database Config
    DB_HANDLE = "/storage/app.db"
    DBASE = BASE_DIR + DB_HANDLE
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DBASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True

    POSTS_PER_PAGE = 20
    FOLLOWERS_PER_PAGE = 100
    COMMENTS_PER_PAGE = 20
    SLOW_DB_QUERY_TIME = 0.25

    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    IMAGES_DIR = os.path.join(STATIC_DIR, 'imgs')
    PROFILE_IMAGE_DIR = os.path.join(IMAGES_DIR, 'profile')
    DOC_DIR = os.path.join(STATIC_DIR, 'docs')
    TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'templates')
    # Email
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'centryplan@gmail.com' #os.environ.get('MAIL_USERNAME')
    #MAIL_PASSWORD = '' #os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'centryplan@gmail.com'
    JIRI_MAIL_SUBJECT_PREFIX = '[JIRI]'
    JIRI_MAIL_SENDER = 'Jamaica Industrial Rates Index Admin <centryplan@gmail.com>'

    # Administrator list
    ADMIN_EMAILS = ['centryplan@gmail.com']

    # Celerey Broker 
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    LOG_DIRECTORY  = '/logs'
    LOG_BASE = BASE_DIR + LOG_DIRECTORY
    LOG_LEVEL=logging.WARNING
    
    BOOTSTRAP_SERVE_LOCAL = True

    CACHE_TYPE = 'redis'
    # File Uploads
    MAX_CONTENT_LENGTH = 1024 * 1024 * 20
    
'''
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/builders_dev.db'.format(Config.BASE_DIR)
    LOG_LEVEL=logging.DEBUG


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/builders_test.db'.format(Config.BASE_DIR)
    WTF_CSRF_ENABLED = False
    LOG_LEVEL=logging.ERROR


class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/builders.db'.format(Config.BASE_DIR)
    MAX_CONTENT_LENGTH = 1024 * 20

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False

    POSTS_PER_PAGE = 10
    FOLLOWERS_PER_PAGE = 20
    COMMENTS_PER_PAGE = 20
    VRSTAN_SLOW_DB_QUERY_TIME = 0.25

    
    LOG_LEVEL=logging.WARNING

'''

