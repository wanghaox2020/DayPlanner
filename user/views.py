from django.http.response import HttpResponseRedirect
from django.shortcuts import render


from django.http import HttpResponse

# Create your views here.

def register_view(request):
    if request.method =='GET':
        return render(request, 'user/SignUp.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password2']
        password2 = request.POST['password2']
        if password1 != password2:
            return HttpResponse('two password must align with eachother')

    user = user.objects.create_user(username=username,password=password1)
    return HttpResponseRedirect('user/SignUp.html')

def login_view(request):
    if request.method == 'GET':
        return
    elif request.method == 'POST':
        return

