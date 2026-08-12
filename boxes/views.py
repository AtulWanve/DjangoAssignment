import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_list_or_404
from .models import Box, Product
from .packing import pack_order_into_box

@csrf_exempt
@require_POST
def recommend_box_view(request):
    """
    Expects a JSON payload like: {"product_ids": [1, 2, 2, 5]}
    Returns the cheapest box that can fit all products.
    """
    try:
        data = json.loads(request.body)
        product_ids = data.get('product_ids', [])
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)

    if not isinstance(product_ids, list) or not product_ids:
        return JsonResponse({"error": "Please provide a non-empty list of 'product_ids'."}, status=400)

    # Fetch products. If an ID doesn't exist, we fail gracefully
    products = []
    for pid in product_ids:
        try:
            products.append(Product.objects.get(id=pid))
        except Product.DoesNotExist:
            return JsonResponse({"error": f"Product with ID {pid} does not exist."}, status=404)

    # Fetch all boxes, ordered by cost (cheapest first)
    # The algorithm is greedy for price, so the first box that fits is the winner!
    available_boxes = Box.objects.order_by('cost')

    if not available_boxes.exists():
        return JsonResponse({"error": "No boxes are configured in the system."}, status=500)

    # Test each box from cheapest to most expensive
    for box in available_boxes:
        if pack_order_into_box(box, products):
            return JsonResponse({
                "recommended_box_id": box.id,
                "box_name": box.name,
                "cost": str(box.cost),
                "status": "success"
            }, status=200)

    # If the loop finishes, no box was large enough or strong enough
    return JsonResponse({
        "error": "No available box can fit this order.",
        "status": "failed"
    }, status=400)
