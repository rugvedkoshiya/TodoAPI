class ErrorStringHandler():
    INVALID_EMAIL = {"success": False, "status_message": "Invalid email"}
    BAD_REQUEST = {"success": False, "status_message": "Bad request"}
    WRONG_PASSWORD = {"success": False, "status_message": "Wrong password"}
    USER_NOT_REGISTERED = {"success": False, "status_message": "User not registered"}
    UNAUTHORIZED = {"success": False, "status_message": "Unauthorized"}
    EXPIRED_TOKEN = {"success": False, "status_message": "Token expired, login again"}
    INVALID_TOKEN = {"success": False, "status_message": "Token expired, login again"}
    TODO_NOT_EXISTS = {"success": False, "status_message": "Todo doesn't exists"}

class SuccessStringHandler():
    REGISTRATION_SUCCESS = {"success": True, "status_message": "Successfully registerd"}
    EMAIL_ALREADY_REGISTERED = {"success": False, "status_message": "Email already registerd"}
    USERNAME_TAKEN = {"success": False, "status_message": "Username already taken"}
    TODO_CREATED = {"success": True, "status_message": "Todo created"}
    TODO_EXISTS = {"success": False, "status_message": "Todo aleady exists"}
    TODO_EDITED = {"success": True, "status_message": "Todo edited successfully"}
    TODO_DELETED = {"success": True, "status_message": "Todo deleted successfully"}

class ServerErrorStringHandler():
    INTERNAL_SERVER_ERROR = {"success": False, "status_message": "Internal server error"}