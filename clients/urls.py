from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, AdminUserViewSet

router = DefaultRouter()
router.register('admin-users', AdminUserViewSet, basename='admin-user')
router.register('', ClientViewSet, basename='client')

urlpatterns = [
    path('', include(router.urls)),
]
