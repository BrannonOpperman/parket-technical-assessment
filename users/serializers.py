from rest_framework import serializers
from .models import ParketUser
from clients.models import Client

class ParketUserSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ParketUser
        fields = ['id', 'first_name', 'last_name', 'email', 'license_plate', 'client_id']
        read_only_fields = ['id']

    def validate_client_id(self, value):
        # Ensure the client exists and that the user is an administrator for them
        try:
            client = Client.objects.get(id=value)
            if not client.administrators.filter(id=self.context['request'].user.id).exists():
                raise serializers.ValidationError("You are not an administrator for this client")
            return value
        except Client.DoesNotExist:
            raise serializers.ValidationError("Invalid client ID")
