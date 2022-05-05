import django_filters as filters

from ..models import *
from technologies.models import ProgrammingLanguage, Technology, Topic


class CandidateFilter(filters.FilterSet):
    # language_share = filters.NumberFilter(
    #     field_name='github_accounts__programming_languages__language_share',
    #     lookup_expr='gte',
    # )

    # language_choices = [(language, language) for language in ProgrammingLanguage.objects.values_list('name', flat=True).distinct()]
    # language = filters.MultipleChoiceFilter(
    #     field_name='github_accounts__programming_languages__language__name',
    #     lookup_expr='icontains',
    #     conjoined=True,
    #     choices=language_choices,
    # )

    # technology_choices = [(technology, technology) for technology in Technology.objects.values_list('name', flat=True).distinct()]
    # technology = filters.MultipleChoiceFilter(
    #     field_name='github_accounts__technologies__technology__name',
    #     lookup_expr='icontains',
    #     conjoined=False,
    #     choices=technology_choices,
    # )

    topic_choices = [(topic, topic) for topic in Topic.objects.values_list('name', flat=True).distinct()]
    topic = filters.MultipleChoiceFilter(
        field_name='github_accounts__topics__topic__name',
        lookup_expr='icontains',
        conjoined=False,
        choices=topic_choices,
    )

    class Meta:
        model = Candidate
        exclude = ['created_at', 'updated_at', 'work_score', 'popularity_score', 'hireability_score', 'fit_score']
        
    # @property
    # def qs(self):
    #     parent = super().qs
    #     print("START", parent.count())
    #     if 'language' in self.request.query_params.keys():
    #         languages = self.request.query_params.getlist('language')
    #         print("LANGUAGE:", languages)
    #         for language in languages:
    #             print(language)
    #             print("Before:", parent.count())
    #             specific_languages = parent.filter(github_accounts__programming_languages__language__name=language)
    #             parent = specific_languages.filter(github_accounts__programming_languages__language_share__gt=0.1)
    #             print("After:", parent.count())

    #     print("END", parent.count())
    #     return parent
