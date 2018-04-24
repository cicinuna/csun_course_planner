from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.process_registration),
    url(r'^dashboard$', views.dashboard),
    url(r'^schedule_preferences$', views.get_preferences),
    url(r'^schedule_general$', views.get_general_courses),
    url(r'^gpa$', views.gpa),
    url(r'^logout$', views.logout),
    url(r'^login$', views.process_login),
]