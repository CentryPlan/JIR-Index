# Jamaica Industrial Rates Application
# Author Ian Moncrieffe
# CentryPlan Building Services Jamaica.
#August 2019

# Dependencies
from redis import Redis

from logging.handlers import RotatingFileHandler, SMTPHandler
from flask import Flask, g, request, session

from flask_login import LoginManager, current_user
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_cache import Cache
from flask_wtf.csrf import CSRFProtect 
from flask_cors import CORS, cross_origin

from config import Config

app = Flask(__name__)

# enable CORS
CORS(app)

#Application Configuration
app.config.from_object(Config)

# Application Cache
cache = Cache(app)

# Bootstrap
Bootstrap(app)

# SQL3 Portable Database connection
db = SQLAlchemy(app)

# Cross Site Request Forgery protection
csrf = CSRFProtect(app)

#Application API 
#api = APIManager(app, flask_sqlalchemy_db=db)


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Handle user authentication
login_manager = LoginManager(app)
login_manager.login_view = "login"

 
bcrypt = Bcrypt(app)

redis_client = Redis()

# Implement Logging

app.logger.setLevel(app.config['LOG_LEVEL'])

file_handler = RotatingFileHandler('app.log')
app.logger.addHandler(file_handler)

'''
@migrate.configure
def configure_alembic(config):
	config = app.config
	return config
'''
@app.before_request
def check_csrf():
    csrf.protect()


@app.before_request
def _before_request():
	g.user = current_user

@app.before_request
def _last_page_visited():
	if "current_page" in session:
		session["last_page"] = session["current_page"]
		session["current_page"] = request.path
		session.permanent = True

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


if __name__ == '__main__':
	manager.run()
