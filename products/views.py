import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Product
from django.contrib.auth.decorators import user_passes_test, login_required

# List all categories
def list_categories(request):
    categories = list(Category.objects.values())
    return JsonResponse({"categories": categories})

# List all products
def list_products(request):
    products = list(Product.objects.values())
    return JsonResponse({"products": products})

# Get product detail
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "stock": product.stock,
            "category": product.category.name,
            "image_url": product.image_url
        }
        return JsonResponse({"product": data})
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)



@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def add_category(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        name = data.get("name")
        description = data.get("description", "")
        category = category.objects.create(name=name, description=description)
        return JsonResponse({"message": "Category added", "category": category.name})
    return JsonResponse({"error": "Invalid request"}, status=400)



@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def add_product(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        category_name = data.get("category")
        try:
            category = category.objects.get(name=category_name)
        except category.DoesNotExist:
            return JsonResponse({"error": "Category not found"}, status=404)

        product = product.objects.create(
            category=category,
            name=data.get("name"),
            description=data.get("description", ""),
            price=data.get("price", 0),
            stock=data.get("stock", 0),
            image_url=data.get("image_url", "")
        )
        return JsonResponse({"message": "Product added", "product": product.name})
    return JsonResponse({"error": "Invalid request"}, status=400)
