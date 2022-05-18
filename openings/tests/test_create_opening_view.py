from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from users.models import Employee, Company, CompanyDomainName
from technologies.models import ProgrammingLanguage, Technology, Topic, programming_language
from ..models import *
from ..views import *


class TestCreateOpeningView(APITestCase):
    def _setup(self):
        user = User.objects.create(
            username='testuser2',
            email='testuser2@company1.com'
        )
        user.set_password('test1234')
        user.save()

        company = Company(name='company1')
        company.save()

        domain = CompanyDomainName(company=company, name='company1.com')
        domain.save()

        employee = Employee(user=user, company=company)
        employee.save()

        programming_language = ProgrammingLanguage(name='test-create-opening-php')
        programming_language.save()
        programming_language = ProgrammingLanguage(name='test-create-opening-python')
        programming_language.save()
        programming_language = ProgrammingLanguage(name='test-create-opening-java')
        programming_language.save()

        technology = Technology(name='test-create-opening-django')
        technology.save()
        technology = Technology(name='test-create-opening-android')
        technology.save()
        technology = Technology(name='test-create-opening-ios')
        technology.save()

        topic = Topic(name='test-create-opening-mobile')
        topic.save()
        topic = Topic(name='test-create-opening-nlp')
        topic.save()
        technology = Technology(name='test-create-opening-crypto')
        technology.save()

        return user, company, employee

    def test_create_opening(self):
        user, company, employee = self._setup()

        factory = APIRequestFactory()
        view = CreateOpeningView.as_view()
        data = {
            'title': 'Example title',
            'team': 'Example team',
            'description': 'Example description',
            'years_of_experience_min': 0,
            'years_of_experience_max': 99,
            'programming_languages': ['test-create-opening-php', 'test-create-opening-python', 'test-create-opening-go'],
            'technologies': ['test-create-opening-django', 'test-create-opening-android', 'test-create-opening-flask'],
            'topics': ['test-create-opening-mobile', 'test-create-opening-nlp', 'test-create-opening-ml'],
            # 'base_compensation_min': 0,
            # 'base_compensation_max': 100,
            # 'base_compensation_currency': 'usd',
            # 'equity_compensation_min': 0,
            # 'equity_compensation_max': 100,
            # 'equity_compensation_currency': 'krw',
            # 'other_compensation_min': 100,
            # 'other_compensation_max': 100,
            # 'other_compensation_currency': 'eur',
        }
        request = factory.post('/openings/create-opening/', data, format='json')
        force_authenticate(request, user=user)
        response = view(request)

        assert(response.status_code == 200)
        assert(Opening.objects.filter(company=company).exists())
        assert(Opening.objects.filter(company=company).count() == 1)
        assert(Opening.objects.filter(created_by=employee).exists())
        assert(Opening.objects.filter(programming_languages__name='test-create-opening-python').exists())
        assert(Opening.objects.filter(programming_languages__name='test-create-opening-php').exists())
        assert(Opening.objects.filter(programming_languages__name='test-create-opening-java').exists() == False)
        assert(Opening.objects.filter(programming_languages__name='test-create-opening-go').exists() == False)
        assert(Opening.objects.filter(technologies__name='test-create-opening-django').exists())
        assert(Opening.objects.filter(technologies__name='test-create-opening-android').exists())
        assert(Opening.objects.filter(technologies__name='test-create-opening-ios').exists() == False)
        assert(Opening.objects.filter(technologies__name='test-create-opening-flask').exists() == False)
        assert(Opening.objects.filter(topics__name='test-create-opening-mobile').exists())
        assert(Opening.objects.filter(topics__name='test-create-opening-nlp').exists())
        assert(Opening.objects.filter(topics__name='test-create-opening-crypto').exists() == False)
        assert(Opening.objects.filter(topics__name='test-create-opening-ml').exists() == False)

        request = factory.post('/openings/create-opening/', data, format='json')
        force_authenticate(request, user=user)
        response = view(request)

        assert(response.status_code == 200)
        assert(Opening.objects.filter(company=company).count() == 2)
        