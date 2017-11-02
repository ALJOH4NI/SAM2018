from django.shortcuts import render, redirect
from .forms import Signupform, UplaodFile
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import Group
from .models import Paper, Notifcation
from django.contrib.auth.models import User



# Create your views here.
def index(request):
    context = {}
    if request.user.is_authenticated() == False:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')

    elif request.user.is_authenticated():

        if request.user.groups.filter(name__in=['PCC']).exists():
            context.update({'is_pcc': 'is_pcc'})
            notification = Notifcation.objects.filter(read=False)
            papers = Paper.objects.all()
            num_notification = len(notification)

            #List<String> list = Arraylist<Strin>;
            #String s = list.get(0);
            #request.user.groups.all() = ['ss']
            #request.user.groups.all().first() = 'ss'

            context.update({'groups': request.user.groups.all().first(),'NumNotifications':num_notification,'notification':notification, 'papers':papers})

        elif request.user.groups.filter(name__in=['Author']).exists():
            context.update({'is_author':'is_author'})
            form = UplaodFile(request.POST, request.FILES)
            if request.method == "POST":
                form = UplaodFile(request.POST, request.FILES)
                if form.is_valid():
                    newpaper = Paper(uplaod = request.FILES['uplaod'], title = request.POST['title'], version="1", user = request.user )
                    newpaper.save()
                    user = User.objects.filter(groups__name='PCC').first()
                    notification = Notifcation(user = user, paper= newpaper)
                    notification.save()
            else:
                form = UplaodFile()
            context.update({'groups': request.user.groups.all().first(), 'form':form})

    return render(request, 'index.html', context)


def view_paper(request, id):
    context = {}
    if request.user.is_authenticated():
        if request.user.groups.filter(name__in=['PCC']).exists():
            paper = Paper.objects.filter(id=id).first()
            context.update({'paper':paper})
            notification = Notifcation.objects.filter(paper = paper).first()
            notification.read = True
            notification.save()
    return render(request, 'view_paper.html', context)


def signup(request):
    context = {}
    form = Signupform() # just showing the form to the user
    context.update({'form': form})# to render

    if request.user.is_authenticated():  #if the user assigned, dont make him access the signup link
        return HttpResponseRedirect('/')
    else:
            if request.method == 'POST':
                # create a form instance and populate it with data from the request:
                form = Signupform(request.POST) # the form with data and chech if the form is valid
                context.update({'form':form})
                # check whether it's valid:
                if form.is_valid():
                    form.save()
                    user = form.save()
                    user.groups.add(Group.objects.get(name='Author'))
                    return redirect("/")
            # if a GET (or any other method) we'll create a blank form
    return render(request, 'signup.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')