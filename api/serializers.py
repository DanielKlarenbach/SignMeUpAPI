from rest_framework.serializers import ModelSerializer
from api.models import User, Year, FieldOfStudy, Subject, Student, SubjectGroup, Points, Application


class YearSerializer(ModelSerializer):

    class Meta:
        fields = ('id','start_year')
        model=Year

class FieldOfStudySerializer(ModelSerializer):
    year=YearSerializer()

    class Meta:
        fields =('id','year','name')
        model=FieldOfStudy

class StudentSerializer(ModelSerializer):
    field_of_study=FieldOfStudySerializer()

    class Meta:
        fields=('id','user','field_of_study')
        model = Student

class UserSerializer(ModelSerializer):
    fields_of_study=StudentSerializer(many=True,read_only=True)

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'groups', 'email','fields_of_study')
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class SubjectGroupSerializer(ModelSerializer):
    student=StudentSerializer()

    class Meta:
        fields=('id','subject','student')
        model=SubjectGroup

class SubjectSerializer(ModelSerializer):
    field_of_study=FieldOfStudySerializer()
    subject_group=SubjectGroupSerializer(many=True,read_only=True)

    class Meta:
        fields=('id','field_of_study','name','description','lecturer','type','start_time','end_time','subject_group')
        model=Subject

class PointsSerializer(ModelSerializer):
    subject=SubjectSerializer()
    student=StudentSerializer()

    class Meta:
        fields=('id','subject','student','points')
        model=Points

class ApplicationSerializer(ModelSerializer):
    unwanted_subject=SubjectSerializer()
    wanted_subject=SubjectSerializer()
    student=StudentSerializer()

    class Meta:
        fields=('id','unwanted_subject','wanted_subject','student','priority','created_at')
        model=Application