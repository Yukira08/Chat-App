from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
# Create your models here.

class User(AbstractUser):
    description = models.CharField(max_length=300)
    online_status = models.IntegerField(default=0)
    offline_time = models.TimeField(default = datetime.now())
    img = models.ImageField(default='pic.jpg',upload_to='profile_pics/')

class Friendship(models.Model):
    #add status field
    friends=models.ManyToManyField(User,null=True)
    cur_user=models.ForeignKey(User,related_name='center',on_delete=models.CASCADE,null=True)
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

