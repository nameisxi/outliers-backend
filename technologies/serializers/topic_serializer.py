from rest_framework import serializers

from ..models import *


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['name']
        