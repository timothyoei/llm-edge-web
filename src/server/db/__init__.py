from flask import current_app, g
from flask_pymongo import PyMongo
from urllib.parse import quote_plus

def init_db(app, mongo_uri):
  app.config["MONGO_URI"] = mongo_uri

  with app.app_context():
    db = get_db()

def get_db():
  if 'db' not in g:
    g.mongo = PyMongo(current_app)
    g.db = g.mongo.db
  return g.db