from django.db import models
import datetime

class Hobby(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length=1)
    dob = models.DateField()
    hobUser = models.ManyToManyField(Hobby)
    image = models.ImageField(upload_to='PicFolder/')
