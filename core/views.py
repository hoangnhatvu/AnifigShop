from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from product.models import Product, Category

def HomeView(request):
    return render(request, 'homepage/index.html')