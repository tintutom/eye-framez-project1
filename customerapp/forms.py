from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser

class RegistrationForm(UserCreationForm):
    
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email','phone','password1','password2']
   
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder':'Last Name'})
        self.fields['email'].widget.attrs.update({'placeholder':'Email'})
        self.fields['phone'].widget.attrs.update({'placeholder':'Phone Number'})
        self.fields['password1'].widget.attrs.update({'placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder':'Confirm Password'})