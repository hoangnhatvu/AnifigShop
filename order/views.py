from django.shortcuts import render, redirect
from django.http import JsonResponse
from cart.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
from product.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def sendEmail(request, order):
    mail_subject = 'Cảm ơn bạn đã đặt hàng!'
    message = render_to_string('order/order_recieved_email.html', {
        'user': request.user,
        'order': order
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

def payments(request):
    try:
        if request.method == 'POST':
            data = request.POST
            order_id = data['orderID']
            trans_id = data['transID']
            payment_method = data['payment_method']
            status = data['status']

            # Lấy bản ghi order
            order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_id)
            # Tạo 1 bản ghi payment
            payment = Payment(
                user=request.user,
                payment_id=trans_id,
                payment_method=payment_method,
                amount_paid=order.order_total,
                status=status,
            )
            payment.save()

            order.payment = payment
            order.is_ordered = True
            order.save()

            # Chuyển hết cart_item thành order_product
            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                order_product = OrderProduct()
                order_product.order_id = order.id
                order_product.payment = payment
                order_product.user_id = request.user.id
                order_product.product_id = item.product_id
                order_product.quantity = item.quantity
                order_product.product_price = item.product.get_price()
                order_product.ordered = True
                order_product.save()

                order_product = OrderProduct.objects.get(id=order_product.id)
                order_product.save()

                # Reduce the quantity of the sold products
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.num_order += item.quantity
                product.save()

            # Xóa hết cart_item
            CartItem.objects.filter(user=request.user).delete()
            # Gửi thư cảm ơn
            sendEmail(request=request, order=order)
            # Phản hồi lại ajax
            data = {
                'order_number': order.order_number,
                'transID': payment.payment_id,
            }
        return JsonResponse({"data": data}, status=200)
    except Exception as e:
        return JsonResponse({"error": e}, status=400)


def place_order(request, total=0, quantity=0):

    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    grand_total = 0
    ship = 0
    for cart_item in cart_items:
        total += (cart_item.product.get_price() * cart_item.quantity)
        quantity += cart_item.quantity
    ship = (2 * total) / 100
    grand_total = total + ship
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address= form.cleaned_data['address']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.ship = ship
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'ship': ship,
                'grand_total': grand_total,
            }
            return render(request, 'order/payments.html', context)
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'order/order_complete.html', context)
    except Exception:
        return redirect('home')
