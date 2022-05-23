from rest_framework import serializers

from technologies.serializers import ProgrammingLanguageSerializer, TechnologySerializer, TopicSerializer
from ..models import *


class GithubRepoLanguageSerializer(serializers.ModelSerializer):
    language = ProgrammingLanguageSerializer()

    class Meta:
        model = GithubRepoLanguage
        fields = ['language', 'language_share', 'language_contribution']
        depth = 1


class GithubRepoTechnologySerializer(serializers.ModelSerializer):
    technology = TechnologySerializer()

    class Meta:
        model = GithubRepoTechnology
        fields = ['technology']
        depth = 1


class GithubRepoTopicSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()

    class Meta:
        model = GithubRepoTopic
        fields = ['topic']
        depth = 1


class GithubRepoSerializer(serializers.ModelSerializer):
    programming_languages = GithubRepoLanguageSerializer(many=True, read_only=True)
    technologies = GithubRepoTechnologySerializer(many=True, read_only=True)
    topics = GithubRepoTopicSerializer(many=True, read_only=True)

    class Meta:
        model = GithubRepo
        fields = '__all__'
        depth = 1
