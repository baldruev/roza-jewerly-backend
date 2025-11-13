from django.contrib import admin
from parler.admin import TranslatableAdmin, TranslatableTabularInline
from .models import Category, Product, ProductImage

# Регистрация модели Category
@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    """
    Настройки административной панели для модели Category.
    Использует TranslatableAdmin для управления переводами.
    """
    list_display = ('name', 'slug', 'parent', 'is_active', 'order')
    list_filter = ('is_active', 'parent')
    search_fields = ('translations__name', 'slug')
    autocomplete_fields = ['parent']  # Для удобного поиска родительской категории

    # Автоматическое заполнение поля slug на основе названия
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

# Инлайн-модель для изображений продукта
class ProductImageInline(admin.TabularInline):
    """
    Позволяет редактировать изображения прямо на странице продукта.
    """
    model = ProductImage
    extra = 1  # Количество пустых форм для добавления новых изображений
    fields = ('image', 'alt_text', 'order')


# Регистрация модели Product
@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    """
    Настройки административной панели для модели Product.
    """
    list_display = ('name', 'sku', 'category', 'price', 'stock_quantity', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'category')
    search_fields = ('translations__name', 'sku')
    autocomplete_fields = ['category']  # Упрощает выбор категории
    inlines = [ProductImageInline]  # Подключение инлайн-редактора изображений

    # Отключаем автозаполнение slug, так как SKU является основным идентификатором
    def get_prepopulated_fields(self, request, obj=None):
        return {}

# Опционально: отдельная регистрация модели ProductImage
# Это позволит управлять всеми изображениями на отдельной странице.
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Настройки для отдельного управления изображениями продуктов.
    """
    list_display = ('__str__', 'product', 'order')
    list_filter = ('product',)
    search_fields = ('product__sku', 'product__translations__name')
    list_per_page = 20