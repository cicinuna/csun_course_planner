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
from urllib.request import urlopen
import json
import ast
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def fetch_data(url):
    #try to read the data	
    try:
        u = urlopen(url, context = ctx)
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

def strip_description(courses):
    for things in courses:
        try: 
            desc = things['description']
            try:
                pre = re.search(r'Prerequisite.[\w \/]*', desc).group(0)
            except AttributeError:
                pre = 'No Prerequisite'
            try:
                pres = re.search(r'Prerequisites.[\w \/\;]*', desc).group(0)
            except AttributeError:
                pres = 'No Prerequisites'
            try:
                core = re.search(r'Corequisite.[\w \/]*', desc).group(0)
            except AttributeError:
                core = 'No Corequisite.'
            try:
                prep = re.search(r'Preparatory.[\w \/]*', desc).group(0)
            except AttributeError:
                prep = 'No Preparatory.'
        except TypeError:
            continue
        things['description'] = pre + ". " + pres + ". " + core + " " + prep
    return courses

def get_dict(li):
    d_li = []
    for t in li:
        d_li.append(ast.literal_eval(t))
    return d_li

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
STUDENT_ID_REGEX = re.compile(r'^(\d{9})$')
AAS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/aas'
AFRS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/afrs'
CAS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/cas'
CHS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/chs'
ENGL_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/engl'
LING_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/ling'
QS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/qs'
COMS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/coms'
PHIL_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/phil'
RS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/rs'
ASTR_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/astr'
BIOL_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/biol'
MATH_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/math'
CHEM_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/chem'
GEOG_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/geog'
GEOL_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/geol'
PHYS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/phys'
SCI_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/sci'
SUST_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/sust'
ANTH_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/anth'
ART_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/art'
CLAS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/clas'
CTVA_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/ctva'
FLIT_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/flit'
GWS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/gws'
HIST_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/hist'
HUM_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/hum'
JS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/js'
KIN_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/kin'
MUS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/mus'
TH_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/th'
AIS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/ais'
CADV_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/cadv'
ECON_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/econ'
HHD_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/hhd'
HSCI_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/hsci'
MKT_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/mkt'
POLS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/pols'
PSY_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/psy'
SOC_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/soc'
URBS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/urbs'
BLAW_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/blaw'
BUS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/bus'
CCE_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/cce'
CD_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/cd'
CJS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/cjs'
CM_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/cm'
EOH_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/eoh'
COMP_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/comp'
FCS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/fcs'
FIN_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/fin'
JOUR_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/jour'
MSE_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/mse'
RTM_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/rtm'
UNIV_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/univ'
ARAB_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/arab'
ARMN_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/armn'
CHIN_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/chin'
FREN_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/fren'
HEBR_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/hebr'
ITAL_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/ital'
JAPN_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/japn'
KOR_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/kor'
PERS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/pers'
RUSS_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/russ'
SPAN_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/span'
SPED_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/fall-'+str(datetime.datetime.now().year-1)+'/courses/sped'
COMP_SP_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/spring-'+str(datetime.datetime.now().year-1)+'/courses/sped'
COMP_SU_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/summer-'+str(datetime.datetime.now().year-1)+'/courses/sped'
MATH_SP_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/spring-'+str(datetime.datetime.now().year-1)+'/courses/sped'
MATH_SU_URL = u'http://api.metalab.csun.edu/curriculum/api/2.0/terms/summer-'+str(datetime.datetime.now().year-1)+'/courses/sped'

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
comp_sp_data = fetch_data(COMP_SP_URL)
comp_su_data = fetch_data(COMP_SU_URL)
math_sp_data = fetch_data(MATH_SP_URL)
math_su_data = fetch_data(MATH_SU_URL)

