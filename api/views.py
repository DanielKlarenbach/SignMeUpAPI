from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from api.models import Year, FieldOfStudy, Subject, User, Student, SubjectGroup, Points, Application
from api.permissions import IsAdminUser, IsDeansOfficeUser, HasPKAsObjectsFK
from api.serializers import YearSerializer, FieldOfStudySerializer, SubjectSerializer, UserSerializer, \
    StudentSerializer, SubjectGroupSerializer, PointsSerializer, ApplicationSerializer


class YearViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = Year.objects.all()
    serializer_class = YearSerializer
    permission_classes = [IsAuthenticated & (IsAdminUser | IsDeansOfficeUser)]

class FieldOfStudyViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = FieldOfStudy.objects.all()
    serializer_class = FieldOfStudySerializer
    permission_classes = [IsAuthenticated & (IsAdminUser | IsDeansOfficeUser)]

class SubjectViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes  = [IsAuthenticated & (IsAdminUser | IsDeansOfficeUser)]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated & (IsAdminUser | IsDeansOfficeUser | HasPKAsObjectsFK)]
        return [permission() for permission in permission_classes]

class UserViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'list':
            permission_classes  = [IsAuthenticated & (IsAdminUser | IsDeansOfficeUser)]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthenticated & (IsAdminUser | IsDeansOfficeUser | HasPKAsObjectsFK)]
        return [permission() for permission in permission_classes]

class StudentViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SubjectGroupViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = SubjectGroup.objects.all()
    serializer_class = SubjectGroupSerializer

class PointsViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = Points.objects.all()
    serializer_class = PointsSerializer
    permission_classes = [IsAuthenticated & (IsAdminUser | IsDeansOfficeUser | HasPKAsObjectsFK)]

class ApplicationViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated & (IsAdminUser | IsDeansOfficeUser | HasPKAsObjectsFK)]