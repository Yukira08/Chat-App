from django.db import models
# from django.contrib.auth.models import User AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.conf import settings
from django.db.models.deletion import CASCADE
# from django.contrib.auth.models import User
# Create your models here.


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    participants=models.ManyToManyField(to=settings.AUTH_USER_MODEL)


class Message(models.Model): #Change to Message
    idmessage=models.IntegerField(primary_key=True)
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    room =models.ForeignKey(Room,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now=True)
    message=models.CharField(max_length=1000)
    #path
