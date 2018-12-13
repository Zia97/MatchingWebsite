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
    currentUser = UserProfile.objects.get(username=request.user)
    restUsers = UserProfile.objects.all().exclude(username=request.user)
    count = 0;
    pos = [0];
    usersArr = [""];
    i = 0;
    for rUser in restUsers:
        usersArr[i] = rUser.id
        count = count + 1;
        for cUser in currentUser.hobUser.all():
            for user in rUser.hobUser.all():
                if(cUser == user):
                    pos[i] = pos[i] + 1;
                else:
                    pos[i] = pos[i] + 0;
        if(count != len(restUsers)): #gone through already
            i = i + 1;
            pos.append(0)
            usersArr.append("")

    pos, usersArr = zip(*sorted(zip(pos, usersArr), reverse=True))
    pos, usersArr = (list(t) for t in zip(*sorted(zip(pos, usersArr),reverse=True)))

    rankedUsers = []
    for selectedUser in usersArr:
        rankedUsers.append(UserProfile.objects.get(id=selectedUser))
    resultsJson = [UserProfile.as_json() for UserProfile in rankedUsers]
    return JsonResponse(resultsJson, safe=False);
