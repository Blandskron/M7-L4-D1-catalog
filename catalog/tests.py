from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Product


class CatalogSnapshotTests(TestCase):
    def test_snapshot_returns_the_current_schema_fields(self):
        Product.objects.create(sku="SKU-001", name="Cuaderno", unit_price=Decimal("1990.50"))

        response = self.client.get(reverse("catalog_snapshot"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["catalog"][0]["sku"], "SKU-001")
