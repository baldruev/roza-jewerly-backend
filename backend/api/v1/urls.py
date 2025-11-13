from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.api.v1.views import (
    CategoryViewSet,
    ProductViewSet,
)

app_name = 'api_v1'

# Create router and register viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]