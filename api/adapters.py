from allauth.account.adapter import DefaultAccountAdapter

from api import models


class UniversityAdminAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super(UniversityAdminAccountAdapter, self).save_user(request, user, form, commit=False)
        user.groups_id = 1
        models.University(name=request.data['university']).save()
        user.university_id = models.University.objects.get(name=request.data['university']).id
        user.save()