from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ParketUser
from .serializers import ParketUserSerializer

class ParketUserViewSet(viewsets.ModelViewSet):
    serializer_class = ParketUserSerializer
    permission_classes = [IsAuthenticated]

    # Filter users by the client of the authenticated user
    def get_queryset(self):
        return ParketUser.objects.filter(client__administrators=self.request.user)
