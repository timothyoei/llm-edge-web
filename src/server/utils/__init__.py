from flask import Flask, current_app, g, url_for
from flask_pymongo import PyMongo
from flasgger import Swagger
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from datetime import timedelta
from routes import register_routes
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
import re
import logging

logging.basicConfig(level=logging.DEBUG)

# ============================================
# DATABASE HELPERS
# ============================================

def init_db(app, mongo_uri):
  app.config["MONGO_URI"] = mongo_uri
  with app.app_context():
    db = get_db()

def get_db():
  if "db" not in g:
    g.mongo = PyMongo(current_app)
    g.db = g.mongo.db
  return g.db

# ============================================
# AUTHORIZATION HELPERS
# ============================================

def config_auth(app, secret_key):
  app.config["JWT_SECRET_KEY"] = secret_key
  app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
  jwt = JWTManager(app)

# ============================================
# MAILING HELPERS
# ============================================

def config_mailer(app, mail_port, mail_username, mail_password):
  app.config["MAIL_SERVER"] = "smtp.gmail.com"
  app.config["MAIL_PORT"] = mail_port
  app.config["MAIL_USERNAME"] = mail_username
  app.config["MAIL_PASSWORD"] = mail_password
  app.config["MAIL_USE_TLS"] = False
  app.config["MAIL_USE_SSL"] = True

  with app.app_context():
    mailer = get_mailer()

def get_mailer():
  if "mailer" not in g:
    g.mailer = Mail(current_app)
  return g.mailer

def is_valid_email(email):
  pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
  return re.match(pattern, email)

def send_verification_email(email, confirm_token):
  confirm_url = f"localhost:5001/api/confirm_tokens/{confirm_token}"
  msg = Message("Please Confirm Your Email", sender=os.getenv("MAIL_USERNAME"), recipients=[email])
  msg.body = f"Hello! Please confirm your email using the following link: {confirm_url}"
  mailer = get_mailer()
  try:
    mailer.send(msg)
  except Exception as e:
    print(e)
    return False
  return True

# ============================================
# INITIALIZATION HELPER
# ============================================

def init_app():
  load_dotenv()

  app = Flask(__name__)

  init_db(app, os.getenv("MONGO_URI"))
  config_auth(app, os.getenv("JWT_SECRET_KEY"))
  config_mailer(app, os.getenv("MAIL_PORT"), os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"))
  swagger = Swagger(app)
  register_routes(app, os.getenv("API_URL_PREFIX"))

  return app