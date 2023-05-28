from django.shortcuts import render
from django.views.generic import (ListView, DetailView, DeleteView, CreateView, UpdateView)
from ecommerce.apps.products.models import *
from django.db.models import Q


class SearchProductListView(ListView):
    model = Product
    template_name = 'layout/search_result.html'
    
    def get_context_data(self, **kwargs):
        context = super(SearchProductListView, self).get_context_data(**kwargs)
        context["query"] = self.request.GET.get('q')
        context['categories'] = Category.objects.all().filter(active=True)
        # context['products'] = Product.objects.all().filter()
        return context
    
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET)
        
        query = request.GET.get('q', None)
        print(query)
        if query is not None:
            return Product.objects.search(query=query)
        return Product.objects.all()