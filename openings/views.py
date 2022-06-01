from django.utils import timezone

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
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Employee not found.',
            })

        try:
            company = Company.objects.get(employees=employee)
        except Company.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Company not found.',
            })

        opening = Opening(
            company=company,
            opening_created_by=employee,
            opening_updated_by=None,
            status='Sourcing',
            title=request.data.get('title'),
            team=request.data.get('team'),
            description=request.data.get('description'),
            years_of_experience_min=request.data.get('years_of_experience_min', 0) or 0,
            years_of_experience_max=request.data.get('years_of_experience_max', 100) or 100,
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


class UpdateOpeningView(APIView):
    def patch(self, request, opening_id):
        # TODO: pass data to serializer and use serialized_data.is_valid(). Reference: https://stackoverflow.com/questions/39185912/can-we-use-serializer-class-attribute-with-apiviewdjango-rest-framework 
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Employee not found.',
            })

        try:
            company = Company.objects.get(employees=employee)
        except Company.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Company not found.',
            })

        try:
            opening = Opening.objects.get(id=opening_id, company=company)
        except Opening.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Opening not found.',
            })

        Opening.objects.filter(id=opening_id, company=company).update(
            company=company,
            opening_created_by=opening.opening_created_by,
            opening_updated_by=employee,
            status=opening.status,
            title=request.data.get('title') or opening.title,
            team=request.data.get('team', opening.team),
            description=request.data.get('description', opening.description),
            years_of_experience_min=request.data.get('years_of_experience_min', opening.years_of_experience_min) or 0,
            years_of_experience_max=request.data.get('years_of_experience_max', opening.years_of_experience_max) or 100,
            updated_at=timezone.now(),
        )

        programming_languages = request.data.get('programming_languages', None)
        if programming_languages and len(programming_languages) > 0:
            for programming_language in opening.programming_languages.all():
                if programming_language.name.upper() not in programming_languages:
                    try: 
                        opening.programming_languages.remove(programming_language)
                    except Exception as e:
                        print(f"Error occurred while removing programming language '{programming_language}' from opening:")
                        print(e)
                        continue

            for programming_language in programming_languages:
                try: 
                    language = ProgrammingLanguage.objects.get(name=programming_language.lower())
                    opening.programming_languages.add(language)
                except Exception as e:
                    print(f"Error occurred while adding programming language '{programming_language}' to opening:")
                    print(e)
                    continue

        technologies = request.data.get('technologies', None)
        if technologies and len(technologies) > 0:
            for technology in opening.technologies.all():
                if technology.name.upper() not in technologies:
                    try: 
                        opening.technologies.remove(technology)
                    except Exception as e:
                        print(f"Error occurred while removing technology '{technology}' from opening:")
                        print(e)
                        continue

            for technology in technologies:
                try:
                    technology = Technology.objects.get(name=technology.lower())
                    opening.technologies.add(technology)
                except Exception as e:
                    print(f"Error occurred while adding technology '{technology}' to opening:")
                    print(e)
                    continue

        topics = request.data.get('topics', None)
        if topics and len(topics) > 0:
            for topic in opening.topics.all():
                if topic.name.upper() not in topics:
                    try: 
                        opening.topics.remove(topic)
                    except Exception as e:
                        print(f"Error occurred while removing topic '{topic}' from opening:")
                        print(e)
                        continue

            for topic in topics:
                try:
                    topic = Topic.objects.get(name=topic.lower())
                    opening.topics.add(topic)
                except Exception as e:
                    print(f"Error occurred while adding topic '{topic}' to opening:")
                    print(e)
                    continue

        return JsonResponse({
            'status': 200,
            'opening_id': opening.id,
        })


class DeleteOpeningView(APIView):
    def patch(self, request, opening_id):
        # TODO: pass data to serializer and use serialized_data.is_valid(). Reference: https://stackoverflow.com/questions/39185912/can-we-use-serializer-class-attribute-with-apiviewdjango-rest-framework 
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Employee not found.',
            })

        try:
            company = Company.objects.get(employees=employee)
        except Company.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Company not found.',
            })

        Opening.objects.filter(id=opening_id, company=company).update(
            opening_updated_by=employee,
            updated_at=timezone.now(),
            is_deleted=True,
        )

        return JsonResponse({
            'status': 200,
        })


class OpeningList(APIView):
    """
    Returns a list of Opening objects, belonging to a Company, for a logged in Employee.
    """
    def get(self, request, opening_id=None):
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Employee not found.',
            })

        try:
            company = Company.objects.get(employees=employee)
        except Company.DoesNotExist:
            return JsonResponse({
                'status': 404,
                'message': 'Company not found.',
            })

        if opening_id:
            try:
                opening = Opening.objects.get(id=opening_id, company=company)
            except Opening.DoesNotExist:
                return JsonResponse({
                    'status': 404,
                    'message': 'Opening not found.',
                })

            serializer = OpeningSerializer(opening, many=False)

            return Response(serializer.data)

        openings = Opening.objects.filter(company=company, is_deleted=False)
        serializer = OpeningSerializer(openings, many=True)

        return Response(serializer.data)

