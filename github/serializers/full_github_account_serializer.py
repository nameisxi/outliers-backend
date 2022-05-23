from rest_framework import serializers

from technologies.serializers import ProgrammingLanguageSerializer, TechnologySerializer, TopicSerializer
from ..models import *
from .github_account_serializer import GithubAccountLanguageSerializer, GithubAccountTechnologySerializer, GithubAccountTopicSerializer
from .github_repo_serializer import GithubRepoSerializer


class FullGithubAccountSerializer(serializers.ModelSerializer):
    programming_languages = GithubAccountLanguageSerializer(many=True, read_only=True)
    technologies = GithubAccountTechnologySerializer(many=True, read_only=True)
    topics = GithubAccountTopicSerializer(many=True, read_only=True)
    repos = GithubRepoSerializer(many=True, read_only=True)

    class Meta:
        model = GithubAccount
        fields = '__all__'
        depth = 1
