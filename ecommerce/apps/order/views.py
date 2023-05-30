from typing import Any, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DateDetailView, DetailView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from ecommerce.apps.billing.models import *


# LISTE DE TOUTES LES COMMANDES
class OrderListView(LoginRequiredMixin, ListView):
    model = Orders
    template_name = "registration/account.html"
    context_object_name = 'orders'

    
    def get_queryset(self):
        return Orders.objects.by_request(self.request).not_created()
    

# DETAIL D'UNE COMMANDE
class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'order/order_detail.html'
    context_object_name = 'order_detail'
    def get_object(self):
        qs = Orders.objects.by_request(self.request).filter(order_id=self.kwargs.get('order_id'))
        if qs.count() == 1:
            return qs.first()
        return Http404
    
    
# LISTE DES ARTICLES DIGITAUX (EXEMPLE DES EBOOKS ACHETÉS SUR LE SITE)
class LibraryView(LoginRequiredMixin, ListView):
    template_name = 'order/library.html'
    context_object_name = 'digital_item'
    def get_queryset(self) -> QuerySet[Any]:
        return ProductPurchase.objects.by_request(self.request).digital()