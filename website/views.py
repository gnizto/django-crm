from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "You've been logged in!")
        else:
            messages.error(request, "Credentials does not match!")
    return render(request, 'home.html', {'records': records})

def login_user(request):
    pass

def customer_record(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to view this page...")
        return redirect('home')

    record = Record.objects.get(id=pk)
    return render(request, 'record.html', {'record': record})

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You've successfully registered")
            return redirect('home')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out!")
    return render(request, 'home.html', {})
