from flask import Blueprint, jsonify, request, Response, redirect
import json
from jwtToken import jwtDecodeFunc
from stringHandler import ErrorStringHandler, ServerErrorStringHandler, SuccessStringHandler
todoController = Blueprint('todo', __name__)
from config import Config

# importing setting as per enviroment
if Config.DEBUG == True:
    from config import TestingConfig as SETTING
else:
    from config import ProductionConfig as SETTING
from app import db
from models import UserTodo


# Get todo by todo id
def getTodo(username, todoId):
    try:
        userData = db.session.query(UserTodo).filter(UserTodo.id == username).first()
        formattedData = {
            "username" : userData.id,
            "todos" : userData.todos[todoId]
        }
        return Response(json.dumps(formattedData), status=200, mimetype='application/json')
    except IndexError:
        return Response(json.dumps(ErrorStringHandler.TODO_NOT_EXISTS), status=404, mimetype='application/json')
    except Exception as e:
        if SETTING.DEBUG:
            print(e)
        return Response(json.dumps(ServerErrorStringHandler.INTERNAL_SERVER_ERROR), status=500, mimetype='application/json')


# Edit todo by todo id
def editTodo(username, todoId, todo):
    try:
        if todo != "":
            # grab old todos
            userData = db.session.query(UserTodo).filter(UserTodo.id == username).first()
            newData = userData.todos

            # check that todo already exists or not
            if todo not in newData:
                userData = db.session.query(UserTodo).filter(UserTodo.id == username).first()
                newData = userData.todos
                newData[todoId] = todo

                # add into database
                db.session.execute(db.update(UserTodo).where(UserTodo.id == username).values(todos=newData))
                db.session.commit()
                return Response(json.dumps(SuccessStringHandler.TODO_EDITED), status=200, mimetype='application/json')
            else:
                return Response(json.dumps(SuccessStringHandler.TODO_EXISTS), status=200, mimetype='application/json')
        else:
            return Response(json.dumps(ErrorStringHandler.BAD_REQUEST), status=400, mimetype='application/json')
    except IndexError:
        return Response(json.dumps(ErrorStringHandler.TODO_NOT_EXISTS), status=404, mimetype='application/json')
    except Exception as e:
        if SETTING.DEBUG:
            print(e)
        return Response(json.dumps(ServerErrorStringHandler.INTERNAL_SERVER_ERROR), status=500, mimetype='application/json')


# Delete todo by todo id
def deleteTodo(username, todoId):
    try:
        # grab old todos
        userData = db.session.query(UserTodo).filter(UserTodo.id == username).first()
        newData = userData.todos
        newData.pop(todoId)

        # add into database
        db.session.execute(db.update(UserTodo).where(UserTodo.id == username).values(todos=newData))
        db.session.commit()
        return Response(json.dumps(SuccessStringHandler.TODO_DELETED), status=200, mimetype='application/json')
    except IndexError:
        return Response(json.dumps(ErrorStringHandler.TODO_NOT_EXISTS), status=404, mimetype='application/json')
    except Exception as e:
        if SETTING.DEBUG:
            print(e)
        return Response(json.dumps(ServerErrorStringHandler.INTERNAL_SERVER_ERROR), status=500, mimetype='application/json')


# Get all todos
def getAllTodo(username):
    try:
        # grab todos
        userData = db.session.query(UserTodo).filter(UserTodo.id == username).first()
        formattedData = {
            "username" : userData.id,
            "todos" : userData.todos
        }
        return Response(json.dumps(formattedData), status=200, mimetype='application/json')
    except Exception as e:
        if SETTING.DEBUG:
            print(e)
        return Response(json.dumps(ServerErrorStringHandler.INTERNAL_SERVER_ERROR), status=500, mimetype='application/json')


# Create new all todos
def createTodo(username, todo):
    try:
        if todo != "":
            # grab old todos
            userData = db.session.query(UserTodo).filter(UserTodo.id == username).first()
            newData = userData.todos

            # check that todo already exists or not
            if todo not in newData:

                # append new todo into array
                newData.append(todo)

                # add into database
                db.session.execute(db.update(UserTodo).where(UserTodo.id == username).values(todos=newData))
                db.session.commit()
                return Response(json.dumps(SuccessStringHandler.TODO_CREATED), status=201, mimetype='application/json')
            else:
                return Response(json.dumps(SuccessStringHandler.TODO_EXISTS), status=200, mimetype='application/json')
        else:
            return Response(json.dumps(ErrorStringHandler.BAD_REQUEST), status=400, mimetype='application/json')
    except Exception as e:
        if SETTING.DEBUG:
            print(e)
        return Response(json.dumps(ServerErrorStringHandler.INTERNAL_SERVER_ERROR), status=500, mimetype='application/json')



