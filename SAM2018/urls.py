
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from SAM2018 import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^$', views.index, name='index'),
                  url(r'^logout/$', auth_views.logout,{'next_page': 'index'}, name='logout'),
                  url(r'^signup', views.signup, name='signup'),
                  url(r'^paper/(?P<id>\d+)/$', views.view_paper, name='view_paper_url'),
                  url(r'^pcc/', include('pccDashboard.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
