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
import requests
from urllib.request import urlopen
import json

def fetch_data(url):
    #try to read the data	
    try:
        u = urlopen(url)
        data = u.read()
    except Exception as e:
        data = {}

    #decode into an array
    data = json.loads(data)

    #setup a blank array
    course_list = []

    #loop through results and add each course's subject
    #and catalog number to course_list array (i.e COMP 100)
    for course in data['courses']:
        item = {
            'subject': course['subject'],
            'catalog_number': course['catalog_number'],
            'title': course['title'],
            'description': course['description'],
            'units': course['units'],
        }
        course_list.append(item)

    return course_list

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
STUDENT_ID_REGEX = re.compile(r'^(\d{9})$')
AAS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/aas'
AFRS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/afrs'
CAS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/cas'
CHS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/chs'
ENGL_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/engl'
LING_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/ling'
QS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/qs'
COMS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/coms'
PHIL_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/phil'
RS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/rs'
MATH_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/math'
ASTR_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/astr'
BIOL_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/biol'
CHEM_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/chem'
GEOG_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/geog'
GEOL_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/geol'
PHYS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/phys'
SCI_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/sci'
SUST_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/sust'
ANTH_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/anth'
ART_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/art'
CLAS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/clas'
CTVA_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/ctva'
FLIT_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/flit'
GWS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/gws'
HIST_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/hist'
HUM_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/hum'
JS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/js'
KIN_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/kin'
MUS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/mus'
TH_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/th'
AIS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/ais'
CADV_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/cadv'
ECON_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/econ'
HHD_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/hhd'
HSCI_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/hsci'
MKT_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/mkt'
POLS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/pols'
PSY_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/psy'
SOC_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/soc'
URBS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/urbs'
BLAW_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/blaw'
BUS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/bus'
CCE_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/cce'
CD_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/cd'
CJS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/cjs'
CM_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/cm'
COMP_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/comp'
EOH_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/eoh'
FCS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/fcs'
FIN_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/fin'
JOUR_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/jour'
MSE_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/mse'
RTM_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/rtm'
UNIV_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/univ'
ARAB_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/arab'
ARMN_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/armn'
CHIN_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/chin'
FREN_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/fren'
HEBR_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/hebr'
ITAL_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/ital'
JAPN_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/japn'
KOR_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/kor'
PERS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/pers'
RUSS_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/russ'
SPAN_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/span'
SPED_URL = u'https://api.metalab.csun.edu/curriculum/api/2.0/courses/sped'

aas_data = fetch_data(AAS_URL)
afrs_data = fetch_data(AFRS_URL)
cas_data = fetch_data(CAS_URL)
chs_data = fetch_data(CHS_URL)
engl_data = fetch_data(ENGL_URL)
ling_data = fetch_data(LING_URL)
qs_data = fetch_data(QS_URL)
coms_data = fetch_data(COMS_URL)
phil_data = fetch_data(PHIL_URL)
rs_data = fetch_data(RS_URL)
math_data = fetch_data(MATH_URL)
astr_data = fetch_data(ASTR_URL)
biol_data = fetch_data(BIOL_URL)
chem_data = fetch_data(CHEM_URL)
geog_data = fetch_data(GEOG_URL)
geol_data = fetch_data(GEOL_URL)
phys_data = fetch_data(PHYS_URL)
sci_data = fetch_data(SCI_URL)
sust_data = fetch_data(SUST_URL)
anth_data = fetch_data(ANTH_URL)
art_data = fetch_data(ART_URL)
clas_data = fetch_data(CLAS_URL)
ctva_data = fetch_data(CTVA_URL)
flit_data = fetch_data(FLIT_URL)
gws_data = fetch_data(GWS_URL)
hist_data = fetch_data(HIST_URL)
hum_data = fetch_data(HUM_URL)
js_data = fetch_data(JS_URL)
kin_data = fetch_data(KIN_URL)
mus_data = fetch_data(MUS_URL)
th_data = fetch_data(TH_URL)
ais_data = fetch_data(AIS_URL)
cadv_data = fetch_data(CADV_URL)
econ_data = fetch_data(ECON_URL)
hhd_data = fetch_data(HHD_URL)
hsci_data = fetch_data(HSCI_URL)
mkt_data = fetch_data(MKT_URL)
pols_data = fetch_data(POLS_URL)
psy_data = fetch_data(PSY_URL)
soc_data = fetch_data(SOC_URL)
urbs_data = fetch_data(URBS_URL)
blaw_data = fetch_data(BLAW_URL)
bus_data = fetch_data(BUS_URL)
cce_data = fetch_data(CCE_URL)
cd_data = fetch_data(CD_URL)
cjs_data = fetch_data(CJS_URL)
cm_data = fetch_data(CM_URL)
comp_data = fetch_data(COMP_URL)
eoh_data = fetch_data(EOH_URL)
fcs_data = fetch_data(FCS_URL)
fin_data = fetch_data(FIN_URL)
jour_data = fetch_data(JOUR_URL)
mse_data = fetch_data(MSE_URL)
rtm_data = fetch_data(RTM_URL)
univ_data = fetch_data(UNIV_URL)
arab_data = fetch_data(ARAB_URL)
armn_data = fetch_data(ARMN_URL)
chin_data = fetch_data(CHIN_URL)
fren_data = fetch_data(FREN_URL)
hebr_data = fetch_data(HEBR_URL)
ital_data = fetch_data(ITAL_URL)
japn_data = fetch_data(JAPN_URL)
kor_data = fetch_data(KOR_URL)
pers_data = fetch_data(PERS_URL)
russ_data = fetch_data(RUSS_URL)
span_data = fetch_data(SPAN_URL)
sped_data = fetch_data(SPED_URL)


def index(request):
    return render(request, 'csun_calendar/index.html')

def dashboard(request):
    if 'user' in request.session:
        return render(request, 'csun_calendar/dashboard.html', {"aas_data": aas_data})
        # {"data": data}
        # {"data": data}
        # {"data": data}
        # 이렇게 보내기
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_preferences(request):
    if 'user' in request.session:
        return render(request, 'csun_calendar/schedule_preferences.html')
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_basic_skills_courses(request):
    if 'user' in request.session:
        return render(request, 'csun_calendar/schedule_basic_skills.html')
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_natural_sciences_courses(request):
    if 'user' in request.session:
        return render(request, 'csun_calendar/schedule_natural_sciences.html')
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_arts_and_humanities_courses(request):
    if 'user' in request.session:
        return render(request, 'csun_calendar/schedule_arts_and_humanities.html')
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_social_sciences_courses(request):
    if 'user' in request.session:
        return render(request, 'csun_calendar/schedule_social_sciences.html')
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_lifelong_learning_courses(request):
    if 'user' in request.session:
        return render(request, 'csun_calendar/schedule_lifelong_learning.html')
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_comparative_cultural_studies_courses(request):
    if 'user' in request.session:
        return render(request, 'csun_calendar/schedule_comparative_cultural_studies.html')
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_us_history_and_government_courses(request):
    if 'user' in request.session:
        return render(request, 'csun_calendar/schedule_us_history_and_government.html')
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

