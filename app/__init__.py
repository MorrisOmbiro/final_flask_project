import requests
import itertools
import re

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap


csrf = CSRFProtect()
app = Flask(__name__) # gunicorn will find you
app.url_map.strict_slashes = False
Bootstrap(app)
app.config["SECRET_KEY"] = "row the boat"
csrf.init_app(app)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import routes
