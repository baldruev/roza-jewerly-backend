from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    """Category model with multi-language support."""
    
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text=_("Display order"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=200),
        description=models.TextField(_("Description"), blank=True),
        meta_title=models.CharField(_("Meta Title"), max_length=200, blank=True),
        meta_description=models.TextField(_("Meta Description"), blank=True),
    )
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['order', 'id']
        indexes = [
            models.Index(fields=['slug', 'is_active']),
        ]
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f"Category {self.id}"
    
    def get_full_path(self):
        """Get full category path (e.g., Parent > Child > Current)."""
        path = [self]
        parent = self.parent
        while parent:
            path.insert(0, parent)
            parent = parent.parent
        return ' > '.join([cat.name for cat in path])


class Product(TranslatableModel):
    """Product model with multi-language support."""
    
    sku = models.CharField(_("SKU"), max_length=100, unique=True, db_index=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Price in EUR")
    )
    discount_price = models.DecimalField(
        _("Discount Price"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    stock_quantity = models.IntegerField(_("Stock Quantity"), default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    weight = models.DecimalField(
        _("Weight (grams)"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    material = models.CharField(_("Material"), max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=200),
        description=models.TextField(_("Description")),
        short_description=models.TextField(_("Short Description"), blank=True),
        meta_title=models.CharField(_("Meta Title"), max_length=200, blank=True),
        meta_description=models.TextField(_("Meta Description"), blank=True),
    )
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sku', 'is_active']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
        ]
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f"Product {self.sku}"
    
    @property
    def effective_price(self):
        """Return discount price if available, otherwise regular price."""
        return self.discount_price if self.discount_price else self.price
    
    @property
    def is_in_stock(self):
        """Check if product is in stock."""
        return self.stock_quantity > 0


class ProductImage(models.Model):
    """Product images model."""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/%Y/%m/')
    alt_text = models.CharField(_("Alt Text"), max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ['order', 'id']
        indexes = [
            models.Index(fields=['product', 'is_primary']),
        ]
    
    def __str__(self):
        return f"Image for {self.product.sku}"
    
    def save(self, *args, **kwargs):
        """Ensure only one primary image per product."""
        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)