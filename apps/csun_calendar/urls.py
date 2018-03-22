from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process_user$', views.process_user),
    url(r'^process$', views.process_courses),
    url(r'^reset$', views.reset),

]