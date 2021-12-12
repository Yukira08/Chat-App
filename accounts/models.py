from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
# Create your models here.

class Client(AbstractUser):
    description = models.CharField(max_length=300)

class Friendship(models.Model):
    friends=models.ManyToManyField(Client,null=True)
    cur_user=models.ForeignKey(Client,related_name='center',on_delete=models.CASCADE,null=True)
    @classmethod
    def make_friend(cls,cur_user,new_friend):
        friend,create=cls.objects.get_or_create(
            cur_user=cur_user
        )
        friend.friends.add(new_friend)
    
    @classmethod
    def unfriend(cls,cur_user,new_friend):
        friend,create=cls.objects.get_or_create(
            cur_user=cur_user
        )
        friend.friends.remove(new_friend)

