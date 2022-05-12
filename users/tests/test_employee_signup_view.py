import json
from unicodedata import name

from rest_framework.test import APITestCase, APIRequestFactory

from ..models import *
from ..views import EmployeeSignupView


class TestEmployeeSignupView(APITestCase):
    company = Company(name='Test Company')
    company.save()

    domain_name1 = CompanyDomainName(
        company=company,
        name='testcompany.com'
    )
    domain_name1.save()

    domain_name2 = CompanyDomainName(
        company=company,
        name='testcompanysales.com'
    )
    domain_name2.save()

    domain_name3 = CompanyDomainName(
        company=company,
        name='testcompanymarketing.com'
    )
    domain_name3.save()

    def test_signup(self):
        factory = APIRequestFactory()
        view = EmployeeSignupView.as_view()
        email = 'test@testcompany.com'
        password = 'test1234'
        data = {
            'email': email,
            'password1': password,
            'password2': password,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 200)
        assert(User.objects.filter(email=email).exists())
        assert(Employee.objects.filter(user=User.objects.get(email=email)).exists())
        assert(Company.objects.filter(employees__user=User.objects.get(email=email)).count() == 1)


    def test_signup_unknown_email_domain(self):
        factory = APIRequestFactory()
        view = EmployeeSignupView.as_view()
        email = 'test@random.com'
        password = 'test1234'
        data = {
            'email': email,
            'password1': password,
            'password2': password,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 400)
        assert(User.objects.filter(email=email).exists() == False)
        assert(Employee.objects.filter(user__email=email).exists() == False)
        assert(Company.objects.filter(employees__user__email=email).count() == 0)

    def test_signup_already_used_email_address(self):
        factory = APIRequestFactory()
        view = EmployeeSignupView.as_view()
        email = 'test@testcompanysales.com'
        password = 'test1234'
        data = {
            'email': email,
            'password1': password,
            'password2': password,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 200)
        assert(User.objects.filter(email=email).exists())
        assert(Employee.objects.filter(user=User.objects.get(email=email)).exists())
        assert(Company.objects.filter(employees__user=User.objects.get(email=email)).count() == 1)

        data = {
            'email': email,
            'password1': password,
            'password2': password,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 400)
        assert(User.objects.filter(email=email).exists())
        assert(Employee.objects.filter(user__email=email).exists())
        assert(Company.objects.filter(employees__user__email=email).count() == 1)

    def test_signup_missing_email_address(self):
        factory = APIRequestFactory()
        view = EmployeeSignupView.as_view()
        email = ''
        password = 'test1234'
        data = {
            'email': '',
            'password1': password,
            'password2': password,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 400)
        assert(User.objects.filter(email=email).exists() == False)
        assert(Employee.objects.filter(user__email=email).exists() == False)
        assert(Company.objects.filter(employees__user__email=email).count() == 0)

        email = None
        data = {
            'email': email,
            'password1': password,
            'password2': password,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 400)
        assert(User.objects.filter(email=email).exists() == False)
        assert(Employee.objects.filter(user__email=email).exists() == False)

    def test_signup_unmatching_passwords(self):
        factory = APIRequestFactory()
        view = EmployeeSignupView.as_view()
        email = 'test@testcompanymarketing.com'
        password1 = 'test1234'
        password2 = 'test4321'
        data = {
            'email': email,
            'password1': password1,
            'password2': password2,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 400)
        assert(User.objects.filter(email=email).exists() == False)
        assert(Employee.objects.filter(user__email=email).exists() == False)
        assert(Company.objects.filter(employees__user__email=email).count() == 0)

    def test_signup_too_short_password(self):
        factory = APIRequestFactory()
        view = EmployeeSignupView.as_view()
        email = 'test@testcompanymarketing.com'
        password = 'test123'
        data = {
            'email': email,
            'password1': password,
            'password2': password,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 400)
        assert(User.objects.filter(email=email).exists() == False)
        assert(Employee.objects.filter(user__email=email).exists() == False)
        assert(Company.objects.filter(employees__user__email=email).count() == 0)

    def test_signup_missing_password(self):
        factory = APIRequestFactory()
        view = EmployeeSignupView.as_view()
        email = 'test@testcompanymarketing.com'
        password1 = ''
        password2 = 'test1234'
        data = {
            'email': '',
            'password1': password1,
            'password2': password2,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 400)
        assert(User.objects.filter(email=email).exists() == False)
        assert(Employee.objects.filter(user__email=email).exists() == False)
        assert(Company.objects.filter(employees__user__email=email).count() == 0)

        password1 = 'test1234'
        password2 = ''
        data = {
            'email': '',
            'password1': password1,
            'password2': password2,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 400)
        assert(User.objects.filter(email=email).exists() == False)
        assert(Employee.objects.filter(user__email=email).exists() == False)
        assert(Company.objects.filter(employees__user__email=email).count() == 0)

        password1 = ''
        password2 = ''
        data = {
            'email': '',
            'password1': password1,
            'password2': password2,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 400)
        assert(User.objects.filter(email=email).exists() == False)
        assert(Employee.objects.filter(user__email=email).exists() == False)
        assert(Company.objects.filter(employees__user__email=email).count() == 0)       

        password1 = None
        password2 = 'test1234'
        data = {
            'email': '',
            'password1': password1,
            'password2': password2,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 400)
        assert(User.objects.filter(email=email).exists() == False)
        assert(Employee.objects.filter(user__email=email).exists() == False)
        assert(Company.objects.filter(employees__user__email=email).count() == 0)

        password1 = 'test1234'
        password2 = None
        data = {
            'email': '',
            'password1': password1,
            'password2': password2,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 400)
        assert(User.objects.filter(email=email).exists() == False)
        assert(Employee.objects.filter(user__email=email).exists() == False)
        assert(Company.objects.filter(employees__user__email=email).count() == 0)

        password1 = None
        password2 = None
        data = {
            'email': '',
            'password1': password1,
            'password2': password2,
        }
        request = factory.post('/employee/signup/', data, format='json')
        response = view(request)

        assert(response.status_code == 400)
        assert(User.objects.filter(email=email).exists() == False)
        assert(Employee.objects.filter(user__email=email).exists() == False)
        assert(Company.objects.filter(employees__user__email=email).count() == 0)
        