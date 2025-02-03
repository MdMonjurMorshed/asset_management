
from typing import Any
from django.views.generic import ListView
from asset.models import *
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, response
from django.core.paginator import  Paginator


class AssetTabeView(ListView):
    model=Assets
    context_object_name='asset_obj'
    template_name='asset/asset_table_view.html'
    paginate_by=1
    
    pagination_choice=[10,25,50,100,200,'All']

    def get_queryset(self):
        queryset= super().get_queryset()
        user=self.request.user

        queryset=Assets.objects.filter(user=user)
        self.paginate_by=int(self.get_paginate_by(None))
        

        return queryset
    
    def get_context_data(self, **kwargs: Any):
         context=super().get_context_data(**kwargs)
      
         context['my_paginator']=Paginator(context['asset_obj'],self.paginate_by)

         return context
   
