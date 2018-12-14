from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import *
from django.template import loader
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
import socket
from datetime import date, datetime as dt
from django.core.mail import EmailMessage


def index(request):
    response = redirect('/accounts/login/')
    return response

#This method handles the user registration on the register page.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.image = request.FILES['image']
            _password1 = request.POST['password1']
            _password2 = request.POST['password2']
            if _password1 != _password2:
                context = {
                    'form': form,
                    'invalid': "true"
                }
                return render(request, 'registration/register.html', context)
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

            #Saves our new user in the database
            newUserProfile = UserProfile(first_name=_first_name, last_name=_last_name,
                                         username=_username, email=_email, gender=_gender, dob=_dob, image=_image)
            newUserProfile.save()

            for h in _hobbies:
                hobby = Hobby.objects.get(name=h)
                newUserProfile.hobUser.add(hobby)

            newUserProfile.save()

            return redirect('index')
        else:
            #Validation incase some invalid fields are entered in the form
            if UserProfile.objects.filter(username=request.POST['username']).exists() or (request.POST['email'] and UserProfile.objects.filter(email=request.POST['email']).exclude(username=request.POST['username']).exists()):
                context = {'form': form}
                return render(request, 'registration/register.html', context)
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def home(request):
    context = {
        'UserProfile': UserProfile
    }
    return render(request, 'Website/home.html', context)


def users(request):
    if request.method == 'GET':
        userProfile = UserProfile.objects.get(username=request.user)
        userJson = userProfile.as_json()
    return JsonResponse(userJson)


#returns queryset of the users filtered by age and gender.
def allUsers(request):
    currDict = {}
    allDict = {}
    currresult = []

    usersdict = {}
    ageFilt = request.GET['ageFilt']
    genderFilt = request.GET['genderFilt']

    if request.method == 'GET':
        currentUser = UserProfile.objects.all().filter(username=request.user)
        currentUserJson = [UserProfile.as_json()
                           for UserProfile in currentUser]
        for currUser in currentUserJson:
            currDict = currUser.get('hobUser')
            for entry in currDict:
                names = []
                v = list(entry.values())
                {names[i]: v[i] for i in range(len(names))}
                currresult.append(v[0])
        if genderFilt == 'e':
            queryset = filterAge(request, ageFilt)
        else:
            users = filterAge(request, ageFilt)
            queryset = users.filter(gender=genderFilt).exclude(
                username=request.user)

        resultsJson = [UserProfile.as_json() for UserProfile in queryset]

        finallist = sortUsersOnHobbies(resultsJson,currresult)

    return JsonResponse(finallist, safe=False)


#This method sorts the users based on the most similar hobbies and returns an ordered list - users with the most similar hobbies are first
def sortUsersOnHobbies(resultsJson,currresult):
    usersdict = {}
    newres = {}
    counter = 0
    for user in resultsJson:
        tempresult = []
        allDict = user.get('hobUser')
        usersdict[counter] = user

        for entry in allDict:
            names = []
            v = list(entry.values())
            {names[i]: v[i] for i in range(len(names))}
            tempresult.append(v[0])

        s = set(currresult).intersection(tempresult)

        newres[counter] = len(s)
        counter = counter + 1

    testing = sorted(newres.items(), key=lambda x: x[1], reverse=True)

    mylist = [i[0] for i in testing]

    finallist = []

    for num in mylist:
        finallist.append(usersdict[num])

    return finallist;


#returns queryset of userprofiles, filtered by the age range.
def filterAge(request, val):
    current = dt.now()
    if val == "0":
        return UserProfile.objects.all().exclude(username=request.user)
    elif val == "1":
        min_date = date(current.year - int(18), current.month, current.day)
        max_date = date(current.year - int(30), current.month, current.day)
    elif val == "2":
        min_date = date(current.year - int(31), current.month, current.day)
        max_date = date(current.year - int(40), current.month, current.day)
    elif val == "3":
        min_date = date(current.year - int(41), current.month, current.day)
        max_date = date(current.year - int(50), current.month, current.day)
    elif val == "4":
        min_date = date(current.year - int(51), current.month, current.day)
        max_date = date(current.year - int(60), current.month, current.day)
    else:
        min_date = date(current.year - int(61), current.month, current.day)
        max_date = date(current.year - int(119), current.month, current.day)

    filteredUsers = UserProfile.objects.filter(
        dob__gte=max_date, dob__lte=min_date).exclude(username=request.user)
    return filteredUsers


def like(request):
    userLiked = UserProfile.objects.get(username=request.POST['user'])
    currentUser = UserProfile.objects.get(username=request.user)
    new_like, created = Like.objects.get_or_create(
        user=currentUser, likedUser=userLiked)
    if created:
        userProf = UserProfile.objects.get(username=request.POST['user'])
        numLikes = userProf.liked.all().count()
        sendEmail(userLiked,currentUser)
        return HttpResponse(numLikes)
    else:
        return HttpResponse("Already Liked")

#This method is responsible for sending the liked user an email, telling them who the like was from.
def sendEmail(userLiked, currentUser):
    email = EmailMessage('MatchingSite', 'You have a new like from '+currentUser.username,
                         'currentUser.email', [userLiked.email])
    email.send()
