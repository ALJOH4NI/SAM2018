from django.contrib import admin

# Register your models here.


from .models import Paper, Review, Notifcation, Deadlines, Report, NotifcationTemp, Deadline

admin.site.register(Paper)
admin.site.register(Review)
admin.site.register(Notifcation)
admin.site.register(Deadline)
admin.site.register(Report)
admin.site.register(NotifcationTemp)



