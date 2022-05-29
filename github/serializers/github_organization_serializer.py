from rest_framework import serializers

from ..models import *


class GithubOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubOrganization
        fields = '__all__'
