
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomBaseuser(BaseUserManager):
   def create_user(self,phone_number,email,password=None,**extra_fields):
      print(phone_number)
      print(password)
      print(email)
      if not phone_number:
        raise ValueError(_('phone number is must required'))
      if not email:
         raise ValueError(_('email is required'))
      
      email=self.normalize_email(email)
      user=self.model(phone_number=phone_number,email=email,**extra_fields) 
      user.set_password(password) 

      user.save()
      return user
   def create_superuser(self,phone_number,email,password=None,**extra_fields):
      

      extra_fields.setdefault("is_staff",True)
      extra_fields.setdefault("is_superuser",True)
      extra_fields.setdefault("is_active",True) 
      email=self.normalize_email(email)
      if extra_fields.get('is_staff') is not True:
         raise ValueError(_('must set is_staff=True'))
      if extra_fields.get('is_superuser') is not True:
         raise ValueError(_('must set is_superuser=True'))
      if phone_number is None:
         raise ValueError('phone number is ')
      
      return self.create_user(phone_number,email,password,**extra_fields)