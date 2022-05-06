from django.db.models import Case, When, F, Q
from rest_framework.generics import ListAPIView

from github.views import populate
from scores.views import compute
from .models import *
from .serializers import *
from .filters import *


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
    )

    serializer_class = CandidateSerializer
    filterset_class = CandidateFilter

# def initialize(request):
#     # Populate database with Github data
#     populate()
#     # Compute ranking scores for Candidate objects
#     compute()