from datetime import timezone
from typing import Iterable, Optional
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,PermissionsMixin
from .manager import CustomBaseuser
from .abstract_class import CommonField


class CustomUser(AbstractBaseUser,PermissionsMixin):
    
  
 
 
    phone_number=models.CharField(max_length=11,unique=True)
    company_name=models.CharField(max_length=100)
    logo=models.ImageField(upload_to="company_logo",null=True)
    email=models.EmailField(null=True,unique=True)
    company_location=models.CharField(max_length=100)
    company_ceo_name=models.CharField(max_length=100,blank=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    USERNAME_FIELD='phone_number'
    REQUIRED_FIELDS=['email']

    
    objects=CustomBaseuser()

    
   

class Assets(CommonField):
   

    title=models.CharField(max_length=100,blank=False)
    description=models.TextField(max_length=150,blank=False)
    total_count=models.IntegerField(default=0)
    available_count=models.IntegerField(default=0)

    def __str__(self):
        return self.title
class UpdateAssets (CommonField):
    
    assets=models.ForeignKey(Assets,on_delete=models.CASCADE)
    count=models.IntegerField(default=0)

    def __str__(self):
        return self.assets.title



class Employee(CommonField):
  
    name=models.CharField(max_length=100,blank=False)
    position=models.CharField(max_length=100 ,blank=False)
    assets=models.ManyToManyField(Assets,blank=True)
    is_active=models.BooleanField(default=True)
    def __str__(self):
        return self.name

class AssetAsign(CommonField):
   
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    asset=models.ManyToManyField(Assets,blank=True)

    def __str__(self):
        return self.employee.name
    
           


class AssetReturn(CommonField):
        
     
        employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
        asset=models.ManyToManyField(Assets)
        quite_job=models.BooleanField(default=False)
        bad_condition=models.BooleanField(default=False)
        return_date=models.DateField(null=True)

        def __str__(self):
            return self.employee.name

     

class BadAsset(CommonField):
   
     asset=models.ForeignKey(Assets,on_delete=models.CASCADE)
     count=models.PositiveIntegerField(default=0)



     def __str__(self):
         return self.asset.title




