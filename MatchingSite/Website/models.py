from django.db import models

class UserProfile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    #profile_image = models.ImageField(upload_to="PicFolder/",default="PicFolder/ball.jpg")
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length=1)
    #dob = models.DateField(auto_now=False, auto_now_add=False)
    #listOfHobbies =  a

class Hobbies(models.Model):
    #question = models.ForeignKey(Question, on_delete=models.CASCADE)
    hobby = models.CharField(max_length=200)
    userProf = models.ManyToManyField(UserProfile);
