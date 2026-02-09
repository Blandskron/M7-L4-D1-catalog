from django.db import models

class Product(models.Model):
    sku = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)

    # Cambio crítico de tipo de dato
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        db_comment="Precio con precisión decimal"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "catalog_product"
        ordering = ["name"]