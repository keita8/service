from django.db import models
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (ListView, DetailView, DeleteView, CreateView, UpdateView, View)
from ecommerce.apps.order.models import ProductPurchase
from ecommerce.apps.marketing.forms import EmailForm
from ecommerce.apps.marketing.models import Newsletter
from ecommerce.apps.marketing.views import subscribe
from ecommerce.apps.cart.models import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from mailchimp_marketing import Client
from django.views.decorators.csrf import csrf_exempt
from ecommerce.apps.analytics.signals import *
from ecommerce.apps.analytics.mixins import ObjectViewMixin
from django.contrib.auth.models import AnonymousUser 
from django.contrib import messages

import os
from wsgiref.util import FileWrapper
from mimetypes import guess_type
from django.conf import settings
  





# PRODUCT LIST VIEW
class ProductListView(ListView):
    model = Product
    template_name = 'layout/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context["features"] = Product.objects.features()
        context['categories'] = Category.objects.all().filter(active=True)[:4]
        context['hero'] = HeroSection.objects.all()
        context['promo'] = Product.objects.all().in_solde().first()
        return context
    
    
 
    def get_queryset(self, *args, **kwargs):
        request = self.request

        images = Product.objects.select_related('products').all()

        return Product.objects.all()
    

        
    
# # CUSTOMER PRODUCT VIEW HISTORY
class UserProductHistoryView(LoginRequiredMixin, ListView):

    template_name = 'registration/history.html'

    
    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args,**kwargs)
        return context
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectview_set.by_model(Product, model_queryset=True)
        return views
    




# PRODUCT DETAIL VIEW
class ProductDetailView(DetailView):
    template_name = 'layout/detail.html'
    context_object_name = 'detail'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, *args, **kwargs):
        request = self.request
        context = super(ProductDetailView, self).get_context_data(*args,**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context["cart"] = cart_obj
        try:
            context['related_products'] = self.get_object().related
        except AttributeError:
            raise Http404("Aucun article trouvé !")
        return context
        
    
    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        request = self.request
        try:
            instance = Product.objects.get_by_slug(slug)
        except Product.DoesNotExist:
            raise Http404("Aucun article trouvé !")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Cet article n'existe pas !!!")

        # if not request:
        #     pass
        # else:
        
        
        # object_viewed_signal.send(instance.__class__, instance=instance, request=request)


        
        return instance
    
    
    

# DOWNLOAD DIGITAL ITEM VIEW
class ProductDownloadView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')

        downloads_qs = DigitalProductFile.objects.filter(pk=pk, products__slug=slug)
        
                
        if downloads_qs.count() != 1:
            raise Http404
        
        downloads_obj = downloads_qs.first()
        
        can_download = False
        user_ready = True
        
        # VERIFIER SI LE CLIENT EST CONNECTÉ À SON COMPTE 
        if downloads_obj.user_required:
            if not request.user.is_authenticated:
                # can_download = True
                user_ready = False
            # else:
            #     # can_download = False
            #     user_can_download=True
        
        purchased_products = Product.objects.none()
        
        # VERIFIER SI LE FICHIER A TELECHARGER EST GRATUIT OU NON
        if downloads_obj.free:
            can_download = True
            user_ready = True
            # ENVOYER LE LIEN DE TELECHARGEMENT AU CLIENT NON CONNECTÉ AU SITE AYANT ACHETE CET ARTICLE
            # 
        else:
            purchased_products= ProductPurchase.objects.products_by_request(request=request)
            if downloads_obj.products in purchased_products:
                can_download = True
                
        if not can_download or not user_ready:
            messages.error(request, "Vous n'avez pas la permission de telecharger ce fichier")
            return redirect(downloads_obj.get_default_url())
            

        
        file_root = settings.PROTECTED_ROOT
        filepath = downloads_obj.file.path
        final_filepath = os.path.join(file_root, filepath)
        
        with open(final_filepath, 'rb') as f:
            
            wrapper = FileWrapper(f)
            mimetype = "application/force-download"
            guessed_mimetype = guess_type(filepath)[0]
            
            if guessed_mimetype:
                mimetype = guessed_mimetype
            response = HttpResponse(wrapper, content_type=mimetype)
            response['Content-Disposition'] = "attachment;filename=%s" %(downloads_obj.name)
            response['X-SendFile'] = str(downloads_obj.name)
            return response
        
        return redirect(downloads_obj.get_default_url())

  
  
  
  
  
  
 

def handle404(request, exception):
    
    template_name = 'include/404.html'
    context = {}
    return render(request, template_name, context)
    
  
  



def shop(request):
    categories = None
    products = Product.objects.all().order_by('-id')
    categories = Category.objects.all().filter(active=True)
        
        
    context = {
        'categories': categories,
        'products': products,
    }
    
    template_name = 'layout/shop.html'
    
    return render(request, template_name, context)

    
  

    

def categorie_products(request, id, categorie_slug):
    categories = Category.objects.all().filter(active=True)
    products = Product.objects.all().filter(category__id=id, category__slug=categorie_slug)
        
    template_name = 'layout/shop.html'
    context = {
        'categories': categories,
        'products': products,
    }
    
    
    return render(request, template_name, context)
    