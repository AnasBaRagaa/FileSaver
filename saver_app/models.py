from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Data(models.Model):
    title = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads', )
    description = models.CharField(max_length=500, null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.file.storage.delete(self.file.name)
        super().delete()


class SharingLink(models.Model):
    data = models.ForeignKey(Data, on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now=True)