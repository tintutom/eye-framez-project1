from django.db import models
from accounts.models import CustomUser
from category.models import Product,Variations
from offers.models import Coupon

# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    variations=models.ManyToManyField(Variations,blank=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    coupon_discount=models.IntegerField(null=True)
    discount=models.IntegerField(null=True)   
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True) 

    def sub_total(self):
        return self.product.price*self.quantity