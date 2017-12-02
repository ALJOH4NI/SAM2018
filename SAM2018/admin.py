from django.contrib import admin

# Register your models here.


from .models import Paper, Review, Notifcation, Deadlines, Report

admin.site.register(Paper)
admin.site.register(Review)
admin.site.register(Notifcation)
admin.site.register(Deadlines)
admin.site.register(Report)

