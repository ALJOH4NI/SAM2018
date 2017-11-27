from django.db import models
from SAM2018.models import Review


class Report(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    comments = models.CharField(max_length=500, null=True)
    rate = models.CharField(max_length=1, null=True)
    reviews = models.ManyToManyField(
        Review,
        related_name='id',
    )