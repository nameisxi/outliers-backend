from rest_framework import serializers

from users.serializers import EmployeeSerializer
from technologies.serializers import ProgrammingLanguageSerializer
from ..models import Opening


class OpeningSerializer(serializers.ModelSerializer):
    opening_created_by = EmployeeSerializer()
    opening_updated_by = EmployeeSerializer()
    programming_languages = ProgrammingLanguageSerializer(many=True)

    class Meta:
        model = Opening
        fields = '__all__'
        