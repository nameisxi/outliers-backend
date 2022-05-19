from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import AllowAny

from users.models import Company, Employee
from technologies.models import ProgrammingLanguage, Technology, Topic
from .models import *
from .serializers import *


class CreateOpeningView(APIView):
    def _create_opening(self):
        pass

    def post(self, request):
        # TODO: pass data to serializer and use serialized_data.is_valid(). Reference: https://stackoverflow.com/questions/39185912/can-we-use-serializer-class-attribute-with-apiviewdjango-rest-framework 
        employee = Employee.objects.get(user=request.user)
        company = Company.objects.get(employees=employee)

        opening = Opening(
            company=company,
            created_by=employee,
            status='Sourcing',
            title=request.data.get('title'),
            team=request.data.get('team'),
            description=request.data.get('description'),
            years_of_experience_min=request.data.get('years_of_experience_min', 0),
            years_of_experience_max=request.data.get('years_of_experience_max', None),
            # base_compensation_min=request.data.get('base_compensation_min', None),
            # base_compensation_max=request.data.get('base_compensation_max', None),
            # base_compensation_currency=request.data.get('base_compensation_currency', 'usd'),
            # equity_compensation_min=request.data.get('equity_compensation_min', None),
            # equity_compensation_max=request.data.get('equity_compensation_max', None),
            # equity_compensation_currency=request.data.get('equity_compensation_currency', 'usd'),
            # other_compensation_min=request.data.get('other_compensation_min', None),
            # other_compensation_max=request.data.get('other_compensation_max', None),
            # other_compensation_currency=request.data.get('other_compensation_currency', 'usd'),
        )
        opening.save()

        programming_languages = request.data.get('programming_languages', None)
        if programming_languages:
            for programming_language in programming_languages:
                try: 
                    language = ProgrammingLanguage.objects.get(name=programming_language.lower())
                    opening.programming_languages.add(language)
                except Exception as e:
                    print(f"Error occurred while adding programming language '{programming_language}' to opening:")
                    print(e)
                    continue

        technologies = request.data.get('technologies', None)
        if technologies:
            for technology in technologies:
                try:
                    technology = Technology.objects.get(name=technology.lower())
                    opening.technologies.add(technology)
                except Exception as e:
                    print(f"Error occurred while adding technology '{technology}' to opening:")
                    print(e)
                    continue

        topics = request.data.get('topics', None)
        if topics:
            for topic in topics:
                try:
                    topic = Topic.objects.get(name=topic.lower())
                    opening.topics.add(topic)
                except Exception as e:
                    print(f"Error occurred while adding topic '{topic}' to opening:")
                    print(e)
                    continue

        # return Response(status=200)
        return JsonResponse({
            'status': 200,
            'opening_id': opening.id,
        })


class OpeningList(APIView):
    """
    Returns a list of Opening objects, belonging to a Company, for a logged in Employee.
    """

    def get(self, request, opening_id=None):
        # employee = Employee.objects.get(user=request.user)
        # company = Company.objects.get(employees=employee)
        # openings = Opening.objects.filter(company=company)
        if opening_id:
            opening = Opening.objects.get(id=opening_id)
            serializer = OpeningSerializer(opening, many=False)

            return Response(serializer.data)

        openings = Opening.objects.all()

        serializer = OpeningSerializer(openings, many=True)

        return Response(serializer.data)

