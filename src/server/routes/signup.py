from flask import Blueprint, request, jsonify
from db import get_db
from werkzeug.security import generate_password_hash

signup_bp = Blueprint("signup", __name__)

@signup_bp.route("/signup", methods=["POST"])
def signup():
  """
  Endpoint for user signups
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
          - fName
          - lName
          - password
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
          password:
            type: string
            description: The user's password
  responses:
    201:
      description: User successfully created
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
    500:
      description: Internal server error
      schema:
        properties:
          error:
            type: string
            description: Error message
  """
  if request.method == "POST":
    return signup_post()

def signup_post():
  # Validate incoming data
  data = request.get_json()
  if not data:
    return jsonify({"error": "Data missing"}), 400
  req_fields = ["email", "fName", "lName", "password"]
  for f in req_fields:
    if not data.get(f):
      return jsonify({"error": f"{f} field missing"}), 400

  # Check if the user already exists
  db = get_db()
  if db.Users.find_one({"email": data["email"]}):
    return jsonify({"error": "User already exists"}), 400

  # Create a new user
  new_user = {
    "email": data["email"],
    "fName": data["fName"],
    "lName": data["lName"],
    "password": generate_password_hash(data["password"]),
    "chatHistory": [],
    "theme": "dark"
  }
  try:
    db.Users.insert_one(new_user)
  except Exception as e:
    print(f"An error occurred while inserting the user: {e}")
    return jsonify({'error': 'Server error'}), 500
  
  del_fields = ["_id", "password"]
  for f in del_fields:
    new_user.pop(f)
  return jsonify(new_user), 201