from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "You've been logged in!")
        else:
            messages.error(request, "Credentials does not match!")
    return render(request, 'home.html', {})

def login_user(request):
    pass

def register_user(request):
    return render(request, 'register.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out!")
    return render(request, 'home.html', {})
