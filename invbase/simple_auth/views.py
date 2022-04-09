from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .service import *
from .forms import *


# Login page
def login(request):
    error_msg = request.session.get("login_error", "")
    request.session["login_error"] = ""
    acess_req_form = LoginForms()
    return render(request, 'simple_auth/sign-in.html', {'login_form': acess_req_form, 'error_msg': error_msg})


# Logout page
def logout(request):
    logout_user(request)
    return redirect("index")


# Page to check input
# redirect to 'home' if success or to 'login' in other case
def check(request):
    if request.method == 'POST':
        if "password" in request.POST:
            request.session["mode"] = check_user_auth(request.POST["password"])
            if request.session["mode"] == "":
                request.session["login_error"] = "Wrong password"
            else:
                return redirect("index", permanent=True)
        else:
            request.session["login_error"] = "Password is empty"
    else:
        request.session["login_error"] = "Internal error"

    return redirect("login", permanent=True)