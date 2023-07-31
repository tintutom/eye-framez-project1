from django.utils import timezone
from django.conf import settings
from random import choices
from django.db import models
from django.urls import reverse
from django.apps import apps
from django.db.models.aggregates import Sum
# Create your models here.

class Category(models.Model):
    cat_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=200,unique=True)

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])

    def __str__(self):
        return self.cat_name
class Subcategory(models.Model):
    sub_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    parent_cat = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('sub_name', 'parent_cat')

    def get_url(self):
        return reverse('products_by_subcategory',args=[self.parent_cat.slug,self.slug])
    def __str__(self):
        return self.sub_name


class Product(models.Model):
    product_name=models.CharField(max_length=500,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    product_desc=models.TextField()
    price=models.FloatField()
    img1=models.ImageField(upload_to='images/product_images',blank=True)
    img2=models.ImageField(upload_to='images/product_images',blank=True)
    img3=models.ImageField(upload_to='images/product_images',blank=True)
    img4=models.ImageField(upload_to='images/product_images',blank=True)
    added_date=models.DateTimeField(auto_now_add=True)
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory=models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    users_wishlist=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='users_wishlist',blank=True)
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.subcategory.slug,self.slug])
        
    def __str__(self):
        return self.product_name


    def offer_price(self):
        try:
            if self.category.categoryoffer.is_valid:
                offer_price=(self.price*(self.category.categoryoffer.discount) / 100)
                new_price=self.price - offer_price
                return {
                    "new_price":new_price
                }
            raise
        except:
            try:
                if self.subcategory.subcategoryoffer.is_valid:
                    offer_price=(self.price*(self.subcategory.subcategoryoffer.discount) / 100)
                    new_price=self.price - offer_price
                    return {
                        "new_price":new_price
                    }
                raise
            except:
                try:
                    if  self.productoffer.is_valid:
                        offer_price=(self.price*(self.productoffer.discount) / 100)
                        new_price=self.price - offer_price
                        return {
                            "new_price":new_price
                        }
                    raise
                except:
                    return {
                            "new_price":self.price
                        }
        

class Color(models.Model):
    color_value=models.CharField(max_length=50,null=True)

class Variations(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE, related_name='variations')
    color=models.ForeignKey(Color,on_delete=models.CASCADE,null=True)
    stock = models.PositiveIntegerField(default=0)  
    img1 = models.ImageField(upload_to='images/product_images', blank=True)
    img2 = models.ImageField(upload_to='images/product_images', blank=True)
    img3 = models.ImageField(upload_to='images/product_images', blank=True)
    img4 = models.ImageField(upload_to='images/product_images', blank=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.color.color_value}" if self.color else f"{self.product.product_name}"

    
    