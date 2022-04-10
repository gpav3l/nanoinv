import hashlib
from django.shortcuts import redirect

TIME_DELTA = 10

# Found person by login and password
# \return FIO if found, empty string in other case
def check_user_auth(password):
    password = password.strip()
    #pass_hash = hashlib.md5(password.encode()).hexdigest()
    if(password == "ed1tth1s"):
        return "editable"
    else:
        return ""


# Decorator for check user
def check_auth(function):
    def wrap(request, *args, **kwargs):
        if request.session.get("mode", "") == "":
            return redirect("login")
        else:
            return function(request, *args, **kwargs)
    return wrap


# Used for check in view function for detect current mode
def check_auth_inline(request):
    if request.session.get("mode", "") == "":
        return False
    else:
        return True


# Logout user
def logout_user(request):
    request.session["mode"] = ""


# Check, is session time is out
def __check_session_timeout(request):
    if request.session.get("lasttouch", -1) == -1:
        request.session["lasttouch"] = -1
        return False