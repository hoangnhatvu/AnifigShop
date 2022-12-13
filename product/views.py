from order.models import OrderProduct
from django.contrib import messages
from product.forms import ReviewForm
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

from product.models import Product, ReviewRating
from cart.models import Cart, CartItem
from cart.views import _cart_id

def product_detail(request, category_slug, product_slug=None):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        cart = Cart.objects.get(cart_id=_cart_id(request=request))
        in_cart = CartItem.objects.filter(
            cart=cart,
            product=single_product
        ).exists()
    except Exception as e:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )

    try:
        orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
    except Exception:
        orderproduct = None

    single_product.num_visit = single_product.num_visit + 1
    single_product.save()
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    context = {
        'single_product': single_product,
        'in_cart': in_cart if 'in_cart' in locals() else False,
        'orderproduct': orderproduct,
        'reviews': reviews,
    }
    return render(request, 'product/product_detail.html', context=context)


def search(request, description):
    if request.method == 'POST':
        seaching = request.POST['searching']
        if seaching:
            products = Product.objects.order_by('-created_date').filter(
                Q(product_name__icontains=seaching)
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
        )
        products_count = products.count()
        context = {
            'paged_products': products,
            'product_count': products_count,
        }
        return render(request, 'store/store.html', context)

    else:
        return render(request, 'store/store.html', {})


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(request, "Cảm ơn! Nhận xét của bạn đã được đăng.")
            return redirect(url)
        except Exception:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Cảm ơn! Nhận xét của bạn đã được cập nhật.")
                return redirect(url)
