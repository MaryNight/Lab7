from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    pass

class Lesson(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=255)
	datetime = models.DateTimeField(auto_now=True)
