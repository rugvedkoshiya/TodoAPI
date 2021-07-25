from flask import Flask, jsonify, request, Response, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid, base64, json
from config import Config

# importing setting as per enviroment
if Config.DEBUG == True:
    from config import TestingConfig as SETTING
else:
    from config import ProductionConfig as SETTING

# configure app
app = Flask(__name__)
app.secret_key = SETTING.SECRET_KEY

# configure database
app.config["SQLALCHEMY_DATABASE_URI"] = SETTING.DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from authController import authController
from todoController import todoController

# register bluprint of controllers
app.register_blueprint(authController, url_prefix='/auth')
app.register_blueprint(todoController, url_prefix='/todo')


# started server
if __name__ == "__main__":
    app.run(debug=SETTING.DEBUG)