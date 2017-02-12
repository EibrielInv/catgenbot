from flask import Flask
from flask import Blueprint
from flask import jsonify
from flask import request

main = Blueprint('main', __name__)

@main.route('/')
def index():
    print ("main")
    print (request.json)
    answer = {
        "method": "sendMessage"
        "chat_id":
        "text": "This is a test"
    }
    return jsonify({"ok": True})
