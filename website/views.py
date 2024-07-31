from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
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

def delete_record(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to view this page...")
        return redirect('home')

    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, f"Customer ID #{pk} deleted successfully!")
    return redirect('home')

def add_record(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to view this page...")
        return redirect('home')

    form = AddRecordForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Record added...")
        return redirect('home')
    
    return render(request, 'add_record.html', {'form': form})

def update_record(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to view this page...")
        return redirect('home')

    record = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=record)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Record updated...")
        return render(request, 'record.html', {'record': record})
    return render(request, 'update_record.html', {'form': form})
    

def register_user(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, "You've successfully registered")
        return redirect('home')
    
    return render(request, 'register.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out!")
    return render(request, 'home.html', {})
