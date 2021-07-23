from flask import Blueprint
authController = Blueprint('auth', __name__)


# Auth Controller

@authController.route('/login', methods=['POST'])
def loginFunc():
    return "loginFunc"

@authController.route('/signup', methods=['POST'])
def signupFunc():
    return "signupFunc"

def verifyAuthFunc():
    return 1

