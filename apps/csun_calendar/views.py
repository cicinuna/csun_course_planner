from django.shortcuts import render, redirect, HttpResponse
from django.db import models
from models import *
from django.contrib import messages
import re
import bcrypt
import datetime
import time

def index(request):
    return render(request, 'csun_calendar/index.html')

def process_user(request):
    request.session['name'] = request.POST['name']
    request.session['desired_years'] = request.POST['desired_years']
    request.session['desired_units'] = request.POST['desired_units']
    return render(request, 'csun_calendar/course_catalog.html')

def process_courses(request):
    all_list = [value.split('=') for value in request.POST.getlist('elective')]
    units = 0
    for i in range(0,len(all_list)):
        units += int(all_list[i][1])
    if units < 48:
        messages.error(request, "You only chose {} units. Total elective units must add up to 48 units!".format(units))
        return render(request, 'csun_calendar/course_catalog.html')

    courses = []
    for i in range(0, len(all_list)):
        courses.append(all_list[i][0])


    if request.session['desired_units'] == '12':
        courses = [courses[i:i + 2] for i in xrange(0, len(courses), 2)]
    if request.session['desired_units'] == '15':
        courses = [courses[i:i + 3] for i in xrange(0, len(courses), 3)]
    
    print len(courses)
    content = {
        'courses': courses,
        'units': units
    }
    return render(request, 'csun_calendar/results.html', content)

def reset(request):
    if 'name' in request.session:
        request.session.pop('name')
    if 'desired_years' in request.session:
        request.session.pop('desired_years')
    if 'desired_units' in request.session:
        request.session.pop('desired_units')
    return redirect(index)