from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from utils import get_db

confirm_tokens_bp = Blueprint("confirm_tokens", __name__)

@confirm_tokens_bp.route("/confirm_tokens/<string:token>", methods=["GET"])
def confirm_tokens(token):
  """
  Endpoint for confirmation tokens
  ---
  parameters:
    - in: path
      name: token
      required: true
      description: The confirmation token of the user being confirmed
      type: string
  responses:
    200:
      description: Successfully confirmed user
      schema:
        properties:
          message:
            type: string
            description: Indication of success
    400:
      description: User does not exist
      schema:
        properties:
          error:
            type: string
            description: Error message
    500:
      description: Server failed to confirm user
      schema:
        properties:
          error:
            type: string
            description: Error message
  """
  if request.method == "GET":
    return confirm_tokens_get_handler(token)

def confirm_tokens_get_handler(token):
  db = get_db()

  res_users_find = db.Users.find_one({"confirmToken": token})
  if not res_users_find:
    return jsonify({"error": "User does not exist"}), 400

  res_users_update = db.Users.update_one({"email": res_users_find["email"]}, {"$set": {"isConfirmed": True}})
  if res_users_update.modified_count > 0:
    return jsonify({"message": "User successfully confirmed"}), 200
  return jsonify({"error": "Server error"}), 500