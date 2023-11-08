from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib import messages

# Create your views here.

def SignupView(request):
    if request.method == "POST":
        username,email,password,password1 = request.POST['username'],request.POST['email'],request.POST['password'],request.POST['password1']
        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.warning(request,"Username Already Exists")
                return redirect('AuthApp:login')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,"Email Already Exists")
                return redirect('AuthApp:login')
            else:
                User.objects.create_user(username=username,email=email,password=password)
                messages.info(request,"Account Created!!")
                return redirect('AuthApp:login')
        else:
            messages.warning(request,"Password mismatch")
            return redirect('AuthApp:login')



def LoginView(request):
    
    if request.method == 'GET':
        return render(request,'signup.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user:
            login(request,user)
            return redirect('UserApp:home')
        else:
            messages.error(request,'UserName/Password invalid, Try Again !!')
            return redirect('AuthApp:login')


def LogoutView(request):
    logout(request)
    return redirect('AuthApp:login')

