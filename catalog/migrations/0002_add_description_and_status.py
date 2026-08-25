from django.db import migrations, models


class Migration(migrations.Migration):
    """Añade información descriptiva sin invalidar los registros existentes."""

    dependencies = [("catalog", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True, db_comment="Descripción extendida del producto", null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="is_active",
            field=models.BooleanField(db_comment="Control lógico de disponibilidad", default=True),
        ),
    ]
