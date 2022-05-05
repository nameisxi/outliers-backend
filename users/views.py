from django.db.models import Case, Value, When, F, Q, Subquery
from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework.generics import ListAPIView

from .models import *
from .serializers import *
from .filters import *


class CandidateList(ListAPIView):
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

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'language' in self.request.query_params.keys():
            languages = self.request.query_params.getlist('language')
            for language in languages:
                queryset = queryset.filter(github_accounts__programming_languages__language__name=language, github_accounts__programming_languages__language_share__gte=0.1)

        if 'topic' in self.request.query_params.keys():
            topics = self.request.query_params.getlist('topic')
            for topic in topics:
                queryset = queryset.filter(github_accounts__topics__topic__name=topic, github_accounts__topics__topic_share__gte=0.1)

        return queryset
