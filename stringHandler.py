class ErrorStringHandler():
    INVALID_EMAIL = {"success": False, "status_message": "Invalid email"}
    BAD_REQUEST = {"success": False, "status_message": "Bad request"}
    WRONG_PASSWORD = {"success": False, "status_message": "Wrong password"}
    USER_NOT_REGISTERED = {"success": False, "status_message": "User not registered"}

class SuccessStringHandler():
    REGISTRATION_SUCCESS = {"success": True, "status_message": "Successfully registerd"}
    EMAIL_ALREADY_REGISTERED = {"success": False, "status_message": "Email already registerd"}
    USERNAME_TAKEN = {"success": False, "status_message": "Username already taken"}

class ServerErrorStringHandler():
    INTERNAL_SERVER_ERROR = {"success": False, "status_message": "Internal server error"}