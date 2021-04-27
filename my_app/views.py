from django.shortcuts import render, redirect
from .models import User 
from django.contrib import messages
import bcrypt  

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')
    else:
        uname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        bday = request.POST['birthday']
        pwd_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() # create the hash
        user = User.objects.create(username=uname, email=email, password=pwd_hash, birthday=bday)
        request.session['logged_in'] = user.id 
        return redirect('/success')

def success(request):
    context = {
        "logged_in" : User.objects.get(id=request.session['logged_in'])
    }
    return render(request, 'success.html', context)

def login_page(request):
    return render(request, 'login.html')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/login')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['logged_in'] = user.id 
        return redirect('/success')


    