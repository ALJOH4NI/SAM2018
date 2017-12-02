
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from SAM2018 import views, cPanel
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^$', views.index, name='index'),
                  url(r'^logout/$', auth_views.logout,{'next_page': 'index'}, name='logout'),
                  url(r'^signup', views.signup, name='signup'),
                  url(r'^paper/(?P<id>\d+)/$', views.view_paper, name='view_paper_url'),
                  url(r'^view_reviewed_papers/$', views.view_reviewed_papers, name='view_reviewed_papers'),
                  url(r'^view_reports/$', views.view_reports, name='view_reports'),
                  url(r'^generate_report/(?P<paper_id>\d+)/$', views.generate_report, name='generate_report'),
                  url(r'^cpanel', cPanel.admin),
                          url(r'^userMangament', cPanel.userMangament)
                        ,  url(r'^deadlines', cPanel.deadlines)
                        ,  url(r'^notifications', cPanel.notifications),
                             url(r'^templates', cPanel.templates),
                            url(r'^upadtaUser', cPanel.updateUser),
                             url(r'^deleteUser', cPanel.deleteUser),
                             url(r'^addNewUser', cPanel.addNewUser),
                            url(r'^configsDeadLine', cPanel.configsDeadLine)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
