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

        print()
        print("DATA:", request.data)
        print()

        opening = Opening(
            company=company,
            created_by=employee,
            status='Sourcing',
            title=request.data.get('title'),
            team=request.data.get('team', None),
            description=request.data.get('description', None),
            years_of_experience=request.data.get('years_of_experience', None),
            base_compensation_min=request.data.get('base_compensation_min', None),
            base_compensation_max=request.data.get('base_compensation_max', None),
            base_compensation_currency=request.data.get('base_compensation_curency', None),
            equity_compensation_min=request.data.get('equity_compensation_min', None),
            equity_compensation_max=request.data.get('equity_compensation_max', None),
            equity_compensation_currency=request.data.get('equity_compensation_curency', None),
            other_compensation_min=request.data.get('other_compensation_min', None),
            other_compensation_max=request.data.get('other_compensation_max', None),
            other_compensation_currency=request.data.get('other_compensation_curency', None),
        )

        programming_languages = request.data.get('programming_languages', None)
        if programming_languages:
            for programming_language in programming_langugages:
                language = ProgrammingLanguage.get(name=programming_language)
                opening.programming_languages.add(language)

        technologies = request.data.get('technologies', None)
        if technologies:
            for technology in technologies:
                technology = Technology.get(name=technology)
                opening.technologies.add(technology)

        topics = request.data.get('topics', None)
        if topics:
            for topic in topics:
                topic = Topic.get(name=topic)
                opening.topics.add(topic)

        opening.save()

        return Response(status=200)
