from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self,first_name,last_name,email,phone,password=None,**extra_fields):
        
        if not phone:
                raise ValueError("phone is required")
        first_name=first_name,
        last_name=last_name,
        phone=phone
        email=self.normalize_email(email)
        user=self.model(first_name=first_name,last_name=last_name,email=email,phone=phone,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,first_name,last_name,email,phone,password):

        user=self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password
        )

        user.is_admin=True
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user
        
