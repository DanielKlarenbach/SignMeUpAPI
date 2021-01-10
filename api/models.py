from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# Create your models here.

class Year(models.Model):
    start_year = models.PositiveSmallIntegerField()

class FieldOfStudy(models.Model):
    year = models.ForeignKey(Year,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Subject(models.Model):
    field_of_study = models.ForeignKey(FieldOfStudy,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    lecturer = models.CharField(max_length=50)
    type = models.CharField(max_length=1)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class User(AbstractUser):
    groups = models.ForeignKey(Group, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, unique=True)

    REQUIRED_FIELDS = ['groups_id', 'email']

class Student(models.Model):
    field_of_study = models.ForeignKey(FieldOfStudy,on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='fields_of_study',on_delete=models.CASCADE)

    class Meta:
        db_table='student'
        constraints = [
            models.UniqueConstraint(fields=['field_of_study', 'user'], name='unique_student')
        ]

class SubjectGroup(models.Model):
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)

    class Meta:
        db_table='subject_group'
        constraints = [
            models.UniqueConstraint(fields=['subject', 'student'], name='unique_subject_group')
        ]

class Points(models.Model):
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField()

    class Meta:
        db_table='points'
        constraints = [
            models.UniqueConstraint(fields=['subject', 'student'], name='unique_points')
        ]

class Application(models.Model):
    unwanted_subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name="unwanted_subject")
    wanted_subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name="wanted_subject")
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    priority = models.PositiveSmallIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='application'
        constraints = [
            models.UniqueConstraint(fields=['unwanted_subject', 'wanted_subject','student'], name='unique_application')
        ]
