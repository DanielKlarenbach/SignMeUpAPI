from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    university = models.ForeignKey(University,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.university} {self.name}"

class Year(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    start_year = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return f"{self.department} {self.start_year}"

class FieldOfStudy(models.Model):
    year = models.ForeignKey(Year,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.year} {self.name}"

class Subject(models.Model):
    field_of_study = models.ForeignKey(FieldOfStudy,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    lecturer = models.CharField(max_length=50)
    type = models.CharField(max_length=1)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.name} {self.start_time}:{self.end_time}"

class User(AbstractUser):
    groups = models.ForeignKey(Group, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, unique=True)
    university=models.ForeignKey(University,on_delete=models.CASCADE)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)

    REQUIRED_FIELDS = ['groups_id', 'email','university']

    def __str__(self):
        return self.username

class Student(models.Model):
    field_of_study = models.ForeignKey(FieldOfStudy,on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='fields_of_study',on_delete=models.CASCADE)

    class Meta:
        db_table='student'
        constraints = [
            models.UniqueConstraint(fields=['field_of_study', 'user'], name='unique_student')
        ]

    def __str__(self):
        return f"{self.user} {self.field_of_study}"

class SubjectGroup(models.Model):
    subject=models.ForeignKey(Subject,related_name='subject_group',on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)

    class Meta:
        db_table='subject_group'
        constraints = [
            models.UniqueConstraint(fields=['subject', 'student'], name='unique_subject_group')
        ]

    def save(self,*args,**kwargs):
        if self.student.field_of_study != self.subject.field_of_study :
            raise Exception("Student can't belong to the group outside of his field of study")
        super(SubjectGroup, self).save(*args,**kwargs)

    def __str__(self):
        return  f"{self.subject} {self.student}"

class Points(models.Model):
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField()

    class Meta:
        db_table='points'
        constraints = [
            models.UniqueConstraint(fields=['subject', 'student'], name='unique_points')
        ]

    def save(self,*args,**kwargs):
        if self.student.field_of_study != self.subject.field_of_study :
            raise Exception("Student can't assign points to the subject outside of his field of study")
        super(Points, self).save(*args,**kwargs)

    def __str__(self):
        return  f"{self.subject} {self.student}"

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

    def save(self,*args,**kwargs):
        if self.student.field_of_study != self.unwanted_subject.field_of_study or self.student.field_of_study != self.wanted_subject.field_of_study:
            raise Exception("Student can't make application with subject outside of his field of study")
        super(Application, self).save(*args,**kwargs)

    def __str__(self):
        return  f"{self.unwanted_subject}->{self.wanted_subject} {self.student}"
