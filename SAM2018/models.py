from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.contrib.auth.models import User

def validate_file_extension(value):
  import os
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.pdf','.doc','.docx']
  if not ext in valid_extensions:
    raise ValidationError(u'File not supported!')

class Paper(models.Model):
    title = models.CharField(max_length=60, null=True)
    authorName = models.CharField(max_length=60, null=True)
    contact = models.CharField(max_length=60, null=True)
    version = models.CharField(max_length=60, null=True)
    uplaod = models.FileField(upload_to='documents/%Y/%m/%d', null=True,validators=[validate_file_extension])
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)




class Report(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    comments = models.CharField(max_length=500, null=True)
    rate = models.CharField(max_length=1, null=True)
    paper = models.ForeignKey(Paper, null=True)


class Review(models.Model):
    comment = models.CharField(max_length=500, null=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    pcm = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.CharField(max_length=1, null=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True)






class Deadlines(models.Model):
    date = models.CharField(max_length=60, null=True)
    group = models.CharField(max_length=60, null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


class Deadline(models.Model):
    nameID = models.CharField(max_length=60, null=True)
    date = models.CharField(max_length=60, null=True)
    createdAt = models.DateTimeField(auto_now=False, auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=False, auto_now_add=True)


class NotifcationTemp(models.Model):
    nameID = models.CharField(max_length=60, null=True)
    text = models.CharField(max_length=500, null=True)
    createdAt = models.DateTimeField(auto_now=False, auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=False, auto_now_add=True)

class Template(models.Model):
    nameID = models.CharField(max_length=60, null=True)
    text = models.CharField(max_length=10000, null=True)
    createdAt = models.DateTimeField(auto_now=False, auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=False, auto_now_add=True)


class favoritePaper(models.Model):
    pcm = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    papers = models.ForeignKey(Paper, null=True)

class Notifcation(models.Model):
    read = models.NullBooleanField(default=False)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reviewedPaper = models.CharField(max_length=60, null=True)
    notiftemp = models.ForeignKey(NotifcationTemp, on_delete=models.CASCADE, null=True)