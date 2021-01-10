from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_extensions.routers import NestedRouterMixin
from api.views import YearViewSet, FieldOfStudyViewSet, SubjectViewSet, StudentViewSet, PointsViewSet, \
    ApplicationViewSet, SubjectGroupViewSet, UserViewSet

router = SimpleRouter()

router.register('years',YearViewSet)
router.register('fields_of_study',FieldOfStudyViewSet)
router.register('subjects',SubjectViewSet)
router.register('students',StudentViewSet)

class NestedSimpleRouter(NestedRouterMixin,SimpleRouter):
    pass

router = NestedSimpleRouter()

years_router = router.register('years',YearViewSet)
years_router.register('fields_of_study',FieldOfStudyViewSet,basename='years-fields_of_study',parents_query_lookups=['year']).register\
    ('subjects',SubjectViewSet,basename='years-fields_of_study-subjects',parents_query_lookups=['field_of_study__year','field_of_study'])

subjects_router=router.register('subjects',SubjectViewSet)
subjects_router.register('subject_groups',SubjectGroupViewSet,basename='subjects-subject_groups',parents_query_lookups=['subject'])

students_router=router.register('students',StudentViewSet)
students_router.register('points',PointsViewSet,basename='students-points',parents_query_lookups=['student'])
students_router.register('applications',ApplicationViewSet,basename='students-applications',parents_query_lookups=['student'])

router.register('users',UserViewSet)
urlpatterns=router.urls