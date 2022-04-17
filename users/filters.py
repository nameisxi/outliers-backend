import django_filters as filters

from .models import *


class  CandidateFilter(filters.FilterSet):
    programming_languages = filters.CharFilter(field_name='github_account__programming_languages', lookup_expr='icontains')
    technologies = filters.CharFilter(field_name='github_account__technologies', lookup_expr='icontains')
    
    class Meta:
        model = Candidate
        fields = ['programming_languages', 'technologies']