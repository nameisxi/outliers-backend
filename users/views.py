from django.db.models import Case, Value, When, F, Q, Subquery
from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework.generics import ListAPIView

from .models import *
from .serializers import *
from .filters import *


class CandidateList(ListAPIView):
    # query = """
    # SELECT 
    #     CASE
    #         WHEN github_githubaccount.name IS NOT NULL THEN github_githubaccount.name
    #     END CASE AS name,

    #     CASE
    #         WHEN github_githubaccount.location IS NOT NULL THEN github_githubaccount.location
    #     END CASE AS location,

    #     CASE
    #         WHEN github_githubaccount.email IS NOT NULL THEN github_githubaccount.email
    #     END CASE AS email,

    #     github_githubaccount.profile_html_url AS github_url,

    #     CASE
    #         WHEN github_githubaccount.website LIKE '%linkedin%' THEN github_githubaccount.website
    #     END CASE AS linkedin_url,

    #     CASE
    #         WHEN github_githubaccount.website IS NOT NULL AND NOT LIKE '%linkedin%' THEN github_githubaccount.website
    #     END CASE AS website_url,

    #     CASE
    #         WHEN github_githubaccount.company IS NOT NULL THEN github_githubaccount.company
    #     END CASE AS current_employer

    # FROM users_candidate
    # LEFT JOIN github_githubaccount 
    # ON user_candidate.id = 
    # """
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
    # filterset_class = CandidateFilter


def users_languages(request):
    return 