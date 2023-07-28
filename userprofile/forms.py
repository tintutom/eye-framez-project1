from django import forms
from django import forms
from .models import Address
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser



class UserAddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=["fname","lname",'address',"country",'pincode','state','email']

        def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["fname"].widget.attrs.update(
                {"class":"form-control","placeholder":"Full Name"}
            )

            self.fields["lname"].widget.attrs.update(
                {"class":"form-control","placeholder":"Last Name"}
            )

            self.fields["address"].widget.attrs.update(
                {"class":"form-control","placeholder":"Address"}
            )

            self.fields["pincode"].widget.attrs.update(
                {"class":"form-control","placeholder":"Pincode"}
            )

            self.fields["country"].widget.attrs.update(
                {"class":"form-control"}
            )
            self.fields["state"].widget.attrs.update(
                {"class":"form-control"}
            )
            self.fields["email"].widget.attrs.update(
                {"class":"form-control","placeholder":"Email"}
            )

class EditUserForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email','phone']
    
        