strip_description(aas_data)
strip_description(afrs_data)
strip_description(cas_data)
strip_description(chs_data)
strip_description(engl_data)
strip_description(ling_data)
strip_description(qs_data)
strip_description(coms_data)
strip_description(phil_data)
strip_description(rs_data)
strip_description(math_data)
strip_description(astr_data)
strip_description(biol_data)
strip_description(chem_data)
strip_description(geog_data)
strip_description(geol_data)
strip_description(phys_data)
strip_description(sci_data)
strip_description(sust_data)
strip_description(anth_data)
strip_description(art_data)
strip_description(clas_data)
strip_description(ctva_data)
strip_description(flit_data)
strip_description(gws_data)
strip_description(hist_data)
strip_description(hum_data)
strip_description(js_data)
strip_description(kin_data)
strip_description(mus_data)
strip_description(th_data)
strip_description(ais_data)
strip_description(cadv_data)
strip_description(econ_data)
strip_description(hhd_data)
strip_description(hsci_data)
strip_description(mkt_data)
strip_description(pols_data)
strip_description(psy_data)
strip_description(soc_data)
strip_description(urbs_data)
strip_description(blaw_data)
strip_description(bus_data)
strip_description(cce_data)
strip_description(cd_data)
strip_description(cjs_data)
strip_description(cm_data)
strip_description(comp_data)
strip_description(eoh_data)
strip_description(fcs_data)
strip_description(fin_data)
strip_description(jour_data)
strip_description(mse_data)
strip_description(rtm_data)
strip_description(univ_data)
strip_description(arab_data)
strip_description(armn_data)
strip_description(chin_data)
strip_description(fren_data)
strip_description(hebr_data)
strip_description(ital_data)
strip_description(japn_data)
strip_description(kor_data)
strip_description(pers_data)
strip_description(russ_data)
strip_description(span_data)
strip_description(sped_data)
strip_description(comp_sp_data)
strip_description(comp_su_data)
strip_description(math_sp_data)
strip_description(math_su_data)

def specific_majors_data(classes, c_num):
    for c in classes:
        if c['catalog_number'] == c_num:
            return c
    return {}


def get_majors(comps, maths):

    # comps_fa = comps_fa.extend(comps_sp for comps_sp in comps_sp if comps_sp not in comps_fa)
    # comps_fa = comps_fa.extend(comps_su for comps_su in comps_su if comps_su not in comps_fa)
    # maths_fa = maths_fa.extend(maths_sp for maths_sp in maths_sp if maths_sp not in maths_fa)
    # maths_fa = maths_fa.extend(maths_su for maths_su in maths_su if maths_su not in maths_fa)

    # print(comps_fa)
    # print(maths_fa)

    major_list = []

    for course in comps:
        if course['catalog_number'] == '108' or course['catalog_number'] == '110' or course['catalog_number'] == '110L' or course['catalog_number'] == '182' or course['catalog_number'] == '182L' or course['catalog_number'] == '282' or course['catalog_number'] == '122' or course['catalog_number'] == '122L' or course['catalog_number'] == '380' or course['catalog_number'] == '380L' or course['catalog_number'] == '490' or course['catalog_number'] == '490L' or course['catalog_number'] == '491' or course['catalog_number'] == '491L' or course['catalog_number'] == '333' or course['catalog_number'] == '310' or course['catalog_number'] == '322' or course['catalog_number'] == '322L' or course['catalog_number'] == '256' or course['catalog_number'] == '256L' or course['catalog_number'] == '222' or course['catalog_number'] == '482':
            major_list.append(course)
    for m in maths:
        if m['catalog_number'] == '102' or m['catalog_number'] == '105' or m['catalog_number'] == '150A' or m['catalog_number'] == '150B' or m['catalog_number'] == '262' or m['catalog_number'] == '482' or m['catalog_number'] == '340' or m['catalog_number'] == '341':
            major_list.append(m)
    return major_list

def get_major_electives(comps):
    elective_list = []
    for c in comps:
        if c['catalog_number'] == '410' or c['catalog_number'] == '424' or c['catalog_number'] == '426' or c['catalog_number'] == '429' or c['catalog_number'] == '440' or c['catalog_number'] == '465' or c['catalog_number'] == '465L' or c['catalog_number'] == '467' or c['catalog_number'] == '469' or c['catalog_number'] == '482' or c['catalog_number'] == '484' or c['catalog_number'] == '484L' or c['catalog_number'] == '485' or c['catalog_number'] == '541' or c['catalog_number'] == '560' or c['catalog_number'] == '565' or c['catalog_number'] == '581' or c['catalog_number'] == '582' or c['catalog_number'] == '583' or c['catalog_number'] == '584' or c['catalog_number'] == '585' or c['catalog_number'] == '586' or c['catalog_number'] == '587' or c['catalog_number'] == '589' or c['catalog_number'] == '595' or c['catalog_number'] == '598' or c['catalog_number'] == '610' or c['catalog_number'] == '615' or c['catalog_number'] == '620' or c['catalog_number'] == '630' or c['catalog_number'] == '680' or c['catalog_number'] == '684' or c['catalog_number'] == '695' or c['catalog_number'] == '696' or c['catalog_number'] == '698' or c['catalog_number'] == '699':
            elective_list.append(c)
    return elective_list

def index(request):
    return render(request, 'csun_calendar/index.html')

