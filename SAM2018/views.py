from django.shortcuts import render, redirect
from .forms import Signupform, UplaodFile
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import Group
from .models import Paper, Notifcation, Deadlines,Review
from django.contrib.auth.models import User
from .forms import AssignForm, DeadlineForm
from django.contrib import messages






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


    elif request.user.is_authenticated():   #PCC, Author and PCM

        if request.user.groups.filter(name__in=['PCC']).exists():
            papers = Paper.objects.all()
            pcm_users = User.objects.filter(groups__name='PCM')
            context.update({'papers': papers, 'evaluators': pcm_users})
            context.update({'is_pcc': 'is_pcc'})
            notification = Notifcation.objects.filter(read=False)
            num_notification = len(notification)
            context.update({'groups': request.user.groups.all().first(),'NumNotifications':num_notification,'notification':notification})

            if request.method == 'POST':
                paper = request.POST["paper_id"]
                pcm = request.POST.getlist('pcm_id')
                for p in pcm:
                    pcm_user = User.objects.filter(id=p).first()
                    paper1= Paper.objects.filter(id=paper).first()
                    if (Review.objects.filter(pcm=pcm_users, paper=paper1).count() == 0):
                        review = Review(paper=paper1,pcm=pcm_user)
                        review.save()

            return render(request, 'pcc_dashboard_index.html', context)

        elif request.user.is_staff:
            form = DeadlineForm(request.POST)
            if request.method == 'POST':

                if form.is_valid():
                    deadline = Deadlines(date=request.POST['date'], group=request.POST['group'])
                    deadline.save()
                else:
                    form = DeadlineForm()

            context.update({'form':form})
            return render(request, 'admin_dhasboard.html', context)



        elif request.user.groups.filter(name__in=['Author']).exists():
            paper = Paper.objects.filter(user=request.user)
            deadline = Deadlines.objects.filter(group='Author').first()

            context.update({'is_author':'is_author'})
            context.update({'deadline': deadline})
            context.update({'paper': paper})

            form = UplaodFile(request.POST, request.FILES)
            if request.method == "POST":
                form = UplaodFile(request.POST, request.FILES)
                if form.is_valid():
                    newpaper = Paper(uplaod = request.FILES['uplaod'], title = request.POST['title'], version="1", user = request.user)
                    newpaper.save()
                    messages.success(request, 'Your password was updated successfully!')
                    user = User.objects.filter(groups__name='PCC').first()
                    notification = Notifcation(user = user, paper= newpaper)
                    notification.save()
            else:
                form = UplaodFile()
            context.update({'groups': request.user.groups.all().first(), 'form':form})
            return render(request, 'author_dashboard.html', context)


        elif request.user.groups.filter(name__in=['PCM']).exists():
            paper = Paper.objects.filter(user=request.user)
            deadline = Deadlines.objects.filter(group='PCM').first()
            reviews = Review.objects.filter(pcm=request.user)

            context.update({'is_pcm':'is_pcm'})
            context.update({'deadline': deadline})
            context.update({'reviews': reviews})
            context.update({'paper': paper})

            form = UplaodFile(request.POST, request.FILES)
            if request.method == "POST":
                form = UplaodFile(request.POST, request.FILES)
                if form.is_valid():
                    newpaper = Paper(uplaod = request.FILES['uplaod'], title = request.POST['title'], version="1", user = request.user)
                    newpaper.save()
                    messages.success(request, 'Your password was updated successfully!')
                    user = User.objects.filter(groups__name='PCC').first()
                    notification = Notifcation(user = user, paper= newpaper)
                    notification.save()
            else:
                form = UplaodFile()
            context.update({'groups': request.user.groups.all().first(), 'form':form})
            return render(request, 'pcm_dashboard.html', context)
    return render(request, 'login.html', context)






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





def assign(request):
    if request.method == 'POST':
        form = AssignForm(request.POST)
        if form.is_valid():
            review = form.save()
            review.add()
    else:
        form = AssignForm()

    return render(request, 'pcc_dashboard_index.html')






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