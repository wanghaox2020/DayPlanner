from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


from django.http import HttpResponse

# Create your views here.

def register_view(request):
    if request.method =='GET':
        return render(request, 'user/SignUp.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return HttpResponse('two password must align with eachother')

    user = User.objects.create_user(username=username,password=password1)
    return HttpResponseRedirect('user/Login.html')

def login_view(request):
    if request.method == 'GET':
        # if this is a get we return a Login page
        return render(request, 'user/Login.html')
    elif request.method == 'POST':
        user = request.POST['username']
        pwd = request.POST['password']

        user = authenticate(username=user, password= pwd)

        if not user:
            return HttpResponse('Login failed')
        else:
            login(request, user)
            return HttpResponseRedirect('/index')

def index_view(request):

    return render(request,'user/index.html',locals())
        

