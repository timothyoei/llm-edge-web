from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from bson.objectid import ObjectId
from utils import get_db

sessions_bp = Blueprint("sessions", __name__)

@sessions_bp.route("/sessions", methods=["POST"])
def sessions():
  """
  Endpoint for sessions
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
      description: Session creation successful
      schema:
        type: object
        properties:
          user:
            type: object
            properties:
              email:
                type: string
                description: The user's email
              theme:
                type: string
                description: The user's theme preference
          token:
            type: string
            description: The user's authentication token
          Session ID:
            type: string
            description: The ID of the new session
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
    return sessions_post_handler()

def sessions_post_handler():
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

  access_token = create_access_token(identity=user["email"])
  new_session = {
    "email": user["email"],
    "token": access_token
  }
  res_session_insert = db.Sessions.insert_one(new_session)

  # Delete unnecessary fields before sending response
  del_fields = ["_id", "password"]
  for f in del_fields:
    user.pop(f)

  return jsonify({"user": user, "token": access_token, "session_id": str(res_session_insert.inserted_id)}), 200

@sessions_bp.route("/sessions/<string:session_id>", methods=["DELETE"])
@jwt_required()
def session(session_id):
  """
  Endpoint for single sessions
  ---
  consumes:
    - application/json
  parameters:
    - in: path
      name: session_id
      required: true
      description: The ID of the session to delete
      type: string
    - in: header
      name: Authorization
      required: true
      type: string
      default: Bearer JWT_TOKEN
  responses:
    204:
      description: Session deletion successful
      schema:
        type: object
        properties:
          message:
            type: string
            description: Session deletion result
  """
  if request.method == "DELETE":
    return session_delete_handler(session_id)

def session_delete_handler(session_id):
  db = get_db()
  res = db.Sessions.delete_one({"_id": ObjectId(session_id)})
  return jsonify({"message": "Successfully logged out"}), 204