from rest_framework import serializers

from .models import *


class GithubAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubAccount
        fields = '__all__'

    
class CandidateSerializer(serializers.ModelSerializer):
    github_accounts = GithubAccountSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'

        