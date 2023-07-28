from django.db import models
from accounts.models import CustomUser


# Create your models here.
class Address(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    fname=models.CharField(max_length=150,null=False)
    lname=models.CharField(max_length=150,null=False)
    email=models.CharField(max_length=150,null=False)
    address=models.CharField(max_length=150,null=False)
    country=models.CharField(max_length=150,null=False)
    state=models.CharField(max_length=150,null=False)
    pincode=models.CharField(max_length=150,null=False)