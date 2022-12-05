from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from product.models import Product
from cart.models import Cart, CartItem
from account.models import UserProfile


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)    # Get object product
    if current_user.is_authenticated:
        if CartItem.objects.filter(product=product, user=current_user).exists():  
            cart_item = CartItem.objects.get(product=product, user=current_user)        
            cart_item.quantity += 1           
        else:
            cart_item = CartItem.objects.create(
                product=product,
                user=current_user,
                quantity=1
            )   
        cart_item.save()
        return redirect('cart')
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()        
        
        if CartItem.objects.filter(product=product, cart=cart).exists():  
            cart_item = CartItem.objects.get(product=product, user=current_user)        
            cart_item.quantity += 1           
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1
            )        
        cart_item.save()
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                id=cart_item_id,
                product=product,
                user=request.user
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                id=cart_item_id,
                product=product,
                cart=cart
            )
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Exception:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                id=cart_item_id,
                product = product,
                user=request.user
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
            cart_item = CartItem.objects.get(
                id=cart_item_id,
                product=product,
                cart=cart
            )
        cart_item.delete()
    except Exception:
        pass
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request=request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.get_price() * cart_item.quantity
            quantity += cart_item.quantity
        ship = total * 2 / 100
        grand_total = total + ship
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'ship': ship if "ship" in locals() else "",
        'grand_total': grand_total if "ship" in locals() else 0,
    }
    return render(request, 'cart/cart.html', context=context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.get_price() * cart_item.quantity
            quantity += cart_item.quantity
        ship = total * 2 / 100
        grand_total = total + ship
    except ObjectDoesNotExist:
        pass    # Chỉ bỏ qua
    user = request.user
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'ship': ship if "ship" in locals() else "",
        'grand_total': grand_total,
        'user': user,
        'user_profile': user_profile,
    }
    return render(request, 'cart/checkout.html', context=context)
