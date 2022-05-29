from rest_framework import serializers

from ..models import *


class GithubContributionsCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubContributionsCalendar
        fields = '__all__'
