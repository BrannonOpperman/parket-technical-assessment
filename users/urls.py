from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ParketUserViewSet

router = DefaultRouter()
router.register('', ParketUserViewSet, basename='parket-user')

urlpatterns = [
    path('', include(router.urls)),
]