from rest_framework.serializers import ModelSerializer
from api.models import User, Year, FieldOfStudy, Subject, Student, SubjectGroup, Points, Application


class YearSerializer(ModelSerializer):

    class Meta:
        fields = ('id','start_year')
        model=Year

class FieldOfStudySerializer(ModelSerializer):

    class Meta:
        fields =('id','year','name')
        model=FieldOfStudy

class SubjectSerializer(ModelSerializer):

    class Meta:
        fields=('id','field_of_study','name','description','lecturer','type','start_time','end_time')
        model=Subject



class StudentSerializer(ModelSerializer):

    class Meta:
        fields=('id','user','field_of_study')
        model = Student


class UserSerializer(ModelSerializer):
    fields_of_study=StudentSerializer(many=True,read_only=True)

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'groups', 'email','fields_of_study')
        model = User

class SubjectGroupSerializer(ModelSerializer):
    students=StudentSerializer(many=True,read_only=True)

    class Meta:
        fields=('id','subject','students')
        model=SubjectGroup

class PointsSerializer(ModelSerializer):

    class Meta:
        fields=('id','subject','student','points')
        model=Points

class ApplicationSerializer(ModelSerializer):

    class Meta:
        fields=('id','unwanted_subject','wanted_subject','student','priority','created_at')
        model=Application