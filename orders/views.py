from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from userprofile.models import Address
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from carts.models import CartItem
from category.models import Product,Variations
from orders.models import Order, OrderItem
from offers.models import Coupon
from django.contrib import messages
from django.core.paginator import Paginator
from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.views.generic import View
from django.template.loader import get_template
from category.models import Category
from django.shortcuts import get_object_or_404

# Create your views here.

@login_required(login_url='login-page')
def order_summary(request):
    categories = Category.objects.all()
    orders = Order.objects.filter(user=request.user).order_by('created_at')[::-1]
    paginator = Paginator(orders, 8)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)

    # Fetch all related OrderItem objects for the orders
    order_items = OrderItem.objects.filter(order__in=orders)

    return render(request, 'customerapp/ordersummary.html', {
        'orders': paged_orders,
        'order_items': order_items,  # Pass the order_items to the template context
        'category': categories
    })

# @login_required(login_url='login-page')
# def view_order(request, id):
#     categories = Category.objects.all()
#     order = Order.objects.filter(id=id, user=request.user).first()
#     order_items = OrderItem.objects.filter(order=order)

#     return render(request, 'customerapp/view_order.html', {
#         'order': order,
#         'order_items': order_items,
#         'category': categories,
#     })


@login_required(login_url='login-page')

def orderview(request, id):
    categories = Category.objects.all()
    # Retrieve the specific order using get_object_or_404
    orders = get_object_or_404(Order, id=id, user=request.user)
    order_items = OrderItem.objects.filter(order=orders)
    
    # Calculate the coupon_price for each order_item
    for order_item in order_items:
        order_item.coupon_price = (order_item.price*order_item.quantity )- orders.total_price
    
    saved = request.session.get('offer_applied', 0)

    context = {
        'orders': orders,
        'order_items': order_items,
        'category': categories,
        'saved':saved,
    }
    return render(request, 'customerapp/orderview.html', context)


def place_order(request):
    if request.method == 'POST':
        neworder = Order()
        neworder.user = request.user
        address = Address.objects.get(id=request.POST.get('address'))
        neworder.address = address
        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        cart_items = CartItem.objects.filter(user=request.user)
        cart_total_price = 0
        for cart_item in cart_items:
            product = get_object_or_404(Product, id=cart_item.product_id)
            variations = cart_item.variations.all()
            coupon =cart_item.coupon

            offer_price = product.offer_price() if not variations else variations.first().product.offer_price()

            cart_total_price += (offer_price["new_price"] * cart_item.quantity)

            if cart_item.coupon_discount:
                cart_total_price = cart_item.coupon_discount

            # Save the 'Order' instance before creating 'OrderItem'
            neworder.total_price = cart_total_price
            neworder.save()

            # Create OrderItem and associate it with the Order
            order_item = OrderItem.objects.create(
                order=neworder,
                product=product,
                variation=variations.first() if variations else None,
                price=offer_price["new_price"],
                quantity=cart_item.quantity,
                coupon=coupon
                
            )

            # Update the stock of the product or its variation after the order is placed
            if variations:
                variation = variations.first()
                variation.stock -= cart_item.quantity
                variation.save()
            else:
                product.stock -= cart_item.quantity
                product.save()
                
             # Set the coupon amount for the OrderItem
            if coupon:
                coupon_amount = coupon.discount * cart_item.quantity
                order_item.coupon_amount = coupon_amount
                order_item.save()

        # Clear the user's cart after placing the order
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request, 'Your order has been placed successfully')

        pay_mode = request.POST.get('payment_mode')
        if pay_mode == "Razorpay" :
            return JsonResponse({'status': 'Your order has been placed successfully'})

    return redirect('order_summary')


def order_cancel(request,id):
    order_item=OrderItem.objects.get(id=id)
    product=Product.objects.get(id=order_item.product_id)
    product.stock+=order_item.quantity
    product.save()
    order_item.status="Order Cancelled"
    order_item.save()
    
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def proceed_to_pay(request):
    cart_items=CartItem.objects.filter(user=request.user)
    cart_total_price=0
    for cart_item in cart_items:
        if cart_item.product.offer_price():
            offer_price=Product.offer_price(cart_item.product)
            cart_total_price+=(offer_price["new_price"]*cart_item.quantity)
        else:
            cart_total_price+=(cart_item.product.price*cart_item.quantity)
        price=cart_total_price
        print(price,'///////')
        if cart_item.coupon_discount:
            cart_total_price=cart_item.coupon_discount
        else:
            cart_total_price=price
    return JsonResponse({
        'total_price':cart_total_price
    })

def order_status_change(request):
    id=request.POST['id']
    status=request.POST['status']
    order_item=OrderItem.objects.get(id=id)
    order_item.status=status
    order_item.save()
    return JsonResponse({"success":True})

def return_order(request,id):
    order_item=OrderItem.objects.get(id=id)
    order_item.status="Requested For Return"
    order_item.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def accept_return(request,id):
    order_item=OrderItem.objects.get(id=id)
    order_item.status="Refund Initiated"
    product_id=order_item.product_id
    product=Product.objects.get(id=product_id)
    product.stock+=order_item.quantity
    order_item.save()
    product.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])




class generateInvoice(View):
    def get(self, request, id, *args, **kwargs):
        try:
            orders = Order.objects.get(id=id, user=request.user)
            order_items = OrderItem.objects.filter(order=orders)
        except Order.DoesNotExist:
            return HttpResponse("505 not found")

        # Retrieve the 'saved' amount from the session
        saved = request.session.get('offer_applied', 0)
        
        for order_item in order_items:
            order_item.coupon_price = (order_item.price*order_item.quantity) - orders.total_price
            productprice = (order_item.price*order_item.quantity)+saved
        coupon = order_item.coupon_price
        pp = productprice
        data = {
            'order_id': orders.id,
            'date': str(orders.created_at),
            'name': orders.user.first_name,
            'address': orders.address.address,
            'total_price': orders.total_price,
            'transaction_id': orders.payment_id,
            'payment_mode': orders.payment_mode,
            'user_email': orders.user.email,
            'orders': orders,
            'saved': saved,  # Pass the 'saved' amount to the data dictionary
            'coupon': coupon,  # Calculate the applied coupon product amount
            'total_paid_amount': orders.total_price - saved,  # Calculate the total paid amount (after applying the discount)
            'pp':pp,
        }

        # Add a list to store product prices
        product_prices = []

        # Loop through the order items to get product prices
        for order_item in orders.orderitem_set.all():
            product_prices.append(order_item.product.price)

        # Pass the product_prices list to the data dictionary
        data['product_prices'] = product_prices

        pdf = render_to_pdf('customerapp/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')



def render_to_pdf(template_src,context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

