from rest_framework import serializers

from ..models import *
from technologies.serializers import *
from github.serializers import GithubAccountSerializer


class CandidateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    location = serializers.CharField()
    email = serializers.CharField()
    github_url = serializers.CharField()
    linkedin_url = serializers.CharField()
    website_url = serializers.CharField()
    employer = serializers.CharField()
    github_accounts = GithubAccountSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'
        