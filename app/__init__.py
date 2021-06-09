
from flask import Flask

from app.utils import get_log
from main import views

app = Flask(__name__)

# app configuration
app.config.from_object('app.config')

# blueprints registration
app.register_blueprint(views.pages)

# logging config
get_log()
