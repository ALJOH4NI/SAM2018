from django.http import HttpResponse
from django.shortcuts import render
from SAM2018.models import Paper, User, Review
from .forms import AssignForm

def index(request):
    context = {}
    papers = Paper.objects.all()
    pcm_users = User.objects.filter(groups__name='PCM')

    context.update({'papers': papers, 'evaluators': pcm_users})
    return render(request, 'pcc_dashboard_index.html', context)


def assign(request):
    if request.method == 'POST':
        form = AssignForm(request.POST)
        if form.is_valid():
            review = form.save()
            review.add()
    else:
        form = AssignForm()

    return render(request, 'pcc_dashboard_index.html')
