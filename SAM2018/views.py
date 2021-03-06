import sys
from django.db.models import Count
from django.shortcuts import render, render_to_response, redirect

from SAM2018 import cPanel, notification
from SAM2018.cPanel import notifications
from SAM2018.observer import Observer
from .forms import Signupform, UplaodFile
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect, Http404, request
from django.contrib.auth.models import Group

from .models import Paper, Notifcation, Deadlines, Review, Report, Deadline, favoritePaper, NotifcationTemp,Template
from django.contrib.auth.models import User
from .forms import AssignForm, DeadlineForm
from django.contrib import messages
import datetime
from observable import Observable

class view(Observer):

    def update(self, *args, **kwargs):
        print("")


def index(request):
    Observable.SAMObservable.update_observers('admin', something='update data base')

    id = request.GET.get('notificationChangeStatus')
    if id:
        Notifcation.objects.all().filter(id=id).update(read=True)
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
            if request.method == 'POST':
                paper_id = request.POST["paper_id"]
                pcms = request.POST.getlist('pcm_list')
                paper = Paper.objects.filter(id=paper_id).first()
                for item in pcms:
                    pcm_user = User.objects.filter(id=item).first()
                    if Review.objects.filter(pcm=pcm_user, paper=paper).count() == 0:
                        review = Review(paper=paper, pcm=pcm_user)
                        review.save()
                        notiftemp = NotifcationTemp.objects.all().filter(nameID="assigned_paper").first()
                        notification = Notifcation(user=pcm_user,
                                                   reviewedPaper=Review.objects.all().filter(paper=paper).first().id,
                                                   notiftemp=notiftemp)
                        notification.save()
                messages.success(request, 'The paper has been assign successfully!')

            reviews = Review.objects.all()
            pcm_users = User.objects.filter(groups__name='PCM')
            papers = Paper.objects.all().exclude(id__in=[x.paper.id for x in reviews])
            context.update({'papers': papers,
                            'evaluators': pcm_users ,'favoritePaper': favoritePaper.objects.all()})
            context.update({'is_pcc': 'is_pcc'})
            context.update({'userData': request.user})
            context.update({'role': 'PCC'})


            context.update({'groups': request.user.groups.all().first()})


            return render(request, 'pcc_dashboard_index.html', context)

        # Admin login
        elif request.user.is_staff:


            return HttpResponseRedirect("cpanel")

        elif request.user.groups.filter(name__in=['Author']).exists():
            paper_submissionData = Deadline.objects.all().filter(nameID='paper_submission').first().date
            currentDate = datetime.datetime.now()
            objectDatetime = datetime.datetime.strptime(paper_submissionData, "%Y-%m-%d")
            paper = Paper.objects.filter(user=request.user)
            context.update({'paper': paper})
            context.update({'userData': request.user})

            context.update({'is_author': 'is_author'})
            context.update({'groups': request.user.groups.all().first()})
            if request.GET.get('submittedPaper'):
                context.update({'submittedPaper': 'true'})

            if request.GET.get('paperUploaded'):
                context.update({'uploaded': 'uploaded'})

            if currentDate.date() < objectDatetime.date():
                context.update({'allowed': '-'})
                form = UplaodFile(request.POST, request.FILES)
                if request.method == "POST":
                    form = UplaodFile(request.POST, request.FILES)
                    if form.is_valid():
                        newpaper = Paper(uplaod=request.FILES['uplaod'], title=request.POST['title'], version=request.POST['version'],
                                         authorName=request.POST['authorName'], contact=request.POST['contact']  ,user=request.user)
                        newpaper.save()
                        PCCuser = User.objects.filter(groups__name='PCC').first()
                        notiftemp = NotifcationTemp.objects.all().filter(nameID="paper_submission").first()
                        Notifcation(user=PCCuser, paper=newpaper,notiftemp=notiftemp).save()

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
            reviews = Review.objects.filter(pcm=request.user).filter(rate__isnull=True)

            context.update({'is_pcm': 'is_pcm'})
            context.update({'deadline': deadline})
            context.update({'reviews': reviews})
            context.update({'papers': Paper.objects.all()})
            context.update({'userData': request.user})

            context.update({'selectedPaper': favoritePaper.objects.all().filter(pcm=request.user)})

            if request.GET.get('SubmitPaper'):
                context.update({"SubmitPaper": "true"})




            form = UplaodFile(request.POST, request.FILES)
            if request.method == "POST":


                if request.POST['paper_id']:
                    for item in request.POST.getlist('paper_id'):
                        paper = Paper.objects.all().filter(pk=item).first()
                        pcm = request.user
                        favoritePaper(pcm=pcm, papers=paper).save()


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
#
# def view_submitted_papers(request):
#     context = {}
#     if request.user.is_authenticated():
#         if request.user.groups.filter(name__in=['PCM']).exists():
#             paper = Paper.objects.filter(id=id).first()
#             context.update({'paper_submitted': paper})
#     return render(request, 'pcm_dashboard.html', context)



