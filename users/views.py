from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.db.models import Case, When, F, Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


from github.views import scrape, populate
from scores.views import compute
from .models import *
from .serializers import *
from .filters import *


def _parse_and_validate_email_address(email_address):
    if not email_address: return None

    email_address = email_address.lower().strip()

    if email_address and len(email_address) >= 3 and '@' in email_address:
        return email_address

    return None

def _get_email_address_domain(email_address):
    if not email_address or '@' not in email_address: 
        return None

    email_address_parts = email_address.split('@')
    if len(email_address_parts) > 1 and email_address_parts[1]:
        return email_address_parts[1]

    return None

def _parse_and_validate_password(password):
    if not password: return None

    password = password.strip()
    if password and len(password) >= 8:
        return password

    return None

def _get_employees_company(domain):
    try:
        company = Company.objects.get(domain_names__name=domain)
    except Exception as e:
        return None

    return company

def initialize(request):
    # Populate database with Github data
    print("#"*50)
    print('# Scraping the Github REST API...', ' '*16, '#')
    print("#"*50)
    print()
    scrape()
    print()

    # Populate database with Github data
    print("#"*50)
    print('# Populating the database with Github data...', ' '*13, '#')
    print("#"*50)
    print()
    populate()
    print()

    # Compute ranking scores for Candidate objects
    print("#"*50)
    print('# Computing ranking scored for candidates...', ' '*4, '#')
    print("#"*50)
    print()
    compute()


class EmployeeSignupView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email_address = _parse_and_validate_email_address(request.data['email'])
        email_address_domain = _get_email_address_domain(email_address)
        if (not email_address) or (not email_address_domain):
            return HttpResponseBadRequest(f'Invalid email address {email_address}')
        if User.objects.filter(email=email_address).exists():
            return HttpResponseBadRequest(f'Email address already taken {email_address}')

        password = _parse_and_validate_password(request.data['password1'])
        if not password:
            return HttpResponseBadRequest(f'Password is too short')
        if request.data['password1'] != request.data['password2']:
            return HttpResponseBadRequest(f"Passwords don't match")

        company = _get_employees_company(email_address_domain)
        if not company:
            # Note, returning any other HTTP code than one in the email address domain step
            # would let others know which companies are customers of Outliers and which are not.
            return HttpResponseBadRequest(f'Invalid email address {email_address}')
        
        user = User.objects.create_user(
            username=email_address,
            email=email_address, 
            password=password,
        )
        user.save()

        employee = Employee(user=user, company=company)
        employee.save()

        token = Token.objects.create(user=user)

        return Response({"Token": token.key})


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data['email'], 
            password=request.data['password']
        )

        if user is not None:
            token = Token.objects.get(user=user)
            
            return Response({"Token": token.key})
        
        return Response(status=401)


class CandidateList(ListAPIView):
    """
    Returns a list of Candidate objects matching given filters.
    """
    queryset = Candidate.objects.annotate(
        name=Case(
            When(github_accounts__name__isnull=False, then='github_accounts__name'),
            default=None,
        ),
        location=Case(
            When(github_accounts__location__isnull=False, then='github_accounts__location'),
            default=None,
        ),
        email=Case(
            When(github_accounts__email__isnull=False, then='github_accounts__email'),
            default=None,
        ),
        github_url=F('github_accounts__profile_html_url'),
        linkedin_url=Case(
            When(github_accounts__website__icontains='linkedin', then='github_accounts__website'),
            default=None,
        ),
        website_url=Case(
            When(Q(github_accounts__website__isnull=False) & ~Q(github_accounts__website__icontains='linkedin'), then='github_accounts__website'),
            default=None,
        ),
        employer=Case(
            When(github_accounts__company__isnull=False, then='github_accounts__company'),
            default=None,
        ),
        verified_job_looker=Case(
            When(github_accounts__hireable__isnull=False, then='github_accounts__hireable'),
            default=None,
        ),
    )

    serializer_class = CandidateSerializer
    filterset_class = CandidateFilter
