from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.process_registration),
    url(r'^dashboard$', views.dashboard),
    url(r'^schedule_preferences$', views.get_preferences),
    url(r'^schedule_basic_skills$', views.get_basic_skills_courses),
    url(r'^schedule_natural_sciences$', views.get_natural_sciences_courses),
    url(r'^schedule_arts_and_humanities$', views.get_arts_and_humanities_courses),
    url(r'^schedule_social_sciences$', views.get_social_sciences_courses),
    url(r'^schedule_lifelong_learning$', views.get_lifelong_learning_courses),
    url(r'^schedule_comparative_cultural_studies$', views.get_comparative_cultural_studies_courses),
    url(r'^schedule_us_history_and_government$', views.get_us_history_and_government_courses),
    url(r'^gpa$', views.gpa),
    url(r'^logout$', views.logout),
    url(r'^login$', views.process_login),
]