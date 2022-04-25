from rest_framework import serializers

from ..models import *


class GithubAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubAccount
        fields = '__all__'
        