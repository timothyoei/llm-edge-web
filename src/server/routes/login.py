from flask import Blueprint, request, jsonify
from db import get_db
from werkzeug.security import check_password_hash

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
  """
  Endpoint for user logins
  ---
  consumes:
    - application/json
  parameters:
    - in: body
      name: body
      required: true
      schema:
        required:
          - email
          - password
        properties:
          email:
            type: string
            description: The user's email
          password:
            type: string
            description: The user's password
  responses:
    200:
      description: User login successful
      schema:
        properties:
          email:
            type: string
            description: The user's email
          fName:
            type: string
            description: The user's first name
          lName:
            type: string
            description: The user's last name
          chatHistory:
            type: array
            items:
              type: object
              properties:
                query:
                  type: string
                  description: The chatbot input text
                response:
                  type: string
                  description: The chatbot output text
          theme:
            type: string
            description: The user's theme preference
    400:
      description: Bad request
      schema:
        properties:
          error:
            type: string
            description: Error message
    401:
      description: Password mismatch
      schema:
        properties:
          error:
            type: string
            description: Error message
  """
  if request.method == "POST":
    return login_post()

def login_post():
  # Validate incoming data
  data = request.get_json()
  if not data:
    return jsonify({"error": "Data missing"}), 400
  req_fields = ["email", "password"]
  for f in req_fields:
    if not data.get(f):
      return jsonify({"error": f"{f} field missing"}), 400

  db = get_db()
  user = db.Users.find_one({"email": data["email"]})

  # Check if the user exists
  if not user:
    return jsonify({"error": "User does not exist"}), 400

  # Check if the password matches
  if not check_password_hash(user["password"], data["password"]):
    return jsonify({"error": "Password does not match"}), 401

  del_fields = ["_id", "password"]
  for f in del_fields:
    user.pop(f)

  return jsonify(user), 200