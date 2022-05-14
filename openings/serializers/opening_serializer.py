from rest_framework import serializers

from users.serializers import EmployeeSerializer
from ..models import Opening


class OpeningSerializer(serializers.ModelSerializer):
    created_by = EmployeeSerializer()

    class Meta:
        model = Opening
        fields = '__all__'
        