from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Variations)
admin.site.register(Category)
admin.site.register(Subcategory)