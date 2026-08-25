from django.db import migrations, models


class Migration(migrations.Migration):
    """Sustituye el precio entero por un importe decimal preciso."""

    dependencies = [("catalog", "0002_add_description_and_status")]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                db_comment="Precio unitario con precisión decimal",
                decimal_places=2,
                max_digits=12,
            ),
        ),
    ]
