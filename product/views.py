from django.shortcuts import render
from django.db.models import Q
from product.models import Product
def search(request, description):
    if request.method == 'POST':
        seaching = request.POST['searching']
        if seaching:
            products = Product.objects.all().filter(
                Q(product_name__icontains=seaching)
                | Q(firm__icontains=seaching)
            )
        else:
            products = Product.objects.all()
        product_count = products.count()
        context = {
            'paged_products': products,
            'product_count': product_count,
        }
        return render(request, 'store/store.html', context)

    # elif description:
    #     products = Product.objects.order_by('-created_date').filter(
    #         Q(description__icontains=description)
    #         | Q(product_name__icontains=description)
    #         | Q(firm__icontains=description)
    #     )
    #     products_count = products.count()
    #     context = {
    #         'paged_products': products,
    #         'product_count': products_count,
    #     }
        return render(request, 'store/store.html', context)

    else:
        return render(request, 'store/store.html', {})
# Create your views here.
