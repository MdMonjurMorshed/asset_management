
import json
from typing import Any, Optional, Type
from django import http
from django.contrib.auth import login,logout,update_session_auth_hash
from django.forms.models import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm
from django.views.generic import CreateView
from django.contrib.auth import authenticate
from django.views import View
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group,Permission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



# Create your views here.
class HomeView(TemplateView):
    template_name='asset/base.html'




class user_create(CreateView):
    template_name='asset/register.html'
    form_class=CustomUserForm
    success_url=reverse_lazy('home')
    
    def post(self,request):

        phone=request.POST.get('phone_number')
        password=request.POST.get('password1')
        email=request.POST.get('email')
        company_name=request.POST.get('company_name')
        logo=request.FILES['logo']

        user=CustomUser.objects.create_user(phone_number=phone,email=email)
        user.set_password(password)
        
        user.company_name=company_name
        user.logo=logo
        
        user.save()
        group=Group.objects.get(name='customer')
      
        u=CustomUser.objects.get(phone_number=phone)
        if u is not None:
            u.groups.add(group)
            permission=Permission.objects.filter(group=group)
            u.user_permissions.set(permission)
            u.save()
            login(self.request,u)
            return redirect('home')
        
        

        
            

        return HttpResponse()

   
    
    def get_success_url(self):
        return self.success_url


class LogoutView(View):
    def get(self,request):

        logout(request)
        return redirect('home')

class LoginView(View):
    def get(self,request):
        return render(self.request,'asset/login.html')


    
    def post(self,request):
        phone=request.POST.get('phone')
        
        password=request.POST.get('password')
        user=authenticate(phone_number=phone,password=password)
        login(self.request,user)

        return redirect('home')

class Change_Password(View):
    

    def get(self,request):
        if request.user.is_authenticated:
            frm=SetPasswordForm(user=request.user)
            frm.fields['new_password1'].widget.attrs['class']='form-control'
            frm.fields['new_password2'].widget.attrs['class']='form-control'
            frm.fields['new_password1'].label='New Password'
            frm.fields['new_password1'].help_text=''
        
            return render(request,'asset/change_pass.html',{'form':frm})
        else:
            return redirect('login')


    def post(self,request):
        
            frm=SetPasswordForm(user=request.user, data=request.POST)
            if frm.is_valid():
                frm.save()
                update_session_auth_hash(request,request.user)

            return redirect('home')    


class AssetCreateView(PermissionRequiredMixin,CreateView):
    permission_required='asset.add_assets'
    form_class=AssetCreationForm
    template_name='asset/create_asset.html'


    def post(self,request):
        user=request.user
        title=request.POST.get('title')
        description=request.POST.get('description')
        count=request.POST.get('total_count')
        defaults={'description':description,'total_count':count,'available_count':count}

        asset,created=Assets.objects.get_or_create(user=user,title=title,defaults=defaults)
        if not created:
            asset.total_count_count += int(count) 
           
            
            asset.available_count +=int(count)
            asset.save()
        return redirect('create-asset')

class UpdateAssetView(PermissionRequiredMixin,CreateView):
    permission_required='asset.add_updateassets'
    form_class=AssetUpdateForm
    template_name='asset/update_asset.html'    

    def post(self,request):
        user=request.user
        asset=request.POST.get('assets')
        count=request.POST.get('count')
        updated=UpdateAssets.objects.create(user=user,assets_id=asset,count=int(count))
        asset=Assets.objects.get(user=user,id=asset)
        if asset is not None:
            asset.total_count += int(count)
           
            asset.available_count += int(count)
            asset.save()
        
        return redirect('update-asset')

class EmployeeCreateView(PermissionRequiredMixin,CreateView):
    permission_required='asset.add_employee'
    form_class=EmployeeCreateForm
    template_name='asset/employee_create.html'
    
    def post(self,request):
        user=request.user
        name=request.POST.get('name')
        position=request.POST.get('position')
        emp=Employee.objects.create(user=user,name=name,position=position)
      
        return redirect('create-employee')
    

class AssetAsignView(CreateView):
    form_class=AssetAsignForm
    template_name='asset/asset_asign.html'
    def post(self,request):
        user=request.user
        employe_id=request.POST.get('employee')
        asset_id=request.POST.getlist('asset')
        asigned=AssetAsign.objects.create(user=user,employee_id=employe_id)
        
        employee_asset=Employee.objects.get(user=user,id=employe_id)
        for asset in asset_id:
              assets=Assets.objects.get(user=user,id=int(asset))
              assets.available_count -=1
              assets.save()
              asigned.asset.add(asset)
              employee_asset.assets.add(asset)

             
        return redirect('asset-asign')


class AssetReturnView(CreateView):
    form_class=AssetReturnForm
    template_name='asset/asset_return.html'

   

    def post(self,request):
        user=request.user
       

        employee_id=request.POST.get('employee')
        asset_id=request.POST.getlist('asset')
        quite_job=bool(request.POST.get('quite_job'))
   
        
        bad_condition=bool(request.POST.get('bad_condition'))

        return_date=request.POST.get('date')
              
        returned=AssetReturn.objects.create(user=user,employee_id=employee_id,quite_job=quite_job,bad_condition=bad_condition,return_date=return_date)
        
        emp=Employee.objects.get(user=user,id=employee_id)

        if quite_job ==True:
            for asset in asset_id:
               returned.asset.add(asset)

               emp.assets.remove(asset)
               emp.is_active=False
               emp.save()
               assets=Assets.objects.get(user=user,id=asset)
               assets.available_count +=1
               assets.save()

        if bad_condition == True:
            for asset in asset_id:
               returned.asset.add(asset)

               emp.assets.remove(asset)
               assets=Assets.objects.get(user=user,id=asset)
               assets.total_count -=1
               assets.available_count -=1
               assets.save()
               defaults={'count':1}
               bad,created=BadAsset.objects.get_or_create(user=user,asset_id=asset,defaults=defaults) 

               if not created:
                   bad.count +=1
                   bad.save()
        return redirect('home')
    
class ReturnAssetAjax(View):
    def get(self,request):
        user=request.user
        data=request.GET.dict()

        emp=Employee.objects.filter(user=user,id=int(data['emp']))
        
        data_list=[]
        for e in emp:
           for asset in e.assets.all():
               
               dat={
                   'id':asset.id,
                   'title':asset.title
                  
               }
              
               data_list.append(dat)
        
      
        
        return JsonResponse(data_list,safe=False)  


class GetAll(APIView):

   def get(self,request):
       return Response({"message":"Request sent successfully"},status=status.HTTP_200_OK)   