def dashboard(request):
    if 'user' in request.session:
        user = User.objects.filter(id = request.session['user']['id']).first()
        schedule = Schedule.objects.filter(user_id = user).first()
        schedule.year_one_semester_one = get_dict(schedule.year_one_semester_one)
        schedule.year_one_semester_two = get_dict(schedule.year_one_semester_two)
        schedule.year_one_summer = get_dict(schedule.year_one_summer)
        schedule.year_two_semester_one = get_dict(schedule.year_two_semester_one)
        schedule.year_two_semester_two = get_dict(schedule.year_two_semester_two)
        schedule.year_two_summer = get_dict(schedule.year_two_summer)
        schedule.year_three_semester_one = get_dict(schedule.year_three_semester_one)
        schedule.year_three_semester_two = get_dict(schedule.year_three_semester_two)
        schedule.year_three_summer = get_dict(schedule.year_three_summer)
        schedule.year_four_semester_one = get_dict(schedule.year_four_semester_one)
        schedule.year_four_semester_two = get_dict(schedule.year_four_semester_two)
        schedule.year_four_summer = get_dict(schedule.year_four_summer)
        content = {
            'y1_s1': schedule.year_one_semester_one,
            'y1_s2': schedule.year_one_semester_two,
            'y1_summer': schedule.year_one_summer,
            'y2_s1': schedule.year_two_semester_one,
            'y2_s2': schedule.year_two_semester_two,
            'y2_summer': schedule.year_two_summer,
            'y3_s1': schedule.year_three_semester_one,
            'y3_s2': schedule.year_three_semester_two,
            'y3_summer': schedule.year_three_summer,
            'y4_s1': schedule.year_four_semester_one,
            'y4_s2': schedule.year_four_semester_two,
            'y4_summer': schedule.year_four_summer,
            'y': user.starting_year
        }
        return render(request, 'csun_calendar/dashboard.html', content)
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_preferences(request):
    if 'user' in request.session:
        u = User.objects.filter(id = request.session['user']['id']).first()
        schedule = Schedule.objects.filter(user_id = u).first()
        schedule.year_one_semester_one = get_dict(schedule.year_one_semester_one)
        schedule.year_one_semester_two = get_dict(schedule.year_one_semester_two)
        schedule.year_one_summer = get_dict(schedule.year_one_summer)
        schedule.year_two_semester_one = get_dict(schedule.year_two_semester_one)
        schedule.year_two_semester_two = get_dict(schedule.year_two_semester_two)
        schedule.year_two_summer = get_dict(schedule.year_two_summer)
        schedule.year_three_semester_one = get_dict(schedule.year_three_semester_one)
        schedule.year_three_semester_two = get_dict(schedule.year_three_semester_two)
        schedule.year_three_summer = get_dict(schedule.year_three_summer)
        schedule.year_four_semester_one = get_dict(schedule.year_four_semester_one)
        schedule.year_four_semester_two = get_dict(schedule.year_four_semester_two)
        schedule.year_four_summer = get_dict(schedule.year_four_summer)

        schedules = [schedule.year_one_semester_one, schedule.year_one_semester_two, schedule.year_one_summer, schedule.year_two_semester_one, schedule.year_two_semester_two, schedule.year_two_summer, schedule.year_three_semester_one, schedule.year_three_semester_two, schedule.year_three_summer, schedule.year_four_semester_one, schedule.year_four_semester_two, schedule.year_four_summer]
        for s in schedules:
            s.clear()
        
        schedule.save()
        return render(request, 'csun_calendar/schedule_preferences.html')
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_basic_skills_courses(request):
    if 'user' in request.session:
        user = User.objects.filter(id = request.session['user']['id']).update(general_elective_preference = request.POST.getlist('general_elective_preference'))
        p = User.objects.filter(id = request.session['user']['id']).values_list('general_elective_preference', flat = True)
        request.session['user']['ge_prefs'] = p[0]
        request.session.modified = True
        content = {
            "aas_data": aas_data,
            "afrs_data": afrs_data,
            "cas_data": cas_data,
            "chs_data": chs_data,
            "engl_data": engl_data,
            "ling_data": ling_data,
            "qs_data": qs_data,
            "coms_data": coms_data,
            "phil_data": phil_data,
            "rs_data": rs_data,
            "math_data": math_data,
        }
        return render(request, 'csun_calendar/schedule_basic_skills.html', content)
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_natural_sciences_courses(request):
    if 'user' in request.session:
        # for t in request.POST.getlist('general_list'):
        #     request.session['user']['ge_list'].append(t)
        # request.session['user']['ge_list'].append(request.POST.getlist('general_list'))
        # f = [item for sublist in request.session['user']['ge_list'] for item in sublist]
        # print(json.loads(str(f)))
        for t in request.POST.getlist('general_list'):
            request.session['user']['ge_list'].append((ast.literal_eval(t)))
            request.session.modified = True
        content = {
            "astr_data": astr_data,
            "biol_data": biol_data,
            "chem_data": chem_data,
            "geog_data": geog_data,
            "geol_data": geol_data,
            "phys_data": phys_data,
            "sci_data": sci_data,
            "sust_data": sust_data
        }
        return render(request, 'csun_calendar/schedule_natural_sciences.html', content)
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_arts_and_humanities_courses(request):
    if 'user' in request.session:
        for t in request.POST.getlist('general_list'):
            request.session['user']['ge_list'].append((ast.literal_eval(t)))
            request.session.modified = True
        content = {
            "afrs_data": afrs_data,
            "aas_data": aas_data,
            "anth_data": anth_data,
            "art_data": art_data,
            "cas_data": cas_data,
            "chs_data": chs_data,
            "clas_data": clas_data,
            "coms_data": coms_data,
            "ctva_data": ctva_data,
            "engl_data": engl_data,
            "flit_data": flit_data,
            "gws_data": gws_data,
            "hist_data": hist_data,
            "hum_data": hum_data,
            "js_data": js_data,
            "kin_data": kin_data,
            "ling_data": ling_data,
            "mus_data": mus_data,
            "phil_data": phil_data,
            "rs_data": rs_data,
            "th_data": th_data
        }
        return render(request, 'csun_calendar/schedule_arts_and_humanities.html', content)
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_social_sciences_courses(request):
    if 'user' in request.session:
        for t in request.POST.getlist('general_list'):
            request.session['user']['ge_list'].append((ast.literal_eval(t)))
            request.session.modified = True
        content = {
            "afrs_data": afrs_data,
            "aas_data": aas_data,
            "anth_data": anth_data,
            "ais_data": ais_data,
            "cadv_data": cadv_data,
            "chs_data": chs_data,
            "cas_data": cas_data,
            "econ_data": econ_data,
            "geog_data": geog_data,
            "gws_data": gws_data,
            "hhd_data": hhd_data,
            "hist_data": hist_data,
            "hsci_data": hsci_data,
            "js_data": js_data,
            "mkt_data": mkt_data,
            "pols_data": pols_data,
            "psy_data": psy_data,
            "rs_data": rs_data,
            "soc_data": soc_data,
            "sust_data": sust_data,
            "urbs_data": urbs_data,
        }
        return render(request, 'csun_calendar/schedule_social_sciences.html', content)
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_lifelong_learning_courses(request):
    if 'user' in request.session:
        for t in request.POST.getlist('general_list'):
            request.session['user']['ge_list'].append((ast.literal_eval(t)))
            request.session.modified = True
        content = {
            "afrs_data": afrs_data,
            "aas_data": aas_data,
            "art_data": art_data,
            "ais_data": ais_data,
            "biol_data": biol_data,
            "blaw_data": blaw_data,
            "bus_data": bus_data,
            "cadv_data": cadv_data,
            "cas_daa": cas_data,
            "cce_data": cce_data,
            "cd_data": cd_data,
            "chs_data": chs_data,
            "cjs_data": cjs_data,
            "cm_data": cm_data,
            "comp_data": comp_data,
            "coms_data": coms_data,
            "ctva_data": ctva_data,
            "engl_data": engl_data,
            "eoh_data": eoh_data,
            "fcs_data": fcs_data,
            "fin_data": fin_data,
            "flit_data": flit_data,
            "geog_data": geog_data,
            "geol_data": geol_data,
            "gws_data": gws_data,
            "hist_data": hist_data,
            "hsci_data": hsci_data,
            "jour_data": jour_data,
            "js_data": js_data,
            "kin_data": kin_data,
            "ling_data": ling_data,
            "mse_data": mse_data,
            "phil_data": phil_data,
            "qs_data": qs_data,
            "rtm_data": rtm_data,
            "sci_data": sci_data,
            "sust_data": sust_data,
            "univ_data": univ_data,
        }
        return render(request, 'csun_calendar/schedule_lifelong_learning.html', content)
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_comparative_cultural_studies_courses(request):
    if 'user' in request.session:
        for t in request.POST.getlist('general_list'):
            request.session['user']['ge_list'].append((ast.literal_eval(t)))
            request.session.modified = True
        content = {
            "aas_data": aas_data,
            "afrs_data": afrs_data,
            "ais_data": ais_data,
            "anth_data": anth_data,
            "arab_data": arab_data,
            "armn_data": armn_data,
            "art_data": art_data,
            "blaw_data": blaw_data,
            "cas_data": cas_data,
            "chin_data": chin_data,
            "chs_data": chs_data,
            "clas_data": clas_data,
            "coms_data": coms_data,
            "engl_data": engl_data,
            "flit_data": flit_data,
            "fren_data": fren_data,
            "geog_data": geog_data,
            "gws_data": gws_data,
            "hebr_data": hebr_data,
            "hist_data": hist_data,
            "ital_data": ital_data,
            "japn_data": japn_data,
            "jour_data": jour_data,
            "js_data": js_data,
            "kin_data": kin_data,
            "kor_data": kor_data,
            "ling_data": ling_data,
            "mse_data": mse_data,
            "mus_data": mus_data,
            "pers_data": pers_data,
            "phil_data": phil_data,
            "pols_data": pols_data,
            "qs_data": qs_data,
            "rs_data": rs_data,
            "rtm_data": rtm_data,
            "russ_data": russ_data,
            "soc_data": soc_data,
            "span_data": span_data,
            "sped_data": sped_data,
            "th_data": th_data,
            "urbs_data": urbs_data,
        }
        return render(request, 'csun_calendar/schedule_comparative_cultural_studies.html', content)
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def get_us_history_and_government_courses(request):
    if 'user' in request.session:
        for t in request.POST.getlist('general_list'):
            request.session['user']['ge_list'].append((ast.literal_eval(t)))
            request.session.modified = True
        content = {
            "aas_data": aas_data,
            "afrs_data": afrs_data,
            "chs_data": chs_data,
            "econ_data": econ_data,
            "hist_data": hist_data,
            "pols_data": pols_data,
            "rs_data": rs_data,
        }
        return render(request, 'csun_calendar/schedule_us_history_and_government.html', content)
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def gpa(request):
    if 'user' in request.session:
        user = User.objects.filter(id = request.session['user']['id']).first()
        schedule = Schedule.objects.filter(user_id = user).first()
        schedule.year_one_semester_one = get_dict(schedule.year_one_semester_one)
        schedule.year_one_semester_two = get_dict(schedule.year_one_semester_two)
        schedule.year_one_summer = get_dict(schedule.year_one_summer)
        schedule.year_two_semester_one = get_dict(schedule.year_two_semester_one)
        schedule.year_two_semester_two = get_dict(schedule.year_two_semester_two)
        schedule.year_two_summer = get_dict(schedule.year_two_summer)
        schedule.year_three_semester_one = get_dict(schedule.year_three_semester_one)
        schedule.year_three_semester_two = get_dict(schedule.year_three_semester_two)
        schedule.year_three_summer = get_dict(schedule.year_three_summer)
        schedule.year_four_semester_one = get_dict(schedule.year_four_semester_one)
        schedule.year_four_semester_two = get_dict(schedule.year_four_semester_two)
        schedule.year_four_summer = get_dict(schedule.year_four_summer)
        content = {
            'y1_s1': schedule.year_one_semester_one,
            'y1_s2': schedule.year_one_semester_two,
            'y1_summer': schedule.year_one_summer,
            'y2_s1': schedule.year_two_semester_one,
            'y2_s2': schedule.year_two_semester_two,
            'y2_summer': schedule.year_two_summer,
            'y3_s1': schedule.year_three_semester_one,
            'y3_s2': schedule.year_three_semester_two,
            'y3_summer': schedule.year_three_summer,
            'y4_s1': schedule.year_four_semester_one,
            'y4_s2': schedule.year_four_semester_two,
            'y4_summer': schedule.year_four_summer,
            'y': user.starting_year
        }
        return render(request, 'csun_calendar/dashboard.html', content)
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def process_schedule(request):
    if 'user' in request.session:
        user = User.objects.filter(id = request.session['user']['id']).first()
        schedule = Schedule.objects.filter(user_id = user).first()
        # print(schedule)
        # p = User.objects.filter(id = request.session['user']['id']).values_list('general_elective_preference', flat = True)
        # print(schedule.year_one_semester_one)
        print(request.POST.getlist('general_requirements'))
        
        if request.POST['year'] == 'y1_s1':
            schedule.year_one_semester_one = request.POST.getlist('general_requirements')
            schedule.save()
        elif request.POST['year'] == 'y1_s2':
            schedule.year_one_semester_two = request.POST.getlist('general_requirements')
            schedule.save()
        elif request.POST['year'] == 'y1_summer':
            schedule.year_one_summer = request.POST.getlist('general_requirements')
            schedule.save()
        elif request.POST['year'] == 'y2_s1':
            schedule.year_two_semester_one = request.POST.getlist('general_requirements')
            schedule.save()
        elif request.POST['year'] == 'y2_s2':
            schedule.year_two_semester_two = request.POST.getlist('general_requirements')
            schedule.save()
        elif request.POST['year'] == 'y2_summer':
            schedule.year_two_summer = request.POST.getlist('general_requirements')
            schedule.save()
        elif request.POST['year'] == 'y3_s1':
            schedule.year_three_semester_one = request.POST.getlist('general_requirements')
            schedule.save()
        elif request.POST['year'] == 'y3_s2':
            schedule.year_three_semester_two = request.POST.getlist('general_requirements')
            schedule.save()
        elif request.POST['year'] == 'y3_summer':
            schedule.year_three_summer = request.POST.getlist('general_requirements')
            schedule.save()
        elif request.POST['year'] == 'y4_s1':
            schedule.year_four_semester_one = request.POST.getlist('general_requirements')
            schedule.save()
        elif request.POST['year'] == 'y4_s2':
            schedule.year_four_semester_two = request.POST.getlist('general_requirements')
            schedule.save()
        elif request.POST['year'] == 'y4_summer':
            schedule.year_four_summer = request.POST.getlist('general_requirements')
            schedule.save()
        
        return redirect(schedule_semesters)
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

