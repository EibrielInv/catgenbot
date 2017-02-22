from flask import Flask
from flask import Blueprint
from flask import jsonify
from flask import request

import json
import time
import requests
import datetime

import random as rd

from catgenbot import app

main = Blueprint('main', __name__)

## SQLITE

import sqlite3
from flask import g

DATABASE = 'stats.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def sqlite_execute(query, name, debug = False):
    try:
        cur = get_db().execute(query)
        get_db().commit()
        print ('{0} applied'.format(name))
        return True
    except sqlite3.OperationalError:
        print ('{0} already applied'.format(name))
        if debug:
            raise
        return False
    except:
        raise


def init_db ():
    sqlite_execute('''CREATE TABLE stats
                         (id integer primary key, query_type integer)''', "stats")

    sqlite_execute('''ALTER TABLE stats
                     ADD COLUMN datetime integer;''',
                     "datetime on stats")

    sqlite_execute('''ALTER TABLE stats
                     ADD COLUMN days integer;''',
                     "days on stats")
##

def save_stats(query_type):
    epoch = datetime.datetime.utcfromtimestamp(0)
    today = datetime.datetime.today()
    d = today - epoch
    #d.days # timedelta object
    get_db().execute("INSERT INTO stats VALUES (null, ?, ?, ?)", [query_type, int(time.time()), d.days])
    get_db().commit()


@main.route('/', methods=['POST', 'GET']) 
def index():
    msg = request.json

    init_db()


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
        save_stats("inline")
        return jsonify(answer)

    if not "message" in msg:
        save_stats("no_message")
        return jsonify({})

    if "left_chat_member" in msg["message"]:
        if rd.random()>0.5:
            answer = {
                'method': "sendMessage",
                'chat_id': msg["message"]["chat"]["id"],
                'text': '{0} 😿'.format(msg["message"]["left_chat_member"]["first_name"])
            }
            save_stats("left_chat_member")
            return jsonify(answer)
    elif "new_chat_member" in msg["message"]:
        if msg["message"]["new_chat_member"]["first_name"].lower() == app.config["BOT_USERNAME"].lower():
            answer = {
                'method': "sendMessage",
                'chat_id': msg["message"]["chat"]["id"],
                'text': 'Hi! 😸'
            }
            save_stats("new_chat_myself")
            return jsonify(answer)
        if rd.random()>0.5:
            answer = {
                'method': "sendMessage",
                'chat_id': msg["message"]["chat"]["id"],
                'text': 'Welcome {0}! 😸'.format(msg["message"]["new_chat_member"]["first_name"])
            }
            save_stats("new_chat_member")
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
        save_stats("no_text")
        return jsonify(answer)

    answer = {
        'method': "sendPhoto",
        'photo': "http://peppercarrot.com/extras/html/2016_cat-generator/avatar.php?seed={0}".format(msg["message"]["text"].replace(" ", "+")),
        'chat_id': msg["message"]["chat"]["id"],
        'caption': "{0}'s avatar! create yours with @{1} 😸\n\nArt from http://peppercarrot.com\n\n⭐️⭐️⭐️⭐️⭐️ https://telegram.me/storebot?start={1}".format(msg["message"]["text"], app.config["BOT_USERNAME"]),
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


    save_stats("avatar")
    return jsonify(answer)
