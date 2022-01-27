from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Data(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads')
    description= models.CharField(max_length=500, null=True, blank=True )

