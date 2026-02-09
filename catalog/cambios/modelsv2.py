from django.db import models

class Product(models.Model):
    sku = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=120)

    # Nuevo campo: descripción opcional
    description = models.TextField(
        null=True,
        blank=True,
        db_comment="Descripción extendida agregada en evolución 2"
    )

    price = models.IntegerField()

    # Nuevo campo con default para no romper datos existentes
    is_active = models.BooleanField(
        default=True,
        db_comment="Control lógico de disponibilidad"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "catalog_product"
        ordering = ["name"]