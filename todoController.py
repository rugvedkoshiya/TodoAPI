from flask import Blueprint, jsonify, request, Response, redirect
import json
from jwtToken import jwtDecodeFunc

todoController = Blueprint('todo', __name__)


# Get todo by todo id
def getTodo(todo_id):
    print(todo_id)
    return Response(json.dumps("get"), status=200, mimetype='application/json')

# Edit todo by todo id
def editTodo(todo_id):
    print(todo_id)
    return Response(json.dumps("edited"), status=200, mimetype='application/json')

# Delete todo by todo id
def deleteTodo(todo_id):
    print(todo_id)
    return Response(json.dumps("delete"), status=200, mimetype='application/json')

# Get all todos
def getAllTodo(todo_id):
    print(todo_id)
    return Response(json.dumps("get all todo"), status=200, mimetype='application/json')

# Create new all todos
def createTodo(todo_id):
    print(todo_id)
    return Response(json.dumps("create todo"), status=200, mimetype='application/json')











#  Todo Controller
@todoController.route('/<int:todo_id>', methods=['GET', 'PUT', 'DELETE'])
def todoFunc(todo_id):

    if(request.method == "GET"):
        response = getTodo(todo_id)

    elif(request.method == "PUT"):
        response = editTodo(todo_id)

    elif(request.method == "DELETE"):
        response = deleteTodo(todo_id)

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@todoController.route('/', methods=['GET', 'POST'])
def todosFunc():

    if(request.method == "GET"):
        response = getAllTodo()

    elif(request.method == "POST"):
        response = createTodo()
    
    response.headers['Access-Control-Allow-Origin'] = '*'
    return "response"