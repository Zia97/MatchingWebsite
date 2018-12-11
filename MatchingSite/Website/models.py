from django.db import models
import datetime

class UserProfile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length=1)
    dob = models.DateField()
    hobUser = models.ManyToManyField('Hobbies')
    model_pic = models.ImageField(upload_to='PicFolder/')

class Hobbies(models.Model):
    hobby = models.CharField(max_length=200)
