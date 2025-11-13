from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from backend.app.models import Category, Product
from backend.api.v1.serializers import (
    CategoryListSerializer,
    CategoryDetailSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
)


@extend_schema_view(
    list=extend_schema(description='List all active categories'),
    retrieve=extend_schema(description='Retrieve a category by slug'),
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Category operations.
    Provides list and detail views for categories.
    """
    
    queryset = Category.objects.filter(is_active=True)
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['parent', 'is_active']
    ordering_fields = ['order', 'created_at']
    ordering = ['order']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategoryListSerializer
    
    def get_queryset(self):
        """Get queryset with proper translations."""
        language = getattr(self.request, 'LANGUAGE_CODE', 'en')
        queryset = self.queryset.active_translations(language)
        
        if self.request.query_params.get('root_only') == 'true':
            queryset = queryset.filter(parent__isnull=True)
        
        return queryset.prefetch_related('children')
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """Get category tree hierarchy."""
        language = getattr(request, 'LANGUAGE_CODE', 'en')
        categories = Category.objects.active_translations(language).filter(
            is_active=True
        ).select_related('parent').prefetch_related('children')
        serializer = CategoryDetailSerializer(
            categories,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(description='List all active products'),
    retrieve=extend_schema(description='Retrieve a product by SKU'),
)
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Product operations.
    Provides list, detail, and search views for products.
    """
    
    queryset = Product.objects.filter(is_active=True)
    lookup_field = 'sku'
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['category__slug', 'is_featured', 'is_active']
    search_fields = ['translations__name', 'translations__description', 'sku']
    ordering_fields = ['price', 'created_at', 'stock_quantity']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    def get_queryset(self):
        """Get queryset with proper translations and filters."""
        language = getattr(self.request, 'LANGUAGE_CODE', 'en')
        queryset = self.queryset.active_translations(language).select_related(
            'category'
        ).prefetch_related('images')
        
        # Filter by category slug
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter in-stock only
        if self.request.query_params.get('in_stock') == 'true':
            queryset = queryset.filter(stock_quantity__gt=0)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products."""
        language = getattr(request, 'LANGUAGE_CODE', 'en')
        limit = int(request.query_params.get('limit', 10))
        products = Product.objects.active_translations(language).filter(
            is_active=True,
            is_featured=True
        ).select_related('category').prefetch_related('images')[:limit]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get products by category slug."""
        category_slug = request.query_params.get('category_slug')
        if not category_slug:
            return Response(
                {'error': 'category_slug parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        language = getattr(request, 'LANGUAGE_CODE', 'en')
        products = Product.objects.active_translations(language).filter(
            category__slug=category_slug,
            is_active=True
        ).select_related('category').prefetch_related('images')
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
