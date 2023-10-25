from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from utils import get_db

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["POST"])
def users():
  """
  Endpoint for users
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
          - fName
          - lName
        properties:
          email:
            type: string
            description: The user's email
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
    return users_post_handler()

def users_post_handler():
  # Validate incoming data
  data = request.get_json()
  if not data:
    return jsonify({"error": "Data missing"}), 400
  req_fields = ["email","password"]
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
    "password": generate_password_hash(data["password"]),
    "isActive": False,
    "theme": "dark"
  }
  try:
    db.Users.insert_one(new_user)
  except Exception as e:
    print(f"An error occurred while inserting the user: {e}")
    return jsonify({'error': 'Server error'}), 500
  
  del_fields = ["_id", "password", "isActive"]
  for f in del_fields:
    new_user.pop(f)
  return jsonify(new_user), 201