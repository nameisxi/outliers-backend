from rest_framework import serializers

from .user_serializer import UserSerializer
from ..models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = '__all__'
        