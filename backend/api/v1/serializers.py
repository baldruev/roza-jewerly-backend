from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from backend.app.models import Category, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for Product Images."""
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'order', 'is_primary']
        read_only_fields = ['id']


class CategoryListSerializer(TranslatableModelSerializer):
    """Serializer for Category list view."""
    
    translations = TranslatedFieldsField(shared_model=Category)
    children_count = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'slug', 'translations', 'parent', 
            'is_active', 'order', 'children_count', 'products_count'
        ]
        read_only_fields = ['id', 'slug']
    
    def get_children_count(self, obj):
        """Get number of child categories."""
        return obj.children.filter(is_active=True).count()
    
    def get_products_count(self, obj):
        """Get number of products in category."""
        return obj.products.filter(is_active=True).count()


class CategoryDetailSerializer(TranslatableModelSerializer):
    """Serializer for Category detail view."""
    
    translations = TranslatedFieldsField(shared_model=Category)
    children = serializers.SerializerMethodField()
    full_path = serializers.CharField(source='get_full_path', read_only=True)
    
    class Meta:
        model = Category
        fields = [
            'id', 'slug', 'translations', 'parent', 
            'is_active', 'order', 'children', 'full_path',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    def get_children(self, obj):
        """Get child categories."""
        children = obj.children.filter(is_active=True)
        return CategoryListSerializer(children, many=True, context=self.context).data


class ProductListSerializer(TranslatableModelSerializer):
    """Serializer for Product list view."""
    
    translations = TranslatedFieldsField(shared_model=Product)
    category = CategoryListSerializer(read_only=True)
    primary_image = serializers.SerializerMethodField()
    effective_price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'translations', 'category', 
            'price', 'discount_price', 'effective_price',
            'stock_quantity', 'is_in_stock', 'is_featured',
            'primary_image', 'material', 'weight'
        ]
        read_only_fields = ['id', 'sku']
    
    def get_primary_image(self, obj):
        """Get primary product image."""
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return ProductImageSerializer(primary_image).data
        first_image = obj.images.first()
        if first_image:
            return ProductImageSerializer(first_image).data
        return None


class ProductDetailSerializer(TranslatableModelSerializer):
    """Serializer for Product detail view."""
    
    translations = TranslatedFieldsField(shared_model=Product)
    category = CategoryDetailSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    effective_price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'translations', 'category', 
            'price', 'discount_price', 'effective_price',
            'stock_quantity', 'is_in_stock', 'is_featured',
            'images', 'material', 'weight',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'sku', 'created_at', 'updated_at']
