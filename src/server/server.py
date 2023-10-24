from flask import Flask
from flasgger import Swagger
from db import init_db
from routes import register_routes
import os
from dotenv import load_dotenv

if __name__ == "__main__":
  load_dotenv()

  app = Flask(__name__)

  init_db(app, os.getenv("MONGO_URI"))
  swagger = Swagger(app)
  register_routes(app)

  app.run(debug=True)