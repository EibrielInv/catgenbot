from flask import Flask
from flask.ext.restful import Api

app = Flask(__name__)

api = Api(app)

from catgenbot.modules.main import main
app.register_blueprint(main)
