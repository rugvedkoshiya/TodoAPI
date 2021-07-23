from flask import Flask, jsonify, request, Response, redirect
from config import Config as SETTING
from authController import authController
from todoController import todoController
import json

app = Flask(__name__)
app.secret_key = SETTING.SECRET_KEY

app.register_blueprint(authController, url_prefix='/auth')
app.register_blueprint(todoController, url_prefix='/todo')

app.run(debug=SETTING.DEBUG)