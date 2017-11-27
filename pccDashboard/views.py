from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>PCC DASHBOARD</h1>")