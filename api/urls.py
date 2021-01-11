from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_extensions.routers import NestedRouterMixin

from api.views import YearViewSet, FieldOfStudyViewSet, SubjectViewSet, StudentViewSet, PointsViewSet, \
    ApplicationViewSet, UserViewSet


class NestedSimpleRouter(NestedRouterMixin,SimpleRouter):
    pass

router = NestedSimpleRouter()

years_router = router.register('years',YearViewSet)
years_router.register('fields_of_study',FieldOfStudyViewSet,basename='years-fields_of_study',parents_query_lookups=['year']).register\
    ('subjects',SubjectViewSet,basename='years-fields_of_study-subjects',parents_query_lookups=['field_of_study__year','field_of_study'])

subjects_router=router.register('subjects',SubjectViewSet)

users_router=router.register('users',UserViewSet)
users_router.register('points',PointsViewSet,basename='students-points',parents_query_lookups=['student'])
users_router.register('applications',ApplicationViewSet,basename='students-applications',parents_query_lookups=['student'])

urlpatterns=router.urls