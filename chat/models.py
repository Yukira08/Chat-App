from django.db import models
# from django.contrib.auth.models import User AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.conf import settings
from django.db.models.deletion import CASCADE
from django import forms
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea

# from django.contrib.auth.models import User
# Create your models here.
#

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    participants=models.ManyToManyField(to=settings.AUTH_USER_MODEL)

class Message(models.Model): #Change to Message
    idmessage=models.AutoField(primary_key=True)
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    room =models.ForeignKey(Room,on_delete=models.CASCADE)
    date=models.DateTimeField()
    message=models.CharField(max_length=1000,null=True)
    filename=models.CharField(max_length=100,null=True)
    path=models.CharField(max_length=500,null=True)

class YourModelForm(forms.ModelForm):
    short_text = forms.CharField(widget=EmojiPickerTextInput)
    long_text = forms.CharField(widget=EmojiPickerTextarea)
    class Meta:
        model = Message
        fields=('message','idmessage')