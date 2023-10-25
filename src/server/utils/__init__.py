from flask import Flask, current_app, g
from flask_pymongo import PyMongo
from flasgger import Swagger
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from datetime import timedelta
from routes import register_routes

def init_db(app, mongo_uri):
  app.config["MONGO_URI"] = mongo_uri
  with app.app_context():
    db = get_db()

def get_db():
  if 'db' not in g:
    g.mongo = PyMongo(current_app)
    g.db = g.mongo.db
  return g.db

def config_auth(app, secret_key):
  app.config["JWT_SECRET_KEY"] = secret_key
  app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
  jwt = JWTManager(app)

def init_app():
  load_dotenv()

  app = Flask(__name__)

  init_db(app, os.getenv("MONGO_URI"))
  config_auth(app, os.getenv("JWT_SECRET_KEY"))
  swagger = Swagger(app)
  register_routes(app, os.getenv("API_URL_PREFIX"))

  return app