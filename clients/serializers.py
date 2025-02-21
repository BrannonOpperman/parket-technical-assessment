from rest_framework import serializers
from django.contrib.auth.models import User, Permission
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name']
        read_only_fields = ['id']

class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    client_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'client_id']
        read_only_fields = ['id']

    def create(self, validated_data):
        client_id = validated_data.pop('client_id')
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.is_staff = True

        # Add required permissions for ParketUser model
        from users.models import ParketUser
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(ParketUser)
        Permission.objects.filter(content_type=content_type).values_list('codename', flat=True)
        content_type = ContentType.objects.get_for_model(ParketUser)
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=['add_parketuser', 'change_parketuser', 'view_parketuser', 'delete_parketuser']
        )
        user.user_permissions.add(*permissions)

        user.save()

        # Link administrator user to client
        try:
            client = Client.objects.get(id=client_id)
            client.administrators.add(user)
        except Client.DoesNotExist:
            user.delete()
            raise serializers.ValidationError({"client_id": f"Invalid client ID"})

        return user