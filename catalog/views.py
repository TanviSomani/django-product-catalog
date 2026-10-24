from django.db.models import Q
from django.shortcuts import render

from .models import Category, Product, Tag


def product_list(request):
    products = Product.objects.select_related("category").prefetch_related("tags")
    search_text = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()
    tag_id = request.GET.get("tag", "").strip()

    if search_text:
        products = products.filter(description__icontains=search_text)

    if category_id:
        products = products.filter(category_id=category_id)

    if tag_id:
        products = products.filter(tags__id=tag_id)

    products = products.distinct()

    context = {
        "products": products,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "search_text": search_text,
        "selected_category": category_id,
        "selected_tag": tag_id,
        "result_count": products.count(),
    }
    return render(request, "catalog/product_list.html", context)
