from datetime import date
from math import prod
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from carts.models import CartItem
from category.models import Product,Color, Variations
from carts.models import Cart
from django.contrib.auth.decorators import login_required
from userprofile.models import Address
from category.models import Category,Subcategory,Variations
from django.http import HttpResponseRedirect
from django.contrib import messages
from offers.models import Coupon

# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart


def cart(request,total=0,quantity=0,cart_items=None):
    category=Category.objects.all()
    total_price=0
    saved=0
    subcategory=Subcategory.objects.all()
    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        
        for cart_item in cart_items:
            total_price+=(cart_item.product.price*cart_item.quantity)
            if cart_item.product.offer_price():
                offer_price=Product.offer_price(cart_item.product)
                total+=(offer_price["new_price"]*cart_item.quantity)    
                total=round(total,2)
                
            else:
                total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
            saved=total_price-total
            saved=round(saved,2)
    except:
        pass
    
    request.session['offer_applied'] = saved
    return render(request,'customerapp/cart.html',{
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'category':category,
        'subcategory':subcategory,
        'total_price':total_price,
        'saved':saved
    })

def add_cart(request, product_id):
    product_variation = []
    current_user = request.user
    product = Product.objects.get(id=product_id)

    if request.method == "POST" and request.POST.get('color'):
        c = int(request.POST.get('color'))  # Convert color value to an integer
        try:
            variation = product.variations.get(color__id=c)  # Use the color id for comparison
            if variation.stock > 0:
                product_variation.append(variation)
            else:
                messages.error(request, 'Selected variation is out of stock.')
                return HttpResponseRedirect(request.META["HTTP_REFERER"])
        except Variations.DoesNotExist:
            messages.error(request, 'Invalid variation selected.')
            return HttpResponseRedirect(request.META["HTTP_REFERER"])

    else:
        messages.error(request, 'Choose colour..!!')
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    if current_user.is_authenticated:
        is_cart_item_exists=CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,user=current_user)

            ex_var_list=[]
            id=[]

            for item in cart_item:
                exsisting_varation=item.variations.all()
                ex_var_list.append(list(exsisting_varation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity+=1
                item.save()
            else:
                item=CartItem.objects.create(product=product,quantity=1,user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,

            )
            if len(product_variation) >0:
                cart_item.variations.clear()
                
                cart_item.variations.add(*product_variation)
            cart_item.save()
        messages.success(request,'Added to Cart')
        
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:

        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        is_cart_item_exists=CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,cart=cart)

            ex_var_list=[]
            id=[]

            for item in cart_item:
                exsisting_varation=item.variations.all()
                ex_var_list.append(list(exsisting_varation))
                id.append(item.id)
            if product_variation in ex_var_list:
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity+=1
                item.save()
            else:
                item=CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,

            )
            if len(product_variation) >0:
                cart_item.variations.clear()
                
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        return HttpResponseRedirect(request.META["HTTP_REFERER"])



def delete_cart_item(request,product_id,cart_item_id):
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def decrease_quantity(request):
    product_id = request.GET.get('id')
    id_cart = request.GET.get('c_id')
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(id=id_cart, product=product, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(id=id_cart, product=product, cart=cart)

    qty = cart_item.quantity - 1
    if qty < 1:
        messages.error(request, 'Minimum quantity should be 1.')
        return JsonResponse({'message': 'Minimum quantity should be 1.', 'status': False}, status=400)

    variation = cart_item.variations.first()

    # Check if the new quantity exceeds the stock count
    if variation and qty > variation.stock:
        messages.error(request, 'Exceeded the available stock count.')
        return JsonResponse({'message': 'Exceeded the available stock count.', 'status': False}, status=400)

    cart_item.quantity = qty
    cart_item.save()

    cart_total_price = 0
    cart_items = CartItem.objects.filter(user=request.user, is_active=True) if request.user.is_authenticated else CartItem.objects.filter(cart=cart, is_active=True)

    for cart_item in cart_items:
        cart_total_price += (cart_item.product.price * cart_item.quantity)
        if cart_item.product.offer_price():
            offer_price = Product.offer_price(cart_item.product)
            cart_total_price += (offer_price["new_price"] * cart_item.quantity)
            cart_total_price = round(cart_total_price, 2)

    sub_total = cart_item.sub_total()
    you_saved = cart_total_price - sub_total
    saved = round(you_saved, 2)

    return JsonResponse({
        'quantity': qty,
        'total': cart_total_price,
        'sub_total': sub_total,
        'total_price': cart_total_price,
        'saved': saved,
        'status': True
    })


def increase_quantity(request):
    product_id = request.GET.get('id')
    id_cart = request.GET.get('c_id')
    total_price = 0
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(id=id_cart, product=product, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(id=id_cart, product=product, cart=cart)

    if cart_item.quantity:
        total_price += (cart_item.product.price * cart_item.quantity)
        variation = cart_item.variations.first()

        # Check if the new quantity exceeds the stock count
        if cart_item.quantity >= variation.stock:
            messages.error(request, 'Exceeded the available stock count.')
            return JsonResponse({'message': 'Exceeded the available stock count.', 'status': False}, status=400)

        qty = cart_item.quantity + 1
        cart_item.quantity += 1
        cart_item.save()

        total = 0
        if cart_item.product.offer_price():
            offer_price = Product.offer_price(cart_item.product)
            total += (offer_price["new_price"] * cart_item.quantity)
            total = round(total, 2)
        else:
            total += (cart_item.product.price * cart_item.quantity)

        cart_item.offer_discount = total
        cart_item.save()
        sub_total = cart_item.sub_total()
        you_saved = total_price - total
        saved = round(you_saved, 2)

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        total_p = 0
        total_price_p = 0

        for cart_item in cart_items:
            total_price_p += (cart_item.product.price * cart_item.quantity)

            if cart_item.product.offer_price():
                offer_price = Product.offer_price(cart_item.product)
                total_p += (offer_price["new_price"] * cart_item.quantity)
                total_p = round(total_p, 2)
            else:
                total_p += (cart_item.product.price * cart_item.quantity)

            saved_p = total_price_p - total_p
            saved_p = round(saved_p, 2)

    return JsonResponse({
        'quantity': qty,
        'total': total_p,
        'sub_total': sub_total,
        'total_price': total_price_p,
        'saved': saved_p,
        'status': True,
    })


def apply_coupon(request):
    total = 0
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)

    for cart_item in cart_items:
        if cart_item.product.offer_price():
            offer_price = Product.offer_price(cart_item.product)
            total += offer_price["new_price"] * cart_item.quantity
            total = round(total, 2)
        else:
            total += cart_item.product.price * cart_item.quantity

    if request.method == 'GET':
        code = request.GET.get('code')
        c_exists = False
        status = False
        coupon = None

        if code:
            try:
                coupon = Coupon.objects.get(code=code)
                c_exists = True
                today = date.today()
                if coupon.valid_from <= today and coupon.valid_to >= today:
                    total -= coupon.discount
                    status = True

                    # Update the coupon_discount and discount fields in cart_item
                    cart_item.coupon_discount = total
                    cart_item.discount = coupon.discount
                    cart_item.save()
                else:
                    status = False
            except Coupon.DoesNotExist:
                print('Coupon not found')
                return redirect('checkout')

    return JsonResponse({
        'total': total,
        'discount': coupon.discount if coupon and status else 0,
        'status': status,
        'c_exists': c_exists
    })


@login_required(login_url='login-page')
def checkout(request):
    total = 0
    quantity = 0
    total_discount = 0  # Variable to accumulate the total discount

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)

        for cart_item in cart_items:
            if cart_item.product.offer_price():
                offer_price = Product.offer_price(cart_item.product)
                total += offer_price["new_price"] * cart_item.quantity
            else:
                total += cart_item.product.price * cart_item.quantity

            quantity += cart_item.quantity

            # Accumulate the discount for each cart_item
            if cart_item.discount is not None:
                total_discount += cart_item.discount

            # Check if the cart item has a valid coupon associated with it
            if cart_item.coupon:
                coupon_amount = cart_item.coupon.discount * cart_item.quantity
                cart_item.coupon_discount = coupon_amount
                total_discount += coupon_amount

            cart_item.save()

        # If the total cart amount is less than or equal to 1500 Rs, remove the coupon discount
        if total <= 1500:
            for cart_item in cart_items:
                cart_item.coupon_discount = 0
                cart_item.discount = 0
                cart_item.save()

    else:
        cart_items = []

    today = date.today()
    coupons = Coupon.objects.all()
    address = Address.objects.filter(user=request.user)

    saved = request.session.get('offer_applied', 0)

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'address': address,
        'coupons': coupons,
        'total_p': total - total_discount,  # Use the updated total with the accumulated discount
        'discount': total_discount,  # Provide the total accumulated discount to the context
        'saved': saved,
    }

    return render(request, 'customerapp/checkout.html', context)
