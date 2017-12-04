from __future__ import print_function
import sys
from pickle import GET

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.template.context_processors import csrf, request
from django.shortcuts import render_to_response

from SAM2018 import observable
from SAM2018.models import Deadline, NotifcationTemp
from SAM2018.observable import Observable
from SAM2018.observer import Observer
from SAM2018.user import user, Role

users = []
class controlPanel(Observer):
     def update(self, *args, **kwargs):
          print ("update controlPanel")
          redirect("/")


def admin(request):
     context = {}
     return render(request, 'admin.html', context)


# hadlee user Management functionality
def whatUserGroup(user):
     if user.groups.filter(name__in=['PCC']).exists():
          return Role.PCC
     elif user.groups.filter(name__in=['Author']).exists():
          return Role.Author
     elif user.groups.filter(name__in=['PCM']).exists():
          return Role.PCM
     else:
          return Role.Admin

def readUserInfoSaveIntoArray():
     del users[:]
     alluser = User.objects.all()
     for u in alluser:
          users.append(user(u.first_name,u.last_name,u.email,whatUserGroup(u),u.username,u.password))


def getUserObject(usename):
     curentname = str(usename)
     alluser = User.objects.all()
     for u in alluser:
          if u.username == curentname.strip():
               return u
def getUserData(usename):
     curentname = str(usename)
     alluser = User.objects.all()
     for u in alluser:
          print("looking at   " + u.username + "    cpmapred wit  " + curentname)
          if u.username == curentname.strip():
               return user(u.first_name,u.last_name,u.email,whatUserGroup(u),u.username,u.password)
     return 'no user'



def userMangament(request):
     observable = Observable.SAMObservable
     observable.update_observers('nnsmsmhbbhhb', something='Hello World')
     context = {}
     context.update(csrf(request))
     selectedUser = request.GET.get('selectedUser')
     newuser = request.GET.get('addNewUser')
     # username = "khalidsalmalki"
     # password = "1"
     # user = authenticate(username=username, password=password)
     # login(request, user)

     if  selectedUser:
          selected = getUserData(selectedUser)

          context.update({'selectedUser': selected})
     elif newuser == 'new':
          context.update({'addNewUser': "yes"})
     context.update({'userMangament': "yes"})
     readUserInfoSaveIntoArray()
     print(len(users))
     context.update({'UserList':users})

     return render(request, 'admin.html', context)


def addNewUser(request):
     context = {}
     firstname = request.GET.get('firstname')
     lastname = request.GET.get('lastname')
     userName = request.GET.get('userName')
     password = request.GET.get('password')
     Email = request.GET.get('Email')

     role = request.GET.get('role')

     user = User.objects.create_user(username=userName,
                                     email=Email,
                              first_name =firstname,
                              last_name = lastname,
                                     password=password)

     groupName  = ''
     print ("role role role"+role)

     if role == 'PCC':
          groupName = 'PCC'
     elif role == 'PCM':
          groupName = 'PCM'
     else:
          groupName = 'Author'


     grupos = Group.objects.all().filter(name=groupName).first()
     user.groups.set([grupos])




     return redirect("/userMangament")
     # return render(request, 'admin.html', context)

def updateUser(request):
     context = {}
     firstname = request.GET.get('firstname')
     lastname = request.GET.get('lastname')
     Email = request.GET.get('Email')
     role = request.GET.get('role')
     userName = request.GET.get('userName')
     password = request.GET.get('password')
     User.objects.all().filter(username=userName).update(first_name =firstname,
                              last_name = lastname,username=userName,email=Email)
     groupName = ''
     user = getUserObject(userName)

     if role == 'PCC':
          groupName = 'PCC'
     elif role == 'PCM':
          groupName = 'PCM'
     else:
          groupName = 'Author'

     grupos = Group.objects.all().filter(name=groupName).first()
     user.groups.set([grupos])

     return redirect("/userMangament")


def deleteUser(request):
     userName = request.GET.get('userName')
     print ("user nqme ehf",userName)

     user = getUserObject(userName).delete()

     return redirect("/userMangament")

# hadlee  deadlines functionality
def setUpDeadlines():
     Deadline(nameID="paper_submission",date="2016-12-12").save()

def deadlines(request):
     context = {}
     selected = request.GET.get('selected')
     if selected:
          selected = selected.strip()
          print ("sdsds",Deadline.objects.all().filter(nameID=selected).first())
          context.update({'selected': Deadline.objects.all().filter(nameID=selected).first()})
     if len( Deadline.objects.all()) == 0:
          setUpDeadlines()
          print (len( Deadline.objects.all()))
     for te in Deadline.objects.all():
          print (" dad",te.nameID)

     context.update({'deadlines': Deadline.objects.all()})


     return render(request, 'admin.html', context)



def configsDeadLine(request):
     id = request.GET.get('pk')
     date = request.GET.get('date')
     print ("configsDeadLine",id,date)
     context = {}

     context.update({'deadlines': Deadline.objects.all()})
     Deadline.objects.all().filter(nameID=id).update(date=date)

     return render(request, 'admin.html', context)
# hadlee  templates  functionality

def templates(request):
     context = {}

     context.update({'templates': "yes"})
     return render(request, 'admin.html', context)

# hadlee  notifications  functionality
def setUpNotifcationTemp():
     NotifcationTemp(nameID="paper_submission",text="you have a nice paper").save()

def notifications(request):
     context = {}
     selected = request.GET.get('selected')
     if selected:
          selected = selected.strip()
          print("sdsds", NotifcationTemp.objects.all().filter(nameID=selected).first())
          context.update({'selected': NotifcationTemp.objects.all().filter(nameID=selected).first()})


     if len(NotifcationTemp.objects.all()) == 0:
          setUpNotifcationTemp()




     # NotifcationTemp
     context.update({'notificationsTemp': NotifcationTemp.objects.all()})
     return render(request, 'admin.html', context)


def updateNT(request):
     id = request.GET.get('pk')
     date = request.GET.get('date')
     print("updateNT", id, date)
     context = {}
     context.update({'notificationsTemp': NotifcationTemp.objects.all()})

     NotifcationTemp.objects.all().filter(nameID=id).update(text=date)

     return render(request, 'admin.html', context)