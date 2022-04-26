from rest_framework import serializers

from technologies.models import ProgrammingLanguage
from ..models import *


class GithubAccountLanguageSerializer(serializers.ModelSerializer):
    language = ProgrammingLanguage()
    class Meta:
        model = GithubAccountLanguage
        fields = '__all__'


class GithubAccountSerializer(serializers.ModelSerializer):
    programming_languages = GithubAccountLanguageSerializer(many=True, read_only=True)

    class Meta:
        model = GithubAccount
        fields = '__all__'
        