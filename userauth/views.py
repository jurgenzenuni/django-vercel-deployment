from django.shortcuts import render, redirect
from django.db import connection
import bcrypt


# Create your views here.

def home(request):
    username = request.session.get('username')
    return render(request, 'home.html', {'username': username})

def signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (firstname, lastname, email, username, password) VALUES (%s, %s, %s, %s, %s)",
                               [firstname, lastname, email, username, hashed_password])
        except Exception as e:
            return render(request, 'signup.html', {'error': f'Error occurred: {e}'})

        return redirect('home')
    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT username, password FROM users WHERE username = %s", [username])
            user = cursor.fetchone()

        if user:
            hashed_password = user[1].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                request.session['username'] = username
                return redirect('home')

        return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def logout(request):
    request.session.clear()
    return redirect('home') 

def profile(request): 
    return render(request, 'profile.html')
