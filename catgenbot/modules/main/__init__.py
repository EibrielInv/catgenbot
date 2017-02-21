from flask import Flask
from flask import Blueprint
from flask import jsonify
from flask import request

import json
import requests

import random as rd

from catgenbot import app

main = Blueprint('main', __name__)


def save_stats(json_status):
    return
    json_status["count"] += 1
    with open("stats.json", 'w', encoding='utf-8') as data_file:
         json.dump(json_status, data_file, sort_keys=True, indent=4, separators=(',', ': '))

@main.route('/', methods=['POST', 'GET']) 
def index():
    msg = request.json

    json_status = {
        "count": 0,
        "inline": 0,
        "no_message": 0,
        "left_chat_member": 0,
        "new_chat_member": 0,
        "no_text": 0,
        "avatar": 0
    }
    #with open("stats.json", encoding='utf-8') as data_file:
    #    try:
    #        json_status_open = json.load(data_file)
    #        for key in json_status_open:
    #            json_status[key] = json_status_open[key]
    #    except:
    #        raise


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
        json_status["inline"] += 1
        save_stats(json_status)
        return jsonify(answer)

    if not "message" in msg:
        json_status["no_message"] += 1
        save_stats(json_status)
        return jsonify({})

    if "left_chat_member" in msg["message"]:
        if rd.random()>0.5:
            answer = {
                'method': "sendMessage",
                'chat_id': msg["message"]["chat"]["id"],
                'text': '{0} 😿'.format(msg["message"]["left_chat_member"]["first_name"])
            }
            json_status["left_chat_member"] += 1
            save_stats(json_status)
            return jsonify(answer)
    elif "new_chat_member" in msg["message"]:
        if msg["message"]["new_chat_member"]["first_name"].lower() == app.config["BOT_USERNAME"].lower():
            answer = {
                'method': "sendMessage",
                'chat_id': msg["message"]["chat"]["id"],
                'text': 'Hi! 😸'
            }
            json_status["new_chat_member"] += 1
            save_stats(json_status)
            return jsonify(answer)
        if rd.random()>0.5:
            answer = {
                'method': "sendMessage",
                'chat_id': msg["message"]["chat"]["id"],
                'text': 'Welcome {0}! 😸'.format(msg["message"]["new_chat_member"]["first_name"])
            }
            json_status["new_chat_member"] += 1
            save_stats(json_status)
            return jsonify(answer)

    if msg["message"]["chat"]["type"] not in ["private", "group"]:
        return jsonify({})

    if not "text" in msg["message"]:
        answer = {
            'method': "sendMessage",
            'chat_id': msg["message"]["chat"]["id"],
            'text': "Hi! *Write your name and get your cat avatar!*",
            'parse_mode': 'Markdown',
        }
        json_status["no_text"] += 1
        save_stats(json_status)
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

    if msg["message"]["text"].startswith("/"):
        answer = {
            'method': "sendMessage",
            'chat_id': msg["message"]["chat"]["id"],
            'text': "*Reply this message with your name and get your cat avatar!* (_Right click_ or _tap and hold_ on this message and select _Reply_)",
            'parse_mode': 'Markdown',
        }


    json_status["avatar"] += 1
    save_stats(json_status)
    return jsonify(answer)
