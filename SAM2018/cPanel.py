from __future__ import print_function

import sys
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group

from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.shortcuts import render_to_response

from SAM2018.user import user, Role

users = []
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
          users.append(user(u.first_name,u.last_name,u.email,whatUserGroup(u),u.username))


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
               return user(u.first_name,u.last_name,u.email,whatUserGroup(u),u.username)
     return 'no user'



def userMangament(request):
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
     Email = request.GET.get('Email')
     role = request.GET.get('role')

     user = User.objects.create_user(username=firstname + lastname,
                                     email=Email,
                              first_name =firstname,
                              last_name = lastname,
                                     password=firstname)

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
     print (userName)
     User.objects.all().filter(username=userName).update(first_name =firstname,
                              last_name = lastname)
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
     role = request.GET.get('role')
     user = User.objects.all().filter(username=userName).first()
     grupos = Group.objects.all().filter(name=role)
     grupos.filter(name=user).delete()
     return redirect("/userMangament")

# hadlee  deadlines functionality

def deadlines(request):
     context = {}

     context.update({'deadlines': "yes"})
     return render(request, 'admin.html', context)

# hadlee  templates  functionality

def templates(request):
     context = {}

     context.update({'templates': "yes"})
     return render(request, 'admin.html', context)

# hadlee  notifications  functionality

def notifications(request):
     context = {}

     context.update({'notifications': "yes"})
     return render(request, 'admin.html', context)


