from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from api.models import Year, FieldOfStudy, Subject, User, Student, SubjectGroup, Points, Application
from api.serializers import YearSerializer, FieldOfStudySerializer, SubjectSerializer, UserSerializer, \
    StudentSerializer, SubjectGroupSerializer, PointsSerializer, ApplicationSerializer


class YearViewSet(NestedViewSetMixin,ModelViewSet):
    queryset = Year.objects.all()
    serializer_class = YearSerializer

class FieldOfStudyViewSet(NestedViewSetMixin,ModelViewSet):
    queryset = FieldOfStudy.objects.all()
    serializer_class = FieldOfStudySerializer

class SubjectViewSet(NestedViewSetMixin,ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class UserViewSet(NestedViewSetMixin,ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentViewSet(NestedViewSetMixin,ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SubjectGroupViewSet(NestedViewSetMixin,ModelViewSet):
    queryset = SubjectGroup.objects.all()
    serializer_class = SubjectGroupSerializer

class PointsViewSet(NestedViewSetMixin,ModelViewSet):
    queryset = Points.objects.all()
    serializer_class = PointsSerializer

class ApplicationViewSet(NestedViewSetMixin,ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer