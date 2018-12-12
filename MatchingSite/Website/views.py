from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import UserProfile, Hobby
from django.template import loader
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
import socket

def index(request):
    response = redirect('/accounts/login/')
    return response


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.image = request.FILES['image']
            form.save()
            _first_name = form.cleaned_data['first_name']
            _last_name = form.cleaned_data['last_name']
            _username = form.cleaned_data['username']
            _email = form.cleaned_data['email']
            _gender = form.cleaned_data['sex']
            _dob = form.cleaned_data['birthdate']
            _image = form.cleaned_data['image']
            _hobbies = form.cleaned_data.get('hobbies')


            _password = form.cleaned_data['password1']

            user = authenticate(username=_username, password=_password)
            login(request, user)

            newUserProfile = UserProfile(first_name=_first_name,last_name=_last_name,username=_username,email=_email,gender=_gender,dob=_dob,image=_image)
            newUserProfile.save()

            for h in _hobbies:
                hobby = Hobby.objects.get(name=h)
                newUserProfile.hobUser.add(hobby)

            newUserProfile.save()
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

def users(request):
    if request.method == 'GET':
       newUserProfile = list(UserProfile.objects.values())
       return JsonResponse(dict(UserProfile=newUserProfile))
