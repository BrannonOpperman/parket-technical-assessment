from rest_framework import serializers
from .models import ParketUser

class ParketUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParketUser
        fields = ['id', 'first_name', 'last_name', 'email', 'license_plate']
        read_only_fields = ['id', 'client']