def schedule_semesters(request):
    if 'user' in request.session:
        for t in request.POST.getlist('general_list'):
            request.session['user']['ge_list'].append((ast.literal_eval(t)))
            request.session.modified = True

        request.session['user']['json_ge_list'] = json.dumps(request.session['user']['ge_list'])
        request.session.modified = True

        user = User.objects.filter(id = request.session['user']['id']).first()
        schedule = Schedule.objects.filter(user_id = user).first()
        schedule.year_one_semester_one = get_dict(schedule.year_one_semester_one)
        schedule.year_one_semester_two = get_dict(schedule.year_one_semester_two)
        schedule.year_one_summer = get_dict(schedule.year_one_summer)
        schedule.year_two_semester_one = get_dict(schedule.year_two_semester_one)
        schedule.year_two_semester_two = get_dict(schedule.year_two_semester_two)
        schedule.year_two_summer = get_dict(schedule.year_two_summer)
        schedule.year_three_semester_one = get_dict(schedule.year_three_semester_one)
        schedule.year_three_semester_two = get_dict(schedule.year_three_semester_two)
        schedule.year_three_summer = get_dict(schedule.year_three_summer)
        schedule.year_four_semester_one = get_dict(schedule.year_four_semester_one)
        schedule.year_four_semester_two = get_dict(schedule.year_four_semester_two)
        schedule.year_four_summer = get_dict(schedule.year_four_summer)

        schedules = [schedule.year_one_semester_one, schedule.year_one_semester_two, schedule.year_one_summer, schedule.year_two_semester_one, schedule.year_two_semester_two, schedule.year_two_summer, schedule.year_three_semester_one, schedule.year_three_semester_two, schedule.year_three_summer, schedule.year_four_semester_one, schedule.year_four_semester_two, schedule.year_four_summer]
        sc = []
        for s in schedules:
            for p in s:
                sc.append(p)

        if schedule.year_one_semester_one == [] and schedule.year_one_semester_two == []:    
            current = schedule.year_one_semester_one
            previous = schedule.year_one_semester_one
        if schedule.year_one_semester_one != [] and schedule.year_one_semester_two == []:
            current = schedule.year_one_semester_two
        if schedule.year_one_semester_two != [] and schedule.year_two_semester_one == []:
            current = schedule.year_two_semester_one
            previous = schedule.year_one_semester_two
        if schedule.year_two_semester_one != [] and schedule.year_two_semester_two == []:
            current = schedule.year_two_semester_two
            previous = schedule.year_two_semester_one
        if schedule.year_two_semester_two != [] and schedule.year_three_semester_one == []:
            current = schedule.year_three_semester_one
            previous = schedule.year_two_semester_two 
        if schedule.year_three_semester_one != [] and schedule.year_three_semester_two == []:
            current = schedule.year_three_semester_two
            previous = schedule.year_three_semester_one                                    
        if schedule.year_three_semester_two != [] and schedule.year_four_semester_one == []:
            current = schedule.year_four_semester_one
            previous = schedule.year_three_semester_two 
        if schedule.year_four_semester_one != [] and schedule.year_four_semester_two == []:
            current = schedule.year_four_semester_two
            previous = schedule.year_four_semester_one                         
        
        # not_show_list = get_majors(comp_data, math_data)
        request.session['user']['major_list'] = get_majors(comp_data, math_data)
        request.session.modified = True
        to_show_list = []
        for m in request.session['user']['major_list']:
            if m['subject'] == 'COMP':
                if m['catalog_number'] == '108':
                    if m not in (schedule.year_one_semester_one):
                        to_show_list.append(m)
                if m['catalog_number'] == '110' and m not in sc:
                    print("here - 110")
                    if (specific_majors_data(comp_data, '108') and specific_majors_data(math_data, '102')) in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '110L' and m not in sc:
                    print("here - 110L")
                    if (specific_majors_data(comp_data, '108') and specific_majors_data(math_data, '102')) in sc:
                        to_show_list.append(m)                        
                if m['catalog_number'] == '182' and m not in sc:
                    if (specific_majors_data(comp_data, '110') and specific_majors_data(math_data, '105')) in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '182L' and m not in sc:
                    if (specific_majors_data(comp_data, '110') and specific_majors_data(math_data, '105')) in sc:
                        to_show_list.append(m)                      
                if m['catalog_number'] == '122' and m not in sc:
                    if (specific_majors_data(comp_data, '110') and specific_majors_data(math_data, '105')) in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '122L' and m not in sc:
                    if (specific_majors_data(comp_data, '110') and specific_majors_data(math_data, '105')) in sc:
                        to_show_list.append(m)                      
                if m['catalog_number'] == '282' and m not in sc:
                    if (specific_majors_data(comp_data, '182') and specific_majors_data(math_data, '150A')) in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '256' and m not in sc:
                    if (specific_majors_data(comp_data, '182') and specific_majors_data(math_data, '150A')) in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '256L' and m not in sc:
                    if (specific_majors_data(comp_data, '182') and specific_majors_data(math_data, '150A')) in sc:
                        to_show_list.append(m)                        
                if m['catalog_number'] == '222' and m not in sc:
                    if (specific_majors_data(comp_data, '182') and specific_majors_data(comp_data, '122')) in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '380' and m not in sc:
                    if specific_majors_data(comp_data, '282') in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '380L' and m not in sc:
                    if specific_majors_data(comp_data, '282') in sc:
                        to_show_list.append(m)                        
                if m['catalog_number'] == '333' and m not in sc:
                    if specific_majors_data(comp_data, '282') in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '310' and m not in sc:
                    if specific_majors_data(comp_data, '256') in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '322' and m not in sc:
                    if specific_majors_data(comp_data, '222') in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '322L' and m not in sc:
                    if specific_majors_data(comp_data, '222') in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '482' and m not in sc:
                    if (specific_majors_data(comp_data, '282') and specific_majors_data(math_data, '262')) in sc:
                        to_show_list.append(m)                         
                if m['catalog_number'] == '490' and m not in sc:
                    if specific_majors_data(comp_data, '380') in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '490L' and m not in sc:
                    if specific_majors_data(comp_data, '380') in sc:
                        to_show_list.append(m)                          
                if m['catalog_number'] == '491' and m not in sc:
                    if specific_majors_data(comp_data, '490') in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '491L' and m not in sc:
                    if specific_majors_data(comp_data, '490') in sc:
                        to_show_list.append(m)                      
            elif m['subject'] == 'MATH':
                if m['catalog_number'] == '102' and m not in sc:
                    if m not in schedule.year_one_semester_one:
                        to_show_list.append(m)
                if m['catalog_number'] == '105' and m not in sc:
                    if specific_majors_data(math_data, '102') in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '150A' and m not in sc:
                    if specific_majors_data(math_data, '105') in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '150B' and m not in sc:
                    if specific_majors_data(math_data, '150A') in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '262' and m not in sc:
                    if specific_majors_data(math_data, '150B') in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '482' and m not in sc:
                    if (specific_majors_data(math_data, '262') and specific_majors_data(comp_data, '282')) in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '340' and m not in sc:
                    if specific_majors_data(math_data, '150B') in sc:
                        to_show_list.append(m)
                if m['catalog_number'] == '341' and m not in sc:
                    if specific_majors_data(math_data, '150B') in sc:
                        to_show_list.append(m)   
        


        for a in request.session['user']['major_list']:
            if a not in to_show_list and a in sc:
                request.session['user']['major_list'].remove(a)
                request.session.modified = True 
        for t in to_show_list:
            if t in sc:
                to_show_list.remove(t)                                                                 

        if schedule.year_one_semester_one:
            for t in schedule.year_one_semester_one:
                if t in request.session['user']['ge_list']:
                    request.session['user']['ge_list'].remove(t)
                    request.session.modified = True
        if schedule.year_one_semester_two:
            for t in schedule.year_one_semester_two:
                if t in request.session['user']['ge_list']:
                    request.session['user']['ge_list'].remove(t)
                    request.session.modified = True
        if schedule.year_one_summer:
            for t in schedule.year_one_summer:
                if t in request.session['user']['ge_list']:
                    request.session['user']['ge_list'].remove(t)
                    request.session.modified = True
        if schedule.year_two_semester_one:
            for t in schedule.year_two_semester_one:
                if t in request.session['user']['ge_list']:
                    request.session['user']['ge_list'].remove(t)
                    request.session.modified = True
        if schedule.year_two_semester_two:
            for t in schedule.year_two_semester_two:
                if t in request.session['user']['ge_list']:
                    request.session['user']['ge_list'].remove(t)
                    request.session.modified = True
        if schedule.year_two_summer:
            for t in schedule.year_two_summer:
                if t in request.session['user']['ge_list']:
                    request.session['user']['ge_list'].remove(t)
                    request.session.modified = True
        if schedule.year_three_semester_one:
            for t in schedule.year_three_semester_one:
                if t in request.session['user']['ge_list']:
                    request.session['user']['ge_list'].remove(t)
                    request.session.modified = True
        if schedule.year_three_semester_two:
            for t in schedule.year_three_semester_two:
                if t in request.session['user']['ge_list']:
                    request.session['user']['ge_list'].remove(t)
                    request.session.modified = True
        if schedule.year_three_summer:
            for t in schedule.year_three_summer:
                if t in request.session['user']['ge_list']:
                    request.session['user']['ge_list'].remove(t)
                    request.session.modified = True
        if schedule.year_four_semester_one:
            for t in schedule.year_four_semester_one:
                if t in request.session['user']['ge_list']:
                    request.session['user']['ge_list'].remove(t)
                    request.session.modified = True
        if schedule.year_four_semester_two:
            for t in schedule.year_four_semester_two:
                if t in request.session['user']['ge_list']:
                    request.session['user']['ge_list'].remove(t)
                    request.session.modified = True
        if schedule.year_four_summer:
            for t in schedule.year_four_summer:
                if t in request.session['user']['ge_list']:
                    request.session['user']['ge_list'].remove(t)
                    request.session.modified = True
        
        to_show_elective = []
        not_show_elective = request.session['user']['elective_list']
        added_elective = []
        if specific_majors_data(comp_data, '380') in sc and specific_majors_data(comp_data, '322') in sc:
            to_show_elective = request.session['user']['elective_list']
            not_show_elective = []
        for x in to_show_elective:
            if x in sc:
                to_show_elective.remove(x)
                added_elective.append(x)

        elective_unit_sum = 0
        for a in added_elective:
            elective_unit_sum += int(a['units'])

        print(current)
        # y1_s1_json = json.dumps(schedule.year_one_semester_one)
        # print(y1_s1_json)
        content = {
            'y1_s1': schedule.year_one_semester_one,
            'y1_s2': schedule.year_one_semester_two,
            'y1_summer': schedule.year_one_summer,
            'y2_s1': schedule.year_two_semester_one,
            'y2_s2': schedule.year_two_semester_two,
            'y2_summer': schedule.year_two_summer,
            'y3_s1': schedule.year_three_semester_one,
            'y3_s2': schedule.year_three_semester_two,
            'y3_summer': schedule.year_three_summer,
            'y4_s1': schedule.year_four_semester_one,
            'y4_s2': schedule.year_four_semester_two,
            'y4_summer': schedule.year_four_summer,
            'y': user.starting_year,
            'to_show_list': to_show_list,
            'current': current,
            'to_show_elective': to_show_elective,
            'not_show_elective': not_show_elective,
            'elective_unit_sum': elective_unit_sum,
            'added_elective': added_elective
        }
        return render(request, 'csun_calendar/schedule_semesters.html', content)
    else:
        messages.error(request, 'You must be logged in to view this page!')
        return redirect(index)

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
        u = User.objects.last()
        Schedule.objects.create(user_id = u)
        session_user = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'student_id': request.POST['student_id'],
            'id': User.objects.last().id,
            'ge_prefs': [],
            'ge_list': [],
            'json_ge_list': [],
            'major_list': get_majors(comp_data, math_data),
            'elective_list': get_major_electives(comp_data), 
            'y': request.POST['starting_year']
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
                'id': user[0].id,
                'ge_prefs': [],
                'ge_list': [],
                'json_ge_list': [],
                'major_list': get_majors(comp_data, math_data),
                'elective_list': get_major_electives(comp_data),
                'y': user[0].starting_year
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

