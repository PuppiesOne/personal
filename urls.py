from django.conf.urls import patterns, include, url
from Codify import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^Codify/jobcall$', views.jobcall, name='jobcall'),
                       url(r'^Codify/CAupload$', views.upload_file, name='CAupload'),
                       )