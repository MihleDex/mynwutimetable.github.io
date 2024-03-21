from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    module_code = models.CharField(max_length=10)
