from rest_auth.models import TokenModel
from rest_framework.serializers import ModelSerializer
from api.models import User, Year, FieldOfStudy, Subject, Student, SubjectGroup, Points, Application, University, \
    Department

class UniversitySerializer(ModelSerializer):

    class Meta:
        fields = ('id','name')
        model=University

class DepartmentSerializer(ModelSerializer):

    university=UniversitySerializer

    class Meta:
        fields = ('id','university','name')
        model=Department

class YearSerializer(ModelSerializer):

    department=DepartmentSerializer

    class Meta:
        fields = ('id','department','start_year')
        model=Year

class FieldOfStudySerializer(ModelSerializer):

    year=YearSerializer

    class Meta:
        fields =('id','year','name')
        model=FieldOfStudy

class SubjectSerializer(ModelSerializer):

    class Meta:
        fields=('id','field_of_study','name','description','lecturer','type','start_time','end_time','subject_group')
        model=Subject

class StudentSerializer(ModelSerializer):

    field_of_study=FieldOfStudySerializer

    class Meta:
        fields=('id','user','field_of_study')
        model = Student

class SubjectGroupSerializer(ModelSerializer):

    student=StudentSerializer

    class Meta:
        fields=('id','subject','student')
        model=SubjectGroup

class PointsSerializer(ModelSerializer):

    subject=SubjectSerializer()

    class Meta:
        fields=('id','student','subject','points')
        model=Points

class ApplicationSerializer(ModelSerializer):

    unwanted_subject=SubjectSerializer()
    wanted_subject=SubjectSerializer()

    class Meta:
        fields=('id','student','unwanted_subject','wanted_subject','priority','created_at')
        model=Application

class UserSerializer(ModelSerializer):

    university=UniversitySerializer
    department=DepartmentSerializer

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'groups', 'email','university','department')
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class TokenSerializer(ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = TokenModel
        fields = ('key', 'user')