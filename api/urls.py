from django.conf.urls import url
from django.urls import path, include
from patterns import patterns
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin
from rest_framework_nested.routers import NestedSimpleRouter

from api.views import YearViewSet, FieldOfStudyViewSet, SubjectViewSet, StudentViewSet, PointsViewSet, \
    ApplicationViewSet, DepartmentViewSet, UserViewSet, \
    SubjectGroupViewSet, UniversityViewSet

router = DefaultRouter()

router.register('universities',UniversityViewSet,basename='universities')
router.register('years',YearViewSet,basename='years')
router.register('students',StudentViewSet,basename='students')
router.register('users',UserViewSet,basename='users')

universities_router = NestedSimpleRouter(router,r'universities',lookup='university')
universities_router.register(r'departments', DepartmentViewSet,basename='departments')

years_router = NestedSimpleRouter(router,r'years',lookup='year')
years_router.register(r'fields_of_study',FieldOfStudyViewSet,basename='fields_of_study')

fields_of_study_router=NestedSimpleRouter(years_router,r'fields_of_study',lookup='field_of_study')
fields_of_study_router.register(r'students',StudentViewSet,basename='students')
fields_of_study_router.register(r'subjects',SubjectViewSet,basename='subjects')

subjects_router=NestedSimpleRouter(fields_of_study_router,r'subjects',lookup='subject')
subjects_router.register(r'subjects_student_list',SubjectGroupViewSet,basename='subjects_student_list')

students_router=NestedSimpleRouter(router,r'students',lookup='student')
students_router.register('points',PointsViewSet,basename='points')
students_router.register('applications',ApplicationViewSet,basename='applications')
students_router.register('subjects',SubjectViewSet,basename='subjects')

urlpatterns = (
    url(r'^', include(router.urls)),
    url(r'^', include(universities_router.urls)),
    url(r'^', include(years_router.urls)),
    url(r'^', include(fields_of_study_router.urls)),
    url(r'^', include(subjects_router.urls)),
    url(r'^', include(students_router.urls)),
)
