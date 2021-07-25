import datetime
import jwt
from config import Config

# importing setting as per enviroment
if Config.DEBUG == True:
    from config import TestingConfig as SETTING
else:
    from config import ProductionConfig as SETTING


# jwt encode function
def jwtEncodeFunc(userDataObj):
    try:
        payload = {
            'username': userDataObj.id,
            "fname" : userDataObj.fname,
            "lname" : userDataObj.lname,
            "email": userDataObj.email,
            "isactive" : userDataObj.isactive,
            "isadmin" : userDataObj.isadmin,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=24),
            'iat': datetime.datetime.utcnow(),
        }
        return jwt.encode(
            payload,
            SETTING.SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return 1


# jwt decode function
def jwtDecodeFunc(token):
    try:
        payload = jwt.decode(jwt=token, key=SETTING.SECRET_KEY, algorithms="HS256")
        return {"username" : payload['username'], "exp" : payload['exp']}
    except jwt.ExpiredSignatureError:
        return "Expired"
    except jwt.InvalidTokenError:
        return "Invalid"
    except:
        return "Error"