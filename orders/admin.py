from django.contrib import admin
from .models import Order
# Register your models here.
from.models import *
 
admin.site.register(OrderItem)
admin.site.register(Order)