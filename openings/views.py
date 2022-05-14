from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Company, Employee
from technologies.models import ProgrammingLanguage, Technology, Topic
from .models import *


class CreateOpeningView(APIView):
    def _create_opening(self):
        pass

    def post(self, request):
        employee = Employee.objects.get(user=request.user)
        company = Company.objects.get(employees=employee)

        opening = Opening(
            company=company,
            created_by=employee,
            status='Sourcing',
            title=request.data['title'],
            team=request.data['team'],
            description=request.data['description'],
            years_of_experience=request.data['years_of_experience'],
            base_compensation=request.data['base_compensation'],
            equity_compensation=request.data['equity_compensation'],
            other_compensation=request.data['other_compensation'],
        )

        for programming_language in request.data['programming_languages']:
            language = ProgrammingLanguage.get(name=programming_language)
            opening.programming_languages.add(language)

        for technology in request.data['technologies']:
            technology = Technology.get(name=technology)
            opening.technologies.add(technology)

        for topic in request.data['topics']:
            topic = Topic.get(name=topic)
            opening.topics.add(topic)

        opening.save()

        return Response(status=200)