def view_paper(request, id):
    context = {}
    if request.user.is_authenticated():
       paper = Paper.objects.filter(id=id).first()

       if paper:

            context.update({'paper': paper})

            if request.user.groups.filter(name__in=['PCC']).exists():

                 context.update({'role': 'PCC'})
            elif request.user.groups.filter(name__in=['PCM']).exists():
                context.update({'role': 'PCM'})

    return render(request, 'view_paper.html', context)


def view_reports(request):
    context = {}
    if request.user.is_authenticated():
        if request.user.groups.filter(name__in=['PCC']).exists():
            reports = Report.objects.all()
            context.update({'reports': reports})
    return render(request, 'view_reports.html', context)


def view_reviewed_papers(request):
    context = {}
    if request.user.is_authenticated():
        if request.user.groups.filter(name__in=['PCC']).exists():
            data = []
            for paper in Paper.objects.all():
                reviews = []
                review_items = Review.objects.filter(paper=paper, rate__isnull=False)
                for review in review_items:
                    reviews.append(review)



                if len(review_items) == 3:
                    data.append({'paper': paper, 'reviews': reviews})

            context.update({'paper_reviews': data})
    return render(request, 'view_reviewed_papers.html', context)


def generate_report(request, paper_id):
    context = {}
    if request.user.is_authenticated():
        if request.user.groups.filter(name__in=['PCC']).exists():
            if request.method == 'POST':
                paper = Paper.objects.filter(id=paper_id).first()
                rating = request.POST["rating"]
                comment = request.POST["comment"]
                report = Report(comments=comment, rate=rating, paper=paper)
                report.save()
                for review in Review.objects.filter(paper=paper):
                    review.report = report
                    review.save()

                message = NotifcationTemp.objects.all().filter(nameID="ReportIsGenerated").first()

                Notifcation(user=paper.user, notiftemp=message).save()

                messages.success(request, 'The report has been saved successfully!')
                return redirect('index')

            paper = Paper.objects.filter(id=paper_id).first()
            reviews = []
            for review in Review.objects.filter(paper=paper):
                reviews.append(review)

            context.update({'paper': paper, 'reviews': reviews})
            context.update({'ReportTemp': Template.objects.all().filter(nameID="Report").first()})


    return render(request, 'generate_report.html', context)


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


def reviewPaper(request):
    context = {}
    id = request.GET.get('id')
    if request.method == 'POST':
        paper = Paper.objects.filter(pk=request.POST["id"]).first()
        rating = request.POST["rating"]
        comment = request.POST["comment"]
        Review.objects.all().filter(paper=paper,pcm=request.user).update(comment=comment, rate=rating)
        PCMuser = User.objects.filter(groups__name='PCC').first()
        notiftemp1 = NotifcationTemp.objects.all().filter(nameID="assigned_paper").first()
        Notifcation.objects.all().filter(user=request.user, reviewedPaper=Review.objects.all().filter(paper=paper).first().id,
                                   notiftemp=notiftemp1).update(read=True)

        notiftemp = NotifcationTemp.objects.all().filter(nameID="paper_review").first()
        notification = Notifcation(user=PCMuser, reviewedPaper=Review.objects.all().filter(paper=paper).first().id,
                                   notiftemp=notiftemp)
        notification.save()

        if len(Review.objects.all().filter(paper=paper,rate__isnull=False)) == 3:
            message = NotifcationTemp.objects.all().filter(nameID="ThreeReviewCompleted").first()
            if not Notifcation.objects.all().filter(notiftemp=message).filter(AllReviewPaper=paper.id).first():
                Notifcation(AllReviewPaper=paper.id, notiftemp=message, user=PCMuser).save()


        return redirect("/")
    if id:
       context = {"paper":Paper.objects.all().filter(pk=id).first()}
       context.update({'ReviewTemp': Template.objects.all().filter(nameID="Review").first()})

    return render(request, 'pcm_review_papers.html', context)


