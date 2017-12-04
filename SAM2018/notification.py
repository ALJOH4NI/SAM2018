<<<<<<< HEAD
from django.shortcuts import render
from django.template.loader import render_to_string


def setUp(data):

    return  render_to_string( 'notification.html', data)

=======
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers

from SAM2018.models import Notifcation, NotifcationTemp, Review


def index(request):
    role = request.GET.get('role')
    username = request.GET.get('username')
    user = User.objects.all().filter(username=username).first()


    data = []

    for n in Notifcation.objects.all().filter(read=False).filter(user=user):
        if n.paper_id:
            data.append({"PaperTitle":n.paper.title,"text":n.notiftemp.text,"id":n.id})
        elif n.reviewedPaper:

            data.append({"isRead":n.read,"text":n.notiftemp.text,"id":n.id,"title":Review.objects.all().filter(id=n.reviewedPaper).paper.title})
        else:
            data.append({"isRead":n.read,"text":n.notiftemp.text,"id":n.id})




    return JsonResponse({"data":data})
>>>>>>> b6220ecf5aeb1c103088aa29944cb848a33a4b6d
