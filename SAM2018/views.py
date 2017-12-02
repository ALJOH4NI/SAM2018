from django.shortcuts import render, render_to_response, redirect
from .forms import Signupform, UplaodFile
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import Group
from .models import Paper, Notifcation, Deadlines, Review, Deadline
from django.contrib.auth.models import User
from .forms import AssignForm, DeadlineForm
from django.contrib import messages
import datetime



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

    elif request.user.is_authenticated():  # PCC, Author and PCM
        if request.user.groups.filter(name__in=['PCC']).exists():
            pcm_users = User.objects.filter(groups__name='PCM')

            if request.method == 'POST':
                paper_id = request.POST["paper_id"]
                pcms = request.POST.getlist('pcm_list')
                paper = Paper.objects.filter(id=paper_id).first()
                for item in pcms:
                    pcm_user = User.objects.filter(id=item).first()
                    if Review.objects.filter(pcm=pcm_users, paper=paper).count() == 0:
                        review = Review(paper=paper, pcm=pcm_user)
                        review.save()
                messages.success(request, 'The paper has been assign successfully!')

            reviews = Review.objects.all()
            papers = Paper.objects.all().exclude(id__in=[x.paper.id for x in reviews])
            context.update({'papers': papers,
                            'evaluators': pcm_users})
            context.update({'is_pcc': 'is_pcc'})
            notification = Notifcation.objects.filter(read=False)
            num_notification = len(notification)
            context.update({'groups': request.user.groups.all().first(), 'NumNotifications': num_notification,
                            'notification': notification})

            return render(request, 'pcc_dashboard_index.html', context)

        # Admin login
        elif request.user.is_staff:
            form = DeadlineForm(request.POST)
            if request.method == 'POST':

                if form.is_valid():
                    deadline = Deadlines(date=request.POST['date'], group=request.POST['group'])
                    deadline.save()
                else:
                    form = DeadlineForm()

            context.update({'form': form})
            return render(request, 'admin_dhasboard.html', context)

        elif request.user.groups.filter(name__in=['Author']).exists():
            paper_submissionData = Deadline.objects.all().filter(nameID='paper_submission').first().date
            currentDate = datetime.datetime.now()
            objectDatetime = datetime.datetime.strptime(paper_submissionData, "%Y-%m-%d")
            paper = Paper.objects.filter(user=request.user)
            context.update({'paper': paper})
            context.update({'is_author': 'is_author'})
            context.update({'groups': request.user.groups.all().first()})

            if request.GET.get('paperUploaded'):
                context.update({'uploaded': 'uploaded'})

            if currentDate.date() < objectDatetime.date():
                context.update({'allowed': '-'})
                form = UplaodFile(request.POST, request.FILES)
                if request.method == "POST":
                    form = UplaodFile(request.POST, request.FILES)
                    if form.is_valid():
                        newpaper = Paper(uplaod=request.FILES['uplaod'], title=request.POST['title'], version="1",
                                         user=request.user)
                        newpaper.save()
                        user = User.objects.filter(groups__name='PCC').first()
                        notification = Notifcation(user=user, paper=newpaper)
                        notification.save()
                        context.update({'uploaded': 'uploaded'})
                        return redirect('/?paperUploaded="true"')
                else:
                    form = UplaodFile()
                    context.update({'form': form})


            return render(request, 'author_dashboard.html', context)


        # PCM dashboard
        elif request.user.groups.filter(name__in=['PCM']).exists():
            paper = Paper.objects.filter(user=request.user)
            deadline = Deadlines.objects.filter(group='PCM').first()
            reviews = Review.objects.filter(pcm=request.user)

            context.update({'is_pcm': 'is_pcm'})
            context.update({'deadline': deadline})
            context.update({'reviews': reviews})
            context.update({'paper': paper})

            form = UplaodFile(request.POST, request.FILES)
            if request.method == "POST":
                form = UplaodFile(request.POST, request.FILES)
                if form.is_valid():
                    newpaper = Paper(uplaod=request.FILES['uplaod'], title=request.POST['title'], version="1",
                                     user=request.user)
                    newpaper.save()
                    messages.success(request, 'Your password was updated successfully!')
                    user = User.objects.filter(groups__name='PCC').first()
                    notification = Notifcation(user=user, paper=newpaper)
                    notification.save()
            else:
                form = UplaodFile()
            context.update({'groups': request.user.groups.all().first(), 'form': form})
            return render(request, 'pcm_dashboard.html', context)
    return render(request, 'login.html', context)



def view_paper(request, id):
    context = {}
    if request.user.is_authenticated():
        if request.user.groups.filter(name__in=['PCC']).exists():
            paper = Paper.objects.filter(id=id).first()
            context.update({'paper': paper})
            notification = Notifcation.objects.filter(paper=paper).first()
            notification.read = True
            notification.save()
    return render(request, 'view_paper.html', context)


def view_reviewed_papers(request):
    context = {}
    if request.user.is_authenticated():
        if request.user.groups.filter(name__in=['PCC']).exists():
            paper = Paper.objects.filter(id=id).first()
            context.update({'paper_reviews': paper})
    return render(request, 'view_reviewed_papers.html', context)


def signup(request):
    context = {}
    form = Signupform()  # just showing the form to the user
    context.update({'form': form})  # to render
    if request.user.is_authenticated():  # if the user assigned, don't make him access the signup link
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
                    messages.success(request, 'successfully!')
                    user.groups.add(Group.objects.get(name='Author'))
                    return redirect("/")
            # if a GET (or any other method) we'll create a blank form
    return render(request, 'signup.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
