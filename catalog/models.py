from django.db import models

class Product(models.Model):
    sku = models.CharField(
        max_length=40,
        unique=True,
        db_comment="Identificador estable usado entre sistemas"
    )

    name = models.CharField(
        max_length=120,
        db_comment="Nombre comercial del producto"
    )

    description = models.TextField(
        null=True,
        blank=True,
        db_comment="Descripción extendida del producto"
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        db_comment="Precio unitario con precisión decimal"
    )

    is_active = models.BooleanField(
        default=True,
        db_comment="Control lógico de disponibilidad"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Timestamp de creación del registro"
    )

    class Meta:
        db_table = "catalog_product"
        ordering = ["name"]