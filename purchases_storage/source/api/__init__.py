from flask import Flask
from core import api_config

app = Flask(__name__)
app.config['SECRET_KEY'] = api_config['secret_key']
from .api import *