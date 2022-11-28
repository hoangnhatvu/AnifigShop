import datetime
from django.shortcuts import render
from django.db.models import Q
from cart.models import Cart, CartItem
from product.models import Product, ReviewRating
# from cart.views import _cart_id
# from order.models import OrderProduct,Order
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

    elif description:
        products = Product.objects.order_by('-created_date').filter(
            Q(description__icontains=description)
            | Q(product_name__icontains=description)
            | Q(firm__icontains=description)
        )
        products_count = products.count()
        context = {
            'paged_products': products,
            'product_count': products_count,
        }
        return render(request, 'store/store.html', context)

    else:
        return render(request, 'store/store.html', {})
    
def product_detail(request, category_slug, product_slug=None):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        # cart = Cart.objects.get(cart_id=_cart_id(request=request))
        # in_cart = CartItem.objects.filter(
        #     cart=cart,
        #     product=single_product
        # ).exists()
    except Exception as e:
        # cart = Cart.objects.create(
        #     cart_id=_cart_id(request)
        # )
        print("hello")

    # try:
    #     orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
    # except Exception:
    #     orderproduct = None

    single_product.num_visit = single_product.num_visit + 1
    # single_product.last_visit = datetime.now()
    single_product.save()
    # reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    context = {
        'single_product': single_product,
        # 'in_cart': in_cart if 'in_cart' in locals() else False,
        # 'orderproduct': orderproduct,
        # 'reviews': reviews,
    }
    return render(request, 'product/product_detail.html', context=context)
# Create your views here.
