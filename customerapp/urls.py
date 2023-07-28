from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.user_register,name='register'),
    path('signup-otp/',views.signup_otp,name='signup-otp'),
    path('verify_signup_otp/',views.verify_signup_otp,name='verify_signup_otp'),
    path('login-page/',views.login_page,name='login-page'),
    path('login-otp/',views.login_otp,name='login-otp'),
    path('otp/',views.otp,name='otp'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('login-pass/',views.login_pass,name='login-pass'),
    path('logout/',views.user_logout,name='logout_user'),
    # Store
    path('store/',views.store,name='store'),
    path('store/<slug:category_slug>/',views.store,name='products_by_category'),
    path('store/<slug:category_slug>/<slug:subcategory_slug>/',views.store,name='products_by_subcategory'),
    path('store/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    # Wishlist
    path('add_to_wishlist/<int:id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('user_wishlist/',views.user_wishlist,name="user_wishlist"),
    # User Profile
    path('my_profile/',views.my_profile,name="my_profile"),
    path('change_password',views.change_password,name='change_password'),
    # filter
    path('filter_price',views.filter_price,name='filter_price'),


]
