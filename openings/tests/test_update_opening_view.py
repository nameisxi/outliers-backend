import json 

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from users.models import Employee, Company, CompanyDomainName
from technologies.models import ProgrammingLanguage, Technology, Topic
from ..models import *
from ..views import *


class TestUpdateOpeningView(APITestCase):
    def _setup(self):
        user = User.objects.create(
            username='testuser-update-opening',
            email='testuser-update-opening@update-opening-company.com'
        )
        user.set_password('test1234')
        user.save()

        company = Company(name='update-opening-company')
        company.save()

        domain = CompanyDomainName(company=company, name='update-opening-company.com')
        domain.save()

        employee = Employee(user=user, company=company)
        employee.save()

        programming_language = ProgrammingLanguage(name='test-update-opening-php')
        programming_language.save()
        programming_language = ProgrammingLanguage(name='test-update-opening-python')
        programming_language.save()
        programming_language = ProgrammingLanguage(name='test-update-opening-go')
        programming_language.save()

        programming_language = ProgrammingLanguage(name='test-update-opening-php_v2')
        programming_language.save()
        programming_language = ProgrammingLanguage(name='test-update-opening-python_v2')
        programming_language.save()
        programming_language = ProgrammingLanguage(name='test-update-opening-go_v2')
        programming_language.save()

        technology = Technology(name='test-update-opening-django')
        technology.save()
        technology = Technology(name='test-update-opening-android')
        technology.save()
        technology = Technology(name='test-update-opening-ios')
        technology.save()

        technology = Technology(name='test-update-opening-django_v2')
        technology.save()
        technology = Technology(name='test-update-opening-android_v2')
        technology.save()
        technology = Technology(name='test-update-opening-ios_v2')
        technology.save()

        topic = Topic(name='test-update-opening-mobile')
        topic.save()
        topic = Topic(name='test-update-opening-nlp')
        topic.save()
        topic = Topic(name='test-update-opening-crypto')
        topic.save()

        topic = Topic(name='test-update-opening-mobile_v2')
        topic.save()
        topic = Topic(name='test-update-opening-nlp_v2')
        topic.save()
        topic = Topic(name='test-update-opening-crypto_v2')
        topic.save()

        factory = APIRequestFactory()
        view = CreateOpeningView.as_view()
        data = {
            'title': 'Example title',
            'team': 'Example team',
            'description': 'Example description',
            'years_of_experience_min': 0,
            'years_of_experience_max': 99,
            'programming_languages': ['test-update-opening-php', 'test-update-opening-python', 'test-update-opening-go'],
            'technologies': ['test-update-opening-django', 'test-update-opening-android', 'test-update-opening-ios'],
            'topics': ['test-update-opening-mobile', 'test-update-opening-nlp', 'test-update-opening-crypto'],
        }
        request = factory.post('/openings/create/', data, format='json')
        force_authenticate(request, user=user)
        response = view(request)

        response = json.loads(response.content.decode('utf-8'))
        opening_id = response['opening_id']

        return user, company, employee, opening_id

    def test_update_opening(self):
        user, company, employee, opening_id = self._setup()

        factory = APIRequestFactory()
        view = UpdateOpeningView.as_view()
        data = {
            'title': 'Example title v2',
            'team': 'Example team v2',
            'description': 'Example description v2',
            'years_of_experience_min': 1,
            'years_of_experience_max': 98,
            'programming_languages': ['test-update-opening-php_v2', 'test-update-opening-python_v2', 'test-update-opening-go_v2'],
            'technologies': ['test-update-opening-django_v2', 'test-update-opening-android_v2', 'test-update-opening-ios_v2'],
            'topics': ['test-update-opening-mobile_v2', 'test-update-opening-nlp_v2', 'test-update-opening-crypto_v2'],
        }
        request = factory.patch(f'/openings/update/{opening_id}/', data, format='json')
        force_authenticate(request, user=user)
        response = view(request, opening_id=opening_id)

        assert(response.status_code == 200)
        assert(Opening.objects.filter(id=opening_id).exists())

        opening = Opening.objects.get(id=opening_id)

        assert(Opening.objects.filter(opening_created_by=employee).exists())
        assert(opening.opening_created_by == employee)
        assert(Opening.objects.filter(opening_updated_by=employee).exists())
        assert(opening.opening_updated_by == employee)

        assert(opening.title == 'Example title v2')
        assert(opening.team == 'Example team v2')
        assert(opening.description == 'Example description v2')
        assert(opening.years_of_experience_min == 1)
        assert(opening.years_of_experience_max == 98)

        assert(opening.programming_languages.count() == 3)
        assert(opening.programming_languages.filter(name='test-update-opening-php_v2').exists())
        assert(opening.programming_languages.filter(name='test-update-opening-python_v2').exists())
        assert(opening.programming_languages.filter(name='test-update-opening-go_v2').exists())
        assert(opening.programming_languages.filter(name='test-update-opening-php').exists() == False)
        assert(opening.programming_languages.filter(name='test-update-opening-python').exists() == False)
        assert(opening.programming_languages.filter(name='test-update-opening-go').exists() == False)

        assert(opening.technologies.count() == 3)
        assert(opening.technologies.filter(name='test-update-opening-django_v2').exists())
        assert(opening.technologies.filter(name='test-update-opening-android_v2').exists())
        assert(opening.technologies.filter(name='test-update-opening-ios_v2').exists())
        assert(opening.technologies.filter(name='test-update-opening-django').exists() == False)
        assert(opening.technologies.filter(name='test-update-opening-android').exists() == False)
        assert(opening.technologies.filter(name='test-update-opening-ios').exists() == False)

        assert(opening.topics.count() == 3)
        assert(opening.topics.filter(name='test-update-opening-mobile_v2').exists())
        assert(opening.topics.filter(name='test-update-opening-nlp_v2').exists())
        assert(opening.topics.filter(name='test-update-opening-crypto_v2').exists())
        assert(opening.topics.filter(name='test-update-opening-mobile').exists() == False)
        assert(opening.topics.filter(name='test-update-opening-nlp').exists() == False)
        assert(opening.topics.filter(name='test-update-opening-crypto').exists() == False)

    def test_update_opening_missing_data(self):
        user, company, employee, opening_id = self._setup()

        factory = APIRequestFactory()
        view = UpdateOpeningView.as_view()
        data = {}

        request = factory.patch(f'/openings/update/{opening_id}/', data, format='json')
        force_authenticate(request, user=user)
        response = view(request, opening_id=opening_id)

        assert(response.status_code == 200)
        assert(Opening.objects.filter(id=opening_id).exists())

        opening = Opening.objects.get(id=opening_id)

        assert(Opening.objects.filter(opening_created_by=employee).exists())
        assert(opening.opening_created_by == employee)
        assert(Opening.objects.filter(opening_updated_by=employee).exists())
        assert(opening.opening_updated_by == employee)

        assert(opening.title == 'Example title')
        assert(opening.team == 'Example team')
        assert(opening.description == 'Example description')
        assert(opening.years_of_experience_min == 0)
        assert(opening.years_of_experience_max == 99)

        assert(opening.programming_languages.count() == 3)
        assert(opening.programming_languages.filter(name='test-update-opening-php').exists())
        assert(opening.programming_languages.filter(name='test-update-opening-python').exists())
        assert(opening.programming_languages.filter(name='test-update-opening-go').exists())

        assert(opening.technologies.count() == 3)
        assert(opening.technologies.filter(name='test-update-opening-django').exists())
        assert(opening.technologies.filter(name='test-update-opening-android').exists())
        assert(opening.technologies.filter(name='test-update-opening-ios').exists())

        assert(opening.topics.count() == 3)
        assert(opening.topics.filter(name='test-update-opening-mobile').exists())
        assert(opening.topics.filter(name='test-update-opening-nlp').exists())
        assert(opening.topics.filter(name='test-update-opening-crypto').exists())

    def test_update_opening_empty_data(self):
        user, company, employee, opening_id = self._setup()

        factory = APIRequestFactory()
        view = UpdateOpeningView.as_view()
        data = {
            'title': ' ',
            'team': ' ',
            'description': '',
            'years_of_experience_min': None,
            'years_of_experience_max': None,
            'programming_languages': [],
            'technologies': [],
            'topics': [],
        }
        request = factory.patch(f'/openings/update/{opening_id}/', data, format='json')
        force_authenticate(request, user=user)
        response = view(request, opening_id=opening_id)

        assert(response.status_code == 200)
        assert(Opening.objects.filter(id=opening_id).exists())

        opening = Opening.objects.get(id=opening_id)

        assert(Opening.objects.filter(opening_created_by=employee).exists())
        assert(opening.opening_created_by == employee)
        assert(Opening.objects.filter(opening_updated_by=employee).exists())
        assert(opening.opening_updated_by == employee)

        assert(opening.title == ' ')
        assert(opening.team == ' ')
        assert(opening.description == '')
        assert(opening.years_of_experience_min == 0)
        assert(opening.years_of_experience_max == 100)

        assert(opening.programming_languages.count() == 3)
        assert(opening.programming_languages.filter(name='test-update-opening-php').exists())
        assert(opening.programming_languages.filter(name='test-update-opening-python').exists())
        assert(opening.programming_languages.filter(name='test-update-opening-go').exists())

        assert(opening.technologies.count() == 3)
        assert(opening.technologies.filter(name='test-update-opening-django').exists())
        assert(opening.technologies.filter(name='test-update-opening-android').exists())
        assert(opening.technologies.filter(name='test-update-opening-ios').exists())

        assert(opening.topics.count() == 3)
        assert(opening.topics.filter(name='test-update-opening-mobile').exists())
        assert(opening.topics.filter(name='test-update-opening-nlp').exists())
        assert(opening.topics.filter(name='test-update-opening-crypto').exists())
        