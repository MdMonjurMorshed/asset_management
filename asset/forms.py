from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class CustomUserForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=CustomUser
        fields=['phone_number','company_name','logo','email','password1','password2']

        widgets={
            'phone_number':forms.TextInput(attrs={'class':'form-control','name':'phone'}),
            'email':forms.EmailInput(attrs={'class':'form-control','name':'email'}),
             'company_name':forms.TextInput(attrs={'class':'form-control','name':'company'}),
             'logo':forms.ClearableFileInput(attrs={'class':'form-control','name':'logo'}),

            'password1':forms.PasswordInput(attrs={'class':'form-control','name':'password1'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control','name':'password2'})

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        self.fields['email'].widget.attrs['class']='form-control'  
        self.fields['password1'].widget.attrs['class']='form-control'  
        self.fields['password2'].widget.attrs['class']='form-control'  
        self.fields['password1'].help_text=''

class AssetCreationForm(forms.ModelForm) :

    class Meta:
        model=Assets
        fields=['title','description','total_count']

        widgets={
            'title':forms.TextInput(attrs={'class':'form-control','name':'title'}),
            'description':forms.TextInput(attrs={'class':'form-control','name':'description'}),
            'total_count':forms.NumberInput(attrs={'class':'form-control','name':'count'})

        }

class AssetUpdateForm(forms.ModelForm):
    class Meta:
        model=UpdateAssets
        fields=['assets','count']

        widgets={
            'assets':forms.Select(attrs={'class':'form-control','name':'assets'}),
            'count':forms.NumberInput(attrs={'class':'form-control','name':'count'})
        }


class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields=['name','position']

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','name':'name'}),
            'position':forms.TextInput(attrs={'class':'form-control','name':'position'})
        }

class AssetAsignForm(forms.ModelForm):
    class Meta:
        model=AssetAsign 
        fields=['employee','asset']       

        widgets={
            'employee':forms.Select(attrs={'class':'form-control','name':'employee'}),
            'asset':forms.SelectMultiple(attrs={'class':'form-control','name':'asset'})

        }

class AssetReturnForm(forms.ModelForm):
    class Meta:
        model=AssetReturn
        fields=['employee','asset','quite_job','bad_condition','return_date']

        widgets={
            'employee':forms.Select(attrs={'class':'form-control','name':'employee'}),
            'asset':forms.SelectMultiple(attrs={'class':'form-control','name':'asset'}),
            'quite_job':forms.CheckboxInput(attrs={'value':'','name':'quite_job','id':"flexCheckDefault",'value':'job'}),
            'bad_condition':forms.CheckboxInput(attrs={'value':'','name':'bad_condition','value':'bad'}),
            'return_date':forms.DateInput(attrs={'class':'form-control','name':'date','type':'date'})
        } 



    