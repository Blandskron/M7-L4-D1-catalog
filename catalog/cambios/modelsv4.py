from django.db import models

class Product(models.Model):
    sku = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)

    # Renombrado lógico del campo
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        db_comment="Precio unitario final"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "catalog_product"
        ordering = ["name"]