from django.db import models
from accounts.models import CustomUser
from category.models import Product,Variations
from userprofile.models import Address
from offers.models import Coupon
from django.urls import reverse
from django.apps import apps
from django.db.models.aggregates import Sum
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,null=True,on_delete=models.SET_NULL)
    total_price=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=150,null=False)
    payment_id=models.CharField(max_length=250,null=True)
    status=models.CharField(max_length=150,default='Placed')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at_at=models.DateTimeField(auto_now=True)
    
    @property
    def total_paid_amount(self):
        # Calculate the total paid amount based on total_price and applied coupon discounts
        return self.total_price - self.coupon_discount

class OrderItem(models.Model):
    order=models.ForeignKey(Order,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    variation = models.ForeignKey(Variations, null=True, on_delete=models.SET_NULL)
    price=models.FloatField(null=False)
    quantity=models.IntegerField(null=False)
    status=models.CharField(max_length=150,default='Order Placed')
    created_at=models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL) 
    
    def __str__(self):
        return f'{self.quantity} x {self.product.product_name}'
    
    
    
