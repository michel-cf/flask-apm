from flask import Flask
from flask_apm import Apm
import db
import config

from blog import blog_app

app = Flask(__name__)
config.configure(app)

# Blueprints with different components
app.register_blueprint(blog_app.app)

# SQL Alchemy
db.init_app(app)
# SQL Alchemy db migration system
db.alembic.init_app(app)

# APM
apm = Apm()
apm.init_app(app)
