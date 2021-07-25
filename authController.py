from flask import Blueprint, request, Response
from config import Config
# importing setting as per enviroment
if Config.DEBUG == True:
    from config import TestingConfig as SETTING
else:
    from config import ProductionConfig as SETTING

authController = Blueprint('auth', __name__)

import hashlib
from app import db
from models import User, UserTodo
import re, json
from stringHandler import SuccessStringHandler, ErrorStringHandler, ServerErrorStringHandler
from jwtToken import jwtEncodeFunc, jwtDecodeFunc

# email REGEX
EMAIL_REGEX = re.compile(r"[\da-zA-Z](?:[\da-zA-Z]+[-.!$%&'*+/=?^_`{|}~]?[\da-zA-Z]+)*@[\da-zA-Z](?:[\da-zA-Z]*[-.]?[\da-zA-Z]+)*\.[\da-zA-Z]+")


# auth controllers
@authController.route('/login', methods=['POST'])
def loginFunc():
    try:
        if "id" in request.form and "password" in request.form:
            id = request.form["id"]
            password = hashlib.sha256(request.form["password"].encode()).hexdigest()

            # check user is registered or not
            if db.session.query(User).filter(User.id == id).count() != 0:

                # check password
                if db.session.query(User).filter(User.id == id, User.password == password).count() != 0:
                    userDataObj = db.session.query(User).get(id)
                    jwtToken = jwtEncodeFunc(userDataObj = userDataObj)
                    if jwtToken != 1:
                        formattedData = {
                            "username" : id,
                            "token" : jwtToken
                        }
                        response = Response(json.dumps(formattedData), status=200, mimetype='application/json')
                    else:
                        response = Response(json.dumps(ServerErrorStringHandler.INTERNAL_SERVER_ERROR), status=500, mimetype='application/json')
                else:
                    response = Response(json.dumps(ErrorStringHandler.WRONG_PASSWORD), status=401, mimetype='application/json')
            else:
                response = Response(json.dumps(ErrorStringHandler.USER_NOT_REGISTERED), status=404, mimetype='application/json')
        else:
            response = Response(json.dumps(ErrorStringHandler.BAD_REQUEST), status=400, mimetype='application/json')
        
        # sending response
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        if SETTING.DEBUG:
            print(e)
        response = Response(json.dumps(ServerErrorStringHandler.INTERNAL_SERVER_ERROR), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response




@authController.route('/signup', methods=['POST'])
def signupFunc():
    try:
        # grab data from request
        if "id" in request.form and "fname" in request.form and "lname" in request.form and "email" in request.form and "password" in request.form:
            id = request.form["id"]
            fname = request.form["fname"]
            lname = request.form["lname"]
            email = request.form["email"]
            password = hashlib.sha256(request.form["password"].encode()).hexdigest()

            # authenticate admin access
            if "isadmin" in request.form and request.form["isadmin"] == SETTING.ADMIN_KEY:
                isadmin = 1
            else:
                isadmin = 0
            
            # senetize fields
            if EMAIL_REGEX.match(email):

                # check id and email are uniq or not 
                if db.session.query(User).filter(User.id == id).count() == 0:
                    if db.session.query(User).filter(User.email == email).count() == 0:

                        # add entry to database
                        user = User(id=id, fname=fname, lname=lname, email=email, password=password, isactive=0, isadmin=isadmin)
                        db.session.add(user)
                        db.session.commit()

                        # add user todo entry
                        userData = UserTodo(id=id, todos=[])
                        db.session.add(userData)
                        db.session.commit()
                        
                        response = Response(json.dumps(SuccessStringHandler.REGISTRATION_SUCCESS), status=201, mimetype='application/json')
                    else:
                        # email is already registerd
                        response = Response(json.dumps(SuccessStringHandler.EMAIL_ALREADY_REGISTERED), status=200, mimetype='application/json')
                else:
                    # username taken
                    response = Response(json.dumps(SuccessStringHandler.USERNAME_TAKEN), status=200, mimetype='application/json')
            else:
                # email not valid
                response = Response(json.dumps(ErrorStringHandler.INVALID_EMAIL), status=400, mimetype='application/json')
        else:
            # bad request
            response = Response(json.dumps(ErrorStringHandler.BAD_REQUEST), status=400, mimetype='application/json')
        
        # send response
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    
    # error handler
    except Exception as e:
        if SETTING.DEBUG:
            print(e)
        response = Response(json.dumps(ServerErrorStringHandler.INTERNAL_SERVER_ERROR), status=500, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response