from django.shortcuts import render, redirect, HttpResponse
from django.db import models
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.db import models
from .models import *
import re
import bcrypt
import datetime
import time

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
STUDENT_ID_REGEX = re.compile(r'^(\d{9})$')

def index(request):
    return render(request, 'csun_calendar/index.html')

def dashboard(request):
    if 'user' in request.session:
        return render(request, 'csun_calendar/dashboard.html')
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_preferences(request):
    if 'user' in request.session:
        return render(request, 'csun_calendar/schedule_preferences.html')
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_general_courses(request):
    if 'user' in request.session:
        return render(request, 'csun_calendar/schedule_general.html')
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def gpa(request):
    pass

def process_registration(request):
    error = False
    if len(request.POST['first_name']) < 2 or len(request.POST['first_name']) < 2:
        messages.error(request, 'First and Last names must be longer than 2 characters!')
        error = True
    if not request.POST['first_name'].isalpha() or not request.POST['last_name'].isalpha():
        messages.error(request, 'First and Last must be alphabets!')
        error = True
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request, 'Please enter a valid e-mail address!')
        error = True
    emails = User.objects.filter(email = request.POST['email'])
    if emails:
        messages.error(request, 'This email is already taken!')
        error = True
    if not STUDENT_ID_REGEX.match(request.POST['student_id']):
        messages.error(request, 'Student ID must be a 9 digit number!')
        error = True
    student_ids = User.objects.filter(student_id = request.POST['student_id'])
    if student_ids:
        messages.error(request, 'This student id has already been registered!')
        error = True
    if not PASSWORD_REGEX.match(request.POST['password']):
        messages.error(request, 'Password must be 8 or more characters, contain at least 1 upper case and 1 number!')
        error = True
    if request.POST['password'] != request.POST['password_confirm']:
        messages.error(request, 'Passwords must match!')
        error = True
    if request.POST['starting_year'] < str(datetime.date.today().year):
        messages.error(request, 'Starting School Year must be this year or later!')
        error = True
    if error:
        return redirect(index)
    else: 
        User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], student_id = request.POST['student_id'], starting_year = request.POST['starting_year'], email = request.POST['email'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        session_user = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'student_id': request.POST['student_id'],
            'id': User.objects.last().id
        }
        request.session['user'] = session_user
        messages.success(request, "Thank you for registering! You will be directed to the dashboard page!")
        return redirect(dashboard)

def process_login(request):
    user = User.objects.filter(email = request.POST['email'])
    if not user:
        messages.error(request, 'Invalid Login Information!')
        return redirect(index)
    else:
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            # messages.success(request, 'Successfully Logged In!')
            # request.session['user'] = user
            session_user = {
                'first_name': user[0].first_name,
                'last_name': user[0].last_name,
                'email': user[0].email,
                'student_id': user[0].student_id,
                'id': user[0].id
            }
            request.session['user'] = session_user
            return redirect(dashboard)
        else:
            messages.error(request, 'Invalid Login Information!')
            return redirect(index)

def logout(request):
    if 'user' in request.session:
        request.session.pop('user')
        messages.success(request, 'Successfully Logged Out!')
    return redirect(index)