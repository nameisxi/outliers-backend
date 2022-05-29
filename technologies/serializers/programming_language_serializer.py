from rest_framework import serializers

from ..models import *


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = ['name', 'color']
