from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from product.models import Product, Category

# Create your views here.
def store(request,category_slug=None):
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 10)
    paged_products = paginator.get_page(page)

    context = {
        'paged_products': paged_products,
        'products': products,
    }
    return render(request, 'store/store.html', context = context)
def HomeView(request):
    products = Product.objects.all().filter(is_available=True)
    trend_products = Product.objects.all().order_by('-num_visit')[0:10]
    best_seller_products = Product.objects.all().order_by('-num_order')[0:10]
    context = {
        'products': products,
        'trend_products': trend_products,
        'best_seller_products': best_seller_products
    }
    return render(request, 'homepage/index.html', context=context)

