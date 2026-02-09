from django.http import JsonResponse
from .models import Product

def catalog_snapshot(request):
    data = list(
        Product.objects.values(
            "sku",
            "name",
            "unit_price",
            "is_active"
        )
    )
    return JsonResponse(
        {"catalog": data},
        safe=False
    )