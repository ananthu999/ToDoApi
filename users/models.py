from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    username=models.CharField(max_length=100,unique=True,blank=True,null=False)
    password=models.CharField(max_length=100)
    REQUIRED_FIELDS=[]
    def __str__(self):
        return self.username

# ToDo list for logined abstract user
class ToDo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    title=models.CharField(max_length=100)
    # time = models.DateTimeField(null=True)

    time = models.DateTimeField()
    description=models.CharField(max_length=100)
    completed=models.BooleanField(default=False)
    def __str__(self):
        return self.title