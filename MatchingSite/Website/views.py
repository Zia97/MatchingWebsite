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
            for h in _hobbies:
                print(h)


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
        userProfile = UserProfile.objects.get(username=request.user)
        userJson = userProfile.as_json()
    return JsonResponse(userJson)

def allUsers(request):
    currDict = {}
    allDict = {}
    result = {}
    if request.method == 'GET':
        currentUser = UserProfile.objects.all().filter(username=request.user)
        currentUserJson = [UserProfile.as_json() for UserProfile in currentUser]
        for currUser in currentUserJson:
            print(currUser.get('hobUser'))
            currDict = currUser.get('hobUser')
            for entry in currDict:
                result.update(entry.values())
        print(result)
        users = UserProfile.objects.all().exclude(username=request.user)
        resultsJson = [UserProfile.as_json() for UserProfile in users]
        for user in resultsJson:
            print(user.get('hobUser'))
            allDict = user.get('hobUser')
        # shared_items = {k: currUser[k] for k in currUser if k in allDict and currUser[k] == allDict[k]}
        # print(shared_items)
    return JsonResponse(resultsJson, safe=False);
