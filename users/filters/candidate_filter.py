import django_filters as filters

from ..models import *


class CandidateFilter(filters.FilterSet):
    class Meta:
        model = Candidate
        exclude = ['created_at', 'updated_at', 'work_score', 'popularity_score', 'hireability_score', 'fit_score']
        
    @property
    def qs(self):
        queryset = super().qs
        if 'language' in self.request.query_params.keys():
            languages = self.request.query_params.getlist('language')
            for language in languages:
                queryset = queryset.filter(github_accounts__programming_languages__language__name=language.lower(), github_accounts__programming_languages__language_share__gte=0.1)

        if 'topic' in self.request.query_params.keys():
            topics = self.request.query_params.getlist('topic')
            for topic in topics:
                queryset = queryset.filter(github_accounts__topics__topic__name=topic.lower(), github_accounts__topics__topic_share__gte=0.1)

        return queryset
