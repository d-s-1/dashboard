import dash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


app = dash.Dash(__name__)
app_flask = app.server

# configure Flask settings
app_flask.config.from_object(Config)

db = SQLAlchemy(app_flask)
migrate = Migrate(app_flask, db)


# this import is a workaround to circular imports in Flask since other modules need to import the app variable defined above
from app import models, layout, interactivity