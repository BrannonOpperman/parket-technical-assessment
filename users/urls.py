from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ParketUserViewSet

router = DefaultRouter()
router.register('', ParketUserViewSet, basename='parket-user')

urlpatterns = [
    path('client/<int:client_id>/bulk-delete/', ParketUserViewSet.as_view({'delete': 'bulk_delete'})),
    path('client/<int:client_id>/bulk-upload/', ParketUserViewSet.as_view({'post': 'bulk_upload'})),
    path('', include(router.urls)),
]