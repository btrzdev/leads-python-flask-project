from flask import Flask
from app.configs import database, migrations
from app import routes


def create_app():
    app = Flask(__name__)  

    database.init_app(app)
    migrations.init_app(app)
    routes.init_app(app)

    return app
    

