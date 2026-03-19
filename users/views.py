from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import MainUser

# Create your views here.

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        avatar = request.POST.get('avatar')

        if MainUser.objects.filter(username=username).exists():
            return render(request, "users/register.html", {"error": "Username already exists"})
        
        user = MainUser.objects.create_user(username=username, password=password, avatar=avatar)
        login(request, user)
        return redirect('home')
    
    return render(request, 'users/register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credantails'})
        
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')