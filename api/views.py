
# Create your views here.
# from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, UpdateAPIView, \
    DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from api.models import Year, FieldOfStudy, Subject, User, Student, SubjectGroup, Points, Application, University, \
    Department
from api.permissions import IsUniversityAdmin, IsDepartmentAdmin, IsAccountOwner, IsFromThisUniversity, \
    IsFromThisDepartment, IsStudent, AllowNoOne
from api.serializers import YearSerializer, FieldOfStudySerializer, SubjectSerializer, UserSerializer, \
    StudentSerializer, SubjectGroupSerializer, PointsSerializer, ApplicationSerializer, UniversitySerializer, \
    DepartmentSerializer

class UniversityViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [IsAuthenticated & IsUniversityAdmin & IsFromThisUniversity]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'retrieve' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes  = [IsAuthenticated & IsUniversityAdmin & IsFromThisUniversity]
        elif self.action == 'create'  or self.action == 'list':
            permission_classes = [AllowNoOne]
        return [permission() for permission in permission_classes]

class DepartmentViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class YearViewSet(NestedViewSetMixin,ModelViewSet):

    serializer_class = YearSerializer
    permission_classes = [IsAuthenticated & IsDepartmentAdmin & IsFromThisDepartment]

    def get_queryset(self):
        user = self.request.user
        return Year.objects.filter(department=user.department)

class FieldOfStudyViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = FieldOfStudy.objects.all()
    serializer_class = FieldOfStudySerializer

class SubjectViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes  = [IsAuthenticated & IsDepartmentAdmin]
        elif self.action == 'retrieve'  or self.action == 'list':
            permission_classes = [IsAuthenticated & (IsDepartmentAdmin | IsStudent)]
        return [permission() for permission in permission_classes]

class UserViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.groups_id==1 :
            super(UserViewSet, self).create(*args,group_id=2,request=request,**kwargs)
        else:
            super(UserViewSet, self).create(*args,group_id=3,request=request,**kwargs)

    def get_queryset(self):
        if self.request.user.groups_id==1 :
            return User.objects.filter(groups_id=2)
        elif self.request.user.groups_id==2:
            return User.objects.filter(groups_id=3)
        else:
            return User.objects.get(user=self.request.user)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'list' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes  = [IsAuthenticated & (IsDepartmentAdmin | IsUniversityAdmin )]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated & (IsUniversityAdmin | IsDepartmentAdmin | IsAccountOwner)]
        return [permission() for permission in permission_classes]

class StudentViewSet(NestedViewSetMixin,ModelViewSet):

    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Student.objects.filter(user=user)

class SubjectGroupViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = SubjectGroup.objects.all()
    serializer_class = SubjectGroupSerializer

class PointsViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = Points.objects.all()
    serializer_class = PointsSerializer

class ApplicationViewSet(NestedViewSetMixin,ModelViewSet):

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

