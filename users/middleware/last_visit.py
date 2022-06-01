from django.utils import timezone
from rest_framework.authtoken.models import Token

from ..models import Employee


class SetLastVisitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            Employee.objects.filter(user=request.user).update(last_visit=timezone.now())

        return response
