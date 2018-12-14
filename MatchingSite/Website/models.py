from django.db import models
import datetime


#Hobby model containing a single field stating the hobby name
class Hobby(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def as_json(self):
        return {'name': self.name}


#The user model which has a foreign key linked to the hobby model
#ManyToManyField with Hobby so that users can have many hobbies
class UserProfile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length=1)
    dob = models.DateField()
    hobUser = models.ManyToManyField(Hobby)
    image = models.ImageField(upload_to='PicFolder/')

    def __str__(self):
        return self.username

    #Allows us to return the user as a JSON dict object
    def as_json(self):
        return dict(
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            gender=self.gender,
            dob=self.dob,
            image=self.image.url,
            likeCount=self.liked.all().count(),
            hobUser=[h.as_json() for h in self.hobUser.all()],
        )


#This model creates a mapping between the user that liked and the liked user
class Like(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="likes")  #The current logged in user
    likedUser = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="liked")  #The user that was liked
