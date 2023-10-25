from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from utils import get_db, is_valid_email, send_verification_email
from bson.objectid import ObjectId

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

  # Validate email
  if not is_valid_email(data["email"]):
    return jsonify({"error": "Invalid email"}), 400

  # Check if the user already exists
  db = get_db()
  if db.Users.find_one({"email": data["email"]}):
    return jsonify({"error": "User already exists"}), 400

  # Create a new user
  confirm_token = generate_password_hash(data["email"])
  new_user = {
    "email": data["email"],
    "password": generate_password_hash(data["password"]),
    "isConfirmed": False,
    "confirmToken": confirm_token,
    "theme": "dark"
  }
  try:
    res_users_insert = db.Users.insert_one(new_user)
  except Exception as e:
    return jsonify({"error": "Server error"}), 500
  
  # Remove unnecessary fields from response
  del_fields = ["password", "isConfirmed"]
  for f in del_fields:
    new_user.pop(f)
  new_user["_id"] = str(res_users_insert.inserted_id)
  
  return jsonify(new_user), 201

@users_bp.route("/users/<string:user_id>/verify", methods=["POST"])
def user_verify(user_id):
  """
  Endpoint for user verification
  ---
  parameters:
    - in: path
      name: user_id
      required: true
      description: The ID of the user being verified
      type: string
  responses:
    200:
      description: Successfully sent user verification email
      schema:
        properties:
          message:
            type: string
            description: Indication of successful email delivery
    500:
      description: Internal server error
      schema:
        properties:
          error:
            type: string
            description: Error message
  """
  if request.method == "POST":
    return user_verify_post_handler(user_id)

def user_verify_post_handler(user_id):
  db = get_db()
  res_users_find = db.Users.find_one({"_id": ObjectId(user_id)})
  if not send_verification_email(res_users_find["email"], res_users_find["confirmToken"]):
    return jsonify({"error": "Server error"}), 500
  return jsonify({"message": "Verification email sent"}), 200