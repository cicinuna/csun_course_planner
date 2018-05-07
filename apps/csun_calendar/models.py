from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    student_id = models.CharField(max_length = 255)
    starting_year = models.CharField(max_length = 10)
    anticipated_graduation_year = models.CharField(max_length = 10, blank = True)
    graduation_year = models.CharField(max_length = 10, blank = True)
    year_one_semester_one_gpa = models.FloatField(default = 0.0, blank = True)
    year_one_semester_two_gpa = models.FloatField(default = 0.0, blank = True)
    year_one_summer_gpa = models.FloatField(default = 0.0, blank = True)
    year_two_semester_one_gpa = models.FloatField(default = 0.0, blank = True)
    year_two_semester_two_gpa = models.FloatField(default = 0.0, blank = True)
    year_two_summer_gpa = models.FloatField(default = 0.0, blank = True)
    year_three_semester_one_gpa = models.FloatField(default = 0.0, blank = True)
    year_three_semester_two_gpa = models.FloatField(default = 0.0, blank = True)
    year_three_summer_gpa = models.FloatField(default = 0.0, blank = True)
    year_four_semester_one_gpa = models.FloatField(default = 0.0, blank = True)
    year_four_semester_two_gpa = models.FloatField(default = 0.0, blank = True)
    year_four_summer_gpa = models.FloatField(default = 0.0, blank = True)
    cumulative_gpa = models.FloatField(default = 0.0, blank = True)
    general_elective_preference = ArrayField(ArrayField(models.CharField(max_length = 255), blank = True), null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Schedule(models.Model):
    user_id = models.ForeignKey(User, related_name = "student")
    year_one_semester_one = ArrayField(models.TextField(), blank = True, null = True, default = [])
    year_one_semester_two = ArrayField(models.TextField(), blank = True, null = True, default = [])
    year_one_summer = ArrayField(models.TextField(), blank = True, null = True, default = [])
    year_two_semester_one = ArrayField(models.TextField(), blank = True, null = True, default = [])
    year_two_semester_two = ArrayField(models.TextField(), blank = True, null = True, default = [])
    year_two_summer = ArrayField(models.TextField(), blank = True, null = True, default = [])
    year_three_semester_one = ArrayField(models.TextField(), blank = True, null = True, default = [])
    year_three_semester_two = ArrayField(models.TextField(), blank = True, null = True, default = [])
    year_three_summer = ArrayField(models.TextField(), blank = True, null = True, default = [])
    year_four_semester_one = ArrayField(models.TextField(), blank = True, null = True, default = [])
    year_four_semester_two = ArrayField(models.TextField(), blank = True, null = True, default = [])
    year_four_summer = ArrayField(models.TextField(), blank = True, null = True, default = [])
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

