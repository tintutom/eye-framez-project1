from django.db import models
from category.models import Category,Subcategory,Product
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class CategoryOffer(models.Model):
    category_name=models.OneToOneField(Category,on_delete=models.CASCADE)
    discount=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(70)])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_valid=models.BooleanField(default=True)

class SubcategoryOffer(models.Model):
    subcategory_name=models.OneToOneField(Subcategory,on_delete=models.CASCADE)
    discount=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(70)])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_valid=models.BooleanField(default=True)

class ProductOffer(models.Model):
    product_name=models.OneToOneField(Product,on_delete=models.CASCADE)
    discount=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(70)])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_valid=models.BooleanField(default=True)

class Coupon(models.Model):
    coupon_name = models.CharField(max_length=25)
    code = models.CharField(max_length=25, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(70)]
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


