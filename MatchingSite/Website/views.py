from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import UserProfile

def index(request):
    response = redirect('/accounts/login/')
    return response

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()

    context = {'form' : form}
    return render(request, 'registration/register.html', context)

@login_required
def home(request):
    context = {
        'UserProfile' : UserProfile
    }
    return render(request, 'Website/home.html', context)
