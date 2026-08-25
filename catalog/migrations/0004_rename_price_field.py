from django.db import migrations, models


class Migration(migrations.Migration):
    """Aclara el significado del precio sin perder los datos almacenados."""

    dependencies = [("catalog", "0003_change_price_to_decimal")]

    operations = [
        migrations.RenameField(model_name="product", old_name="price", new_name="unit_price"),
        migrations.AlterField(
            model_name="product",
            name="unit_price",
            field=models.DecimalField(
                db_comment="Precio unitario con precisión decimal",
                decimal_places=2,
                max_digits=12,
            ),
        ),
    ]
