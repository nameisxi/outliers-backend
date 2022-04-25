from rest_framework import serializers

from ..models import *
# from github.serializers import GithubAccountSerializer


class CandidateSerializer(serializers.ModelSerializer):
    # github_accounts = GithubAccountSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'
        