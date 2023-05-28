from django.shortcuts import render
from ecommerce.apps.products.models import *
from django.db import models
from django.http import Http404
from django.shortcuts import render
from django.views.generic import (ListView, DetailView, DeleteView, CreateView, UpdateView)
# from core.apps.cart.models import Cart



class ShopListView(ListView):
    model = Product
    template_name = 'layout/shop.html'
    paginate_by = 15
    context_object_name = 'products'
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()
    
    
    def get_context_data(self, *args, **kwargs):
        request = self.request
        context = super(ShopListView, self).get_context_data(*args,**kwargs)
        context['categories'] = Category.objects.all().filter(active=True)

        return context
    
    

  