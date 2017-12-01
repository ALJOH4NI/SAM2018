from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Paper(models.Model):
    title = models.CharField(max_length=60, null = True)
    uplaod = models.FileField(upload_to='documents/%Y/%m/%d',null = True)
    version = models.CharField(max_length=60, null = True)
    date= models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    #rate = models.CharField(max_length=60, null = True)

class Review(models.Model):
    comment = models.CharField(max_length=500)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    pcm = models.ForeignKey(User, on_delete=models.CASCADE)

class Notifcation(models.Model):
    read = models.NullBooleanField(default=False)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, null = True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)

class Deadline(models.Model):
    nameID = models.CharField(max_length=60, null=True)
    date = models.CharField(max_length=60, null=True)
    createdAt = models.DateTimeField(auto_now=False, auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=False, auto_now_add=True)
