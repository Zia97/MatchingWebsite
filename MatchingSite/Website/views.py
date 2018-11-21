from django.http import HttpResponse
from django.shortcuts import render

from .models import UserProfile

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    context = {
    'UserProfile' : UserProfile
    }
    return render(request, 'Website/index.html', context)