#  Todo Controller
@todoController.route('/<int:todoId>', methods=['GET', 'PUT', 'DELETE'])
def todoFunc(todoId):

    # get single todo
    if(request.method == "GET"):
        if "Authorization" in request.headers:
            userData = jwtDecodeFunc(request.headers.get("Authorization")[7:])
            if userData == "Expired":
                response = Response(json.dumps(ErrorStringHandler.EXPIRED_TOKEN), status=401, mimetype='application/json')
            elif userData == "Invalid":
                response = Response(json.dumps(ErrorStringHandler.INVALID_TOKEN), status=401, mimetype='application/json')
            elif userData == "Error":
                response = Response(json.dumps(ServerErrorStringHandler.INTERNAL_SERVER_ERROR), status=500, mimetype='application/json')
            else:
                response = getTodo(username=userData["username"], todoId=todoId)
        else:
            response = Response(json.dumps(ErrorStringHandler.UNAUTHORIZED), status=401, mimetype='application/json')
    
    # edit todo
    elif(request.method == "PUT"):
        if "Authorization" in request.headers:
            if "todo" in request.form:
                userData = jwtDecodeFunc(request.headers.get("Authorization")[7:])
                if userData == "Expired":
                    response = Response(json.dumps(ErrorStringHandler.EXPIRED_TOKEN), status=401, mimetype='application/json')
                elif userData == "Invalid":
                    response = Response(json.dumps(ErrorStringHandler.INVALID_TOKEN), status=401, mimetype='application/json')
                elif userData == "Error":
                    response = Response(json.dumps(ServerErrorStringHandler.INTERNAL_SERVER_ERROR), status=500, mimetype='application/json')
                else:
                    todo = request.form["todo"]
                    response = editTodo(username=userData["username"], todoId=todoId, todo=todo)
            else:
                response = Response(json.dumps(ErrorStringHandler.BAD_REQUEST), status=400, mimetype='application/json')
        else:
            response = Response(json.dumps(ErrorStringHandler.UNAUTHORIZED), status=401, mimetype='application/json')

    # delete todo
    elif(request.method == "DELETE"):
        if "Authorization" in request.headers:
            userData = jwtDecodeFunc(request.headers.get("Authorization")[7:])
            if userData == "Expired":
                response = Response(json.dumps(ErrorStringHandler.EXPIRED_TOKEN), status=401, mimetype='application/json')
            elif userData == "Invalid":
                response = Response(json.dumps(ErrorStringHandler.INVALID_TOKEN), status=401, mimetype='application/json')
            elif userData == "Error":
                response = Response(json.dumps(ServerErrorStringHandler.INTERNAL_SERVER_ERROR), status=500, mimetype='application/json')
            else:
                response = deleteTodo(username=userData["username"], todoId=todoId)
        else:
            response = Response(json.dumps(ErrorStringHandler.UNAUTHORIZED), status=401, mimetype='application/json')

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@todoController.route('/', methods=['GET', 'POST'])
def todosFunc():

    # get all todos
    if(request.method == "GET"):
        if "Authorization" in request.headers:
            userData = jwtDecodeFunc(request.headers.get("Authorization")[7:])
            if userData == "Expired":
                response = Response(json.dumps(ErrorStringHandler.EXPIRED_TOKEN), status=401, mimetype='application/json')
            elif userData == "Invalid":
                response = Response(json.dumps(ErrorStringHandler.INVALID_TOKEN), status=401, mimetype='application/json')
            elif userData == "Error":
                response = Response(json.dumps(ServerErrorStringHandler.INTERNAL_SERVER_ERROR), status=500, mimetype='application/json')
            else:
                response = getAllTodo(username=userData["username"])
        else:
            response = Response(json.dumps(ErrorStringHandler.UNAUTHORIZED), status=401, mimetype='application/json')

    # create new todo
    elif(request.method == "POST"):
        if "Authorization" in request.headers:
            if "todo" in request.form:
                userData = jwtDecodeFunc(request.headers.get("Authorization")[7:])
                if userData == "Expired":
                    response = Response(json.dumps(ErrorStringHandler.EXPIRED_TOKEN), status=401, mimetype='application/json')
                elif userData == "Invalid":
                    response = Response(json.dumps(ErrorStringHandler.INVALID_TOKEN), status=401, mimetype='application/json')
                elif userData == "Error":
                    response = Response(json.dumps(ServerErrorStringHandler.INTERNAL_SERVER_ERROR), status=500, mimetype='application/json')
                else:
                    todo = request.form["todo"]
                    response = createTodo(username=userData["username"], todo=todo)
            else:
                response = Response(json.dumps(ErrorStringHandler.BAD_REQUEST), status=400, mimetype='application/json')
        else:
            response = Response(json.dumps(ErrorStringHandler.UNAUTHORIZED), status=401, mimetype='application/json')
    
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response