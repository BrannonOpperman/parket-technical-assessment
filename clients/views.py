from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return []

    # limit the allowed functionality to POST requests for creating new clients only
    http_method_names = ['post']

    def perform_create(self, serializer):
        serializer.save()
