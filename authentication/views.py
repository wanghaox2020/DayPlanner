from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# TODO: REMOVE this import.  We SHOULD use csrf
from django.views.decorators.csrf import csrf_exempt


# TODO: REMOVE this decorator.  We SHOULD use csrf
@csrf_exempt
def register_view(request):
    context = {}
    handle_message(request, context)
    if request.method == "GET":
        return render(request, "authentication/signup.html", context)
    elif request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 != password2:
            request.session["Error_Message"] = "Password and Repeat Password should be the same!"
            return HttpResponseRedirect(request.path)
        try:
            user = User.objects.create_user(
                email=email, username=username, password=password1
            )
            login(request, user)
        except Exception as e:
            request.session["Error_Message"] = str(e)
            return HttpResponseRedirect(request.path)

    return HttpResponseRedirect("index")


# TODO: REMOVE this decorator.  We SHOULD use csrf
@csrf_exempt
def login_view(request):
    context = {}
    handle_message(request, context)
    if request.method == "GET":
        # if this is a get we return a Login page
        return render(request, "authentication/login.html", context)
    elif request.method == "POST":
        user = request.POST["username"]
        pwd = request.POST["password"]

        user = authenticate(username=user, password=pwd)
        if not user:
            # Create Error Message
            request.session["Error_Message"] = "Your Username/Password is incorrect !!"
            return HttpResponseRedirect(request.path)
        else:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponseRedirect("/admin")
            path = request.GET.get("next") or ("index")
            return HttpResponseRedirect(path)


def logout(request):
    p = auth.logout(request)
    print(p)
    return HttpResponseRedirect("index")


def index_view(request):
    login_user = request.user
    return render(request, "dayplanner/index.html", locals())


def handle_message(request, context):
    if "Error_Message" in request.session:
        context["error"] = request.session["Error_Message"]
        del request.session["Error_Message"]
    elif "Success_Message" in request.session:
        context["message"] = request.session["Success_Message"]
        del request.session["Success_Message"]
