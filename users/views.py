from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ParketUser
from .serializers import ParketUserSerializer
from clients.models import Client

class ParketUserViewSet(viewsets.ModelViewSet):
    serializer_class = ParketUserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return ParketUser.objects.filter(client__administrators=self.request.user)

    def perform_create(self, serializer):
        client = Client.objects.get(id=serializer.validated_data['client_id'])
        serializer.save(client=client)

    @action(detail=False, methods=['delete'], url_path='bulk-delete')
    def bulk_delete(self, request, client_id=None):
        try:
            Client.objects.get(id=client_id, administrators=request.user)
        except Client.DoesNotExist:
            return Response({
                'error': 'invalid client id'
            }, status=status.HTTP_404_NOT_FOUND)

        users_to_delete = self.get_queryset().filter(client_id=client_id)
        count = users_to_delete.count()
        users_to_delete.delete()

        return Response({
            'message': f'Successfully deleted {count} users',
            'deleted_count': count
        }, status=status.HTTP_200_OK)