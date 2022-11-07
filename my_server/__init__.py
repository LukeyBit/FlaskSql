from flask import Flask
from my_server.config import Config
from my_server.main.routes import main

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(main)

from my_server import error