from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ParketUser
from .serializers import ParketUserSerializer
from clients.models import Client

class ParketUserViewSet(viewsets.ModelViewSet):
    serializer_class = ParketUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ParketUser.objects.filter(client__administrators=self.request.user)

    def perform_create(self, serializer):
        client = Client.objects.get(id=serializer.validated_data['client_id'])
        serializer.save(client=client)