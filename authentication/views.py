from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# TODO: REMOVE this import.  We SHOULD use csrf
from django.views.decorators.csrf import csrf_exempt


from django.http import HttpResponse

# Create your views here.

# TODO: REMOVE this decorator.  We SHOULD use csrf
@csrf_exempt
def register_view(request):
    if request.method =='GET':
        return render(request, 'authentication/signup.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return HttpResponse('two password must align with eachother')

    user = User.objects.create_user(username=username,password=password1)
    return HttpResponseRedirect('index')

# TODO: REMOVE this decorator.  We SHOULD use csrf
@csrf_exempt
def login_view(request):
    if request.method == 'GET':
        # if this is a get we return a Login page
        return render(request, 'authentication/login.html')
    elif request.method == 'POST':
        user = request.POST['username']
        pwd = request.POST['password']

        user = authenticate(username=user, password= pwd)

        if not user:
            return HttpResponse('Login failed')
        else:
            login(request, user)
            path = request.GET.get ("next") or ('index')
            return HttpResponseRedirect(path)

def logout(request):
    p = auth.logout(request)
    print(p)
    return HttpResponseRedirect('index')

def index_view(request):
    login_user = request.user
    return render(request, "dayplanner/index.html", locals())
        

