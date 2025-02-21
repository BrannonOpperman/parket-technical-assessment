from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import csv
import io
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

    @action(detail=False, methods=['post'], url_path='bulk-upload')
    def bulk_upload(self, request, client_id=None):
        if 'file' not in request.FILES:
            return Response({
                'error': 'No file uploaded'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Client.objects.get(id=client_id, administrators=request.user)
        except Client.DoesNotExist:
            return Response({
                'error': 'invalid client id'
            }, status=status.HTTP_404_NOT_FOUND)

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return Response({
                'error': 'File must be a CSV'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Read and validate headers
        decoded_file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(io.StringIO(decoded_file))

        required_headers = {'first_name', 'last_name', 'email', 'license_plate'}
        try:
            headers = next(csv_data)
            headers = {h.lower().strip() for h in headers}

            if not required_headers.issubset(headers):
                missing_headers = required_headers - headers
                return Response({
                    'error': f'Missing required headers: {", ".join(missing_headers)}'
                }, status=status.HTTP_400_BAD_REQUEST)
        except StopIteration:
            return Response({
                'error': 'Empty CSV file'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Reset file pointer for DictReader
        csv_file.seek(0)
        csv_data = csv.DictReader(io.StringIO(decoded_file))

        users_created = 0
        errors = []

        for row in csv_data:
            try:
                ParketUser.objects.create(
                    first_name=row.get('first_name', '').strip(),
                    last_name=row.get('last_name', '').strip(),
                    email=row.get('email', '').strip(),
                    license_plate=row.get('license_plate', '').strip(),
                    client=client
                )
                users_created += 1
            except Exception as e:
                errors.append(f"Error on row {users_created + 1}: {str(e)}")

        return Response({
            'message': f'Successfully created {users_created} users',
            'users_created': users_created,
            'errors': errors
        }, status=status.HTTP_201_CREATED if users_created > 0 else status.HTTP_400_BAD_REQUEST)