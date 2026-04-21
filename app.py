from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb+srv://admin:123456qwerty@cluster0.mvdyb6h.mongodb.net/?appName=Cluster0")
db = client["bot"]
users_collection = db["users"]


def convert_mongo(data):
    if isinstance(data, list):
        return [convert_mongo(item) for item in data]

    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = convert_mongo(value)
        return result

    if isinstance(data, ObjectId):
        return str(data)

    if isinstance(data, datetime):
        return data.isoformat()

    return data


@app.route("/")
def home():
    return jsonify({"ok": True, "message": "API works"})


@app.route("/users")
def get_users():
    users = list(users_collection.find())
    return jsonify({
        "ok": True,
        "count": len(users),
        "users": convert_mongo(users)
    })
