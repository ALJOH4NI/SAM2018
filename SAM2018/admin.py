from django.contrib import admin

# Register your models here.


from .models import Paper, Review, Notifcation, Deadlines

admin.site.register(Paper)
admin.site.register(Review)
admin.site.register(Notifcation)
admin.site.register(Deadlines)

