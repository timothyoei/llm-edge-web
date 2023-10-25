from flask import Blueprint, request, jsonify
from utils import get_db
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from flasgger import swag_from

chats_bp = Blueprint("chats", __name__)

@chats_bp.route("/chats", methods=["GET", "POST"])
@jwt_required()
@swag_from("../docs/chats_get.yml")
@swag_from("../docs/chats_post.yml")
def chats():
  db = get_db()
  if request.method == "GET":
    return chats_get_handler(db)
  elif request.method == "POST":
    return chats_post_handler(db)

def chats_get_handler(db):
  chats = list(db.Chats.find({"email": get_jwt_identity()}))
  for c in chats:
    c["_id"] = str(c["_id"])
  return jsonify({"chats": chats}), 200

def chats_post_handler(db):
  # Validate incoming data
  data = request.get_json()
  if not data:
    return jsonify({"error": "Data missing"}), 400
  req_fields = ["init_query"]
  for f in req_fields:
    if not data.get(f):
      return jsonify({"error": f"{f} field missing"}), 400

  # Insert new chat
  new_chat = {
    "title": "TEST TITLE",
    "email": get_jwt_identity(),
    "history": [{"query": data["init_query"], "response": "TEST RESPONSE"}]
  }
  db = get_db()
  res_chats_insert = db.Chats.insert_one(new_chat)
  new_chat["_id"] = res_chats_insert.inserted_id

  return jsonify(new_chat), 201

@chats_bp.route("/chats/<string:chat_id>", methods=["GET", "DELETE"])
@jwt_required()
def chat(chat_id):
  """
  Endpoint for a single chat
  ---
  parameters:
    - in: path
      name: chat_id
      required: true
      description: The ID of the chat to retrieve
      type: string
    - in: header
      name: Authorization
      required: true
      description: The JWT token for the user that this chat belongs to
      type: string
      default: Bearer JWT_TOKEN
  responses:
    200:
      description: Chat details
      schema:
        properties:
          _id:
            type: string
            description: The chat's unique ID
          title:
            type: string
            description: The title of the chat
          email:
            type: string
            description: The email that this chat belongs to
          history:
            type: array
            items:
              type: object
              properties:
                query:
                  type: string
                  description: The input to the model
                response:
                  type: string
                  description: The output of the model
    204:
      description: Chat details
      schema:
        type: object
        properties:
          message:
            type: string
            description: Deletion result
  """
  db = get_db()
  if request.method == "GET":
    return chat_get_handler(chat_id, db)
  elif request.method == "DELETE":
    return chat_delete_handler(chat_id, db)

def chat_get_handler(chat_id, db):
  res = db.Chats.find_one({"_id": ObjectId(chat_id)})
  res["_id"] = str(res["_id"])
  return jsonify(res), 200

def chat_delete_handler(chat_id, db):
  db.Chats.delete_one({"_id": ObjectId(chat_id)})
  return jsonify({"message": "Successfully deleted chat"}), 200