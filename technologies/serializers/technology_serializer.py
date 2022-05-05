from rest_framework import serializers

from ..models import *


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ['name']
        