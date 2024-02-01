from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from carts.models import CartItem
from category.models import Category, Product, Subcategory,Variations
from .forms import RegistrationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import random
from twilio.rest import Client
from django.core.paginator import Paginator
from carts.views import _cart_id
from carts.models import Cart,CartItem
from django.views.decorators.cache import never_cache
from category.models import Variations
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.template.defaultfilters import slugify
from django.http import JsonResponse
import os
# Create your views here.


@never_cache
def home(request):
    if request.user.is_superuser:
        return redirect('adminlogin')
    category=Category.objects.all()
    subcategory=Subcategory.objects.all()
    trendy=Product.objects.all()[:4]
    
    return render(request,'customerapp/home.html',{
        'category':category,
        'subcategory':subcategory,
        'trendy':trendy
    })


class OtpGenerate:
    Otp = None
    phone = None
    
    @staticmethod
    def read_env_file(file_path):
        # Function to read the .env file and return a dictionary of key-value pairs
        env_vars = {}
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    key, value = line.strip().split("=")
                    env_vars[key] = value
        except Exception as e:
            print("Error reading .env file:", e)
        return env_vars

    @staticmethod
    def send_otp(phone):
        # Path to the .env file
        env_file_path = '.env'

        try:
            # Read the .env file and extract the values
            env_vars = OtpGenerate.read_env_file(env_file_path)

            # Get the required Twilio credentials from the extracted values
            account_sid = env_vars.get('account_sid')
            auth_token = env_vars.get('auth_token')
            target_number = '+919061488055'
            twilio_number = env_vars.get('twilio_number')
            
            if not (account_sid and auth_token and twilio_number):
                raise ValueError("Missing Twilio credentials in .env file")

            otp = random.randint(1000, 9999)
            OtpGenerate.Otp = str(otp)
            OtpGenerate.phone = phone

            msg = "Your OTP is " + str(otp)

            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=msg,
                from_=twilio_number,
                to=target_number
            )

            print(message.body)
            return True

        except Exception as e:
            # Handle any potential exceptions here (e.g., file not found, invalid format, Twilio error)
            print("Error:", e)
            return False

def user_register(request): 
    form=RegistrationForm()
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            fname=form.cleaned_data["first_name"]
            lname=form.cleaned_data["last_name"]
            email=form.cleaned_data["email"]
            phone=form.cleaned_data["phone"]
            password=form.cleaned_data["password1"]

            request.session["first_name"]=fname
            request.session["last_name"]=lname
            request.session["email"]=email
            request.session["phone"]=phone
            request.session["password"]=password
            OtpGenerate.send_otp(phone)
            return redirect('signup-otp')

    return render(request,'customerapp/register.html',{
        'form':form
    })

def signup_otp(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,'customerapp/signup-otp.html')
def verify_signup_otp(request):
    obj=OtpGenerate()
    if request.method=='POST':
        re_otp=request.POST.get('otp')
        ge_otp=obj.Otp
        if re_otp==ge_otp:
            first_name=request.session["first_name"]
            last_name=request.session["last_name"]
            email=request.session["email"]
            phone=request.session["phone"]
            password=request.session["password"]


            user=CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                password=password
            )
            user.phone=phone
            user.save()
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid Otp")
            return redirect('signup-otp')
    else:
        messages.error(request,"Invalid Credentials")
        return redirect('signup-otp')


def login_page(request):
    if request.user.is_superuser:
        return redirect('adminlogin')
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,'customerapp/login-otp.html')


def read_env_file(file_path):
    with open(file_path) as f:
        lines = f.readlines()
        env_vars = {}
        for line in lines:
            key, value = line.strip().split('=')
            env_vars[key] = value
        return env_vars


def login_otp(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =='GET' and request.GET.get('phone'):
        phone=request.GET.get('phone')
        try:
            if CustomUser.objects.get(phone=phone):
                OtpGenerate.send_otp(phone)
                return redirect('otp')
        except:
            messages.error(request,'Phone Number is not registered')
            return redirect('login-page')

    else:
        messages.error(request,'Please provide your phone number')
        return redirect('login-page')


def otp(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,'customerapp/otp.html')


def verify_otp(request):
    obj=OtpGenerate()
    if request.method=='POST':
        re_otp=request.POST.get('otp')
        ge_otp=obj.Otp
        if re_otp==ge_otp:
            user=CustomUser.objects.get(phone=obj.phone)
            if user.blocked==False:
                try:
                    cart=Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                    
                    if is_cart_item_exists:
                        cart_item=CartItem.objects.filter(cart=cart)
                        product_variation = []
                        for item in cart_item:
                            variation=item.variations.all()
                            product_variation.append(list(variation))
                        cart_item = CartItem.objects.filter(user=user)
                        ex_var_list = []
                        id = []
                        for item in cart_item:
                            existing_variations = item.variations.all()
                            ex_var_list.append(list(existing_variations))
                            id.append(item.id)


                        for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity = item.quantity + 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()
                except:
                    pass

            if user.is_superuser==False:
                login(request,user)
                return redirect('home')
        else:
            messages.error(request,"Invalid Otp")
            return redirect('otp')
    else:
        messages.error(request,"Invalid Credentials")
        return redirect('otp')


@never_cache
def login_pass(request):
    if request.user.is_superuser:
        return redirect('adminlogin')
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(email=email,password=password)
        
        
        if user is not None and user.blocked==False:

            if user.is_superuser==False:
                try:
                    cart=Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                    
                    if is_cart_item_exists:
                        cart_item=CartItem.objects.filter(cart=cart)
                        product_variation = []
                        for item in cart_item:
                            variation=item.variations.all()
                            product_variation.append(list(variation))
                        cart_item = CartItem.objects.filter(user=user)
                        ex_var_list = []
                        id = []
                        for item in cart_item:
                            existing_variations = item.variations.all()
                            ex_var_list.append(list(existing_variations))
                            id.append(item.id)


                        for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity = item.quantity + 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()
                except:
                    pass
                if user.is_superuser==False:
                    login(request,user)
                    return redirect('home')
                else:
                    return redirect('adminlogin')
        else:
            messages.info(request,"Email or Password is Incorrect")
            return redirect(login_pass)
    return render(request,'customerapp/login-pass.html')



def user_logout(request):
    logout(request)
    return redirect('home')


# Store
def store(request,category_slug=None,subcategory_slug=None):
    category=Category.objects.all()
    subcategories=None
    products=None
    categories=None
    search_query = request.GET.get('keyword')
    
    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories)
        paginator=Paginator(products,2)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)

    elif category_slug and subcategory_slug!=None:
        subcategories=get_object_or_404(Subcategory,slug=subcategory_slug)
        products=Product.objects.filter(subcategory=subcategories,category=category_slug)
        paginator=Paginator(products,2)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
    else:

        products=Product.objects.all()
        if search_query:
            products = products.filter(Q(product_name__icontains=search_query) | Q(product_desc__icontains=search_query))


        paginator=Paginator(products,2)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
    return render(request,'customerapp/store.html',{
        'category':category,
        'products':paged_products,
        'search_query': search_query, 
    })

def product_detail(request, category_slug, subcategory_slug, product_slug):
    category = Category.objects.all()
    
    try:
        single_product = Product.objects.get(category__slug=category_slug, subcategory__slug=subcategory_slug, slug=product_slug) 
        variation = Variations.objects.filter(product=single_product.id)
         # Get available color variants for the selected product
        available_colors = single_product.variations.filter(stock__gt=0).values_list('color', flat=True).distinct()
        result = (Variations.objects.filter(product=single_product.id).values('color'))
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

        # Get the image fields for the product
        images = [single_product.img1, single_product.img2, single_product.img3, single_product.img4]
    except Exception as e:
        raise e

    return render(request, 'customerapp/product-detail.html', {
    'single_product': single_product,
    'category': category,
    'in_cart': in_cart,
    'variation': variation,
    'available_colors':available_colors,
    'product_image_count': range(4)  # Update this line with the correct number of images
})

def search(request):
    category=Category.objects.all()
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            
            products=Product.objects.order_by('-added_date').filter(product_name__icontains=keyword)
        else:
            return HttpResponseRedirect(request.META["HTTP_REFERER"])


    context={
        'products':products,
        'category':category
    }
    
    return render(request,'customerapp/store.html',context)


# Wishlist
@login_required(login_url='login-page')

def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    is_added = False  # Flag to track if the product is already in the wishlist
    
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, "Removed " + product.product_name + " from your wishlist")
    else:
        if product.users_wishlist.filter(id=request.user.id).exists():
            is_added = True
            messages.error(request, "The item is already in your wishlist")
        else:
            product.users_wishlist.add(request.user)
            messages.success(request, "Added " + product.product_name + " to your wishlist")
    
    return HttpResponseRedirect(request.META["HTTP_REFERER"], {'is_added': is_added})

@login_required(login_url='login-page')
def user_wishlist(request):
    
    products=Product.objects.filter(users_wishlist=request.user)
    return render(request,'customerapp/wishlist.html',{
        'wishlist':products,
        
    })


# User Profile
@login_required(login_url='login-page')
def my_profile(request):
    categories=Category.objects.all()
    return render(request,'customerapp/my_profile.html',{
        'category':categories
    })

User = get_user_model()
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = get_user_model().objects.get(email=request.user.email)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password Changed Successfully', extra_tags='success')
                return redirect('my_profile')
            else:
                messages.error(request, 'Your Existing Password Is Incorrect')
                return redirect('my_profile')
        else:
            messages.error(request, 'Password Does Not Match!')
            return redirect('my_profile')
    return redirect('my_profile')


def filter_price(request):
    category = Category.objects.all()
    selected = request.GET.get('gridRadios')
    if int(selected) == 1:
        products = Product.objects.filter(Q(price__lte=100))
    elif int(selected) == 2:
        products = Product.objects.filter(Q(price__gte=100, price__lte=500))
    elif int(selected) == 3:
        products = Product.objects.filter(Q(price__gte=500, price__lte=1000))
    elif int(selected) == 4:
        products = Product.objects.filter(Q(price__gte=1000, price__lte=5000))
    elif int(selected) == 5:
        products = Product.objects.filter(Q(price__gte=5000, price__lte=10000))
    else:
        products = Product.objects.filter(Q(price__gte=10000))

    return render(request, 'customerapp/filter_store.html', {
        'products': products,
        'category': category,
        'selected_filter': selected  # Pass the selected filter value to the template
    })

