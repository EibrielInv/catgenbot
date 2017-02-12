from flask import Flask
from flask import Blueprint
from flask import jsonify
from flask import request

import json
import requests

from catgenbot import app

main = Blueprint('main', __name__)

@main.route('/', methods=['POST', 'GET']) 
def index():
    msg = request.json

    if "inline_query" in msg:
        inline_results = [
            {'type': 'photo',
            'id': '1',
            'photo_url': "http://peppercarrot.com/extras/html/2016_cat-generator/avatar.php?seed={0}".format(msg["inline_query"]["query"].replace(" ", "+")),
            'thumb_url': "http://peppercarrot.com/themes/peppercarrot-theme_v2/cat-avatar-generator.php?seed={0}".format(msg["inline_query"]["query"].replace(" ", "+")),
            'caption': "{0}'s avatar! create yours with\n@{1} 😸".format(msg["inline_query"]["query"],app.config["BOT_USERNAME"]),
            }
        ]

        inline_json = json.dumps(inline_results)

        answer = {
            'method': "answerInlineQuery",
            'inline_query_id': msg["inline_query"]["id"],
            'results': inline_json,
            'cache_time': 3000
        }
        return jsonify(answer)

    if not "message" in msg or msg["message"]["chat"]["type"] != "private":
        return jsonify({})

    if "left_chat_member" in msg["message"]:
        if rd.random()>0.5:
            answer = {
                'method': "sendMessage",
                'chat_id': msg["message"]["chat"]["id"],
                'text': '{0} 😿'.format(msg["message"]["left_chat_member"]["first_name"])
            }
            return jsonify(answer)
    elif "new_chat_member" in msg["message"]:
        if rd.random()>0.5:
            answer = {
                'method': "sendMessage",
                'chat_id': msg["message"]["chat"]["id"],
                'text': 'Welcome {0}! 😸'.format(msg["message"]["new_chat_member"]["first_name"])
            }
            return jsonify(answer)

    if not "text" in msg["message"]:
        answer = {
            'method': "sendMessage",
            'chat_id': msg["message"]["chat"]["id"],
            'text': "Hi! *Write your name and get your cat avatar!*",
            'parse_mode': 'Markdown',
        }
        return jsonify(answer)

    answer = {
        'method': "sendPhoto",
        'photo': "http://peppercarrot.com/extras/html/2016_cat-generator/avatar.php?seed={0}".format(msg["message"]["text"].replace(" ", "+")),
        'chat_id': msg["message"]["chat"]["id"],
        'caption': "{0}'s avatar! create yours with @{1} 😸\nArt from http://peppercarrot.com\n\nAlso, rDany bot, your virtual BFF!\n@rDanyBot 🤖".format(msg["message"]["text"], app.config["BOT_USERNAME"]),
        'parse_mode': "Markdown"
    }

    if msg["message"]["text"].startswith("/start"):
        answer = {
            'method': "sendMessage",
            'chat_id': msg["message"]["chat"]["id"],
            'text': "Hi! *Write your name and get your cat avatar!*",
            'parse_mode': 'Markdown',
        }


    return jsonify(answer)
