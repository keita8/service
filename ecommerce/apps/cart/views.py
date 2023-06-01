from django.http import *
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from ecommerce.apps.order.models import *
from .models import Cart
from ecommerce.apps.products.models import Product
from ecommerce.apps.account.models import *
from ecommerce.apps.account.forms import *
from ecommerce.apps.billing.models import *
from ecommerce.apps.addresses.forms import *
from ecommerce.apps.order.models import Orders
import json
from ecommerce.apps.analytics.signals import *
from ecommerce.apps.addresses.forms import AdressForm




def cart_detail_api_view(request):
    
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    
    print(cart_obj)
    products = [{"name": x.title, "price": x.price} for x in cart_obj.products.all()]
    print(products)
    cart_data = {
        "products": products,
        "total": cart_obj.total
    }
    print(cart_data)
    return JsonResponse(cart_data)






def cart(request):
 
    cart, new_obj = Cart.objects.new_or_get(request=request)
    print(f"panier {cart.products.all()}")
    print(cart.is_digital)

    template_name = 'cart/cart.html'
    context = {
        'cart':cart
    }
    return render(request, template_name, context)
    




def cart_update(request):
    print(request.POST)
    product_id = request.POST.get("product_id")
    instance = request.user
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    

    
    if product_id is not None:
        try:
            obj = Product.objects.get_by_id(id=product_id)
        except Product.DoesNotExist:
            return redirect("cart:main")
        
        cart_obj, new_obj = Cart.objects.new_or_get(request=request)
        if obj in cart_obj.products.all():
            cart_obj.products.remove(obj)
            added = False
        else:
            cart_obj.products.add(obj)
            added = True
        
        request.session['cart_items'] = cart_obj.products.count()
        
 
        if is_ajax:

            json_data = {
                'added': added,
                'removed': not added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data)
            

        
    return redirect("cart:main")





# @login_required(login_url='account:login')
def chechout_homepage(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request=request)
    order_obj = None
    
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:main")


    user = request.user 
    billing_profile = None
    address_qs = None
    shipping_address_qs = None
    billing_address_qs=None
    login_form = UserLogin()
    guest_form = GuestForm()
    address_form = AdressForm()
    billing_address_form = AdressForm()
    facturation_address_id = request.session.get("facturation_address_id", None)
    livraison_address_id = request.session.get("livraison_address_id", None)
    
    facturation_address_required = not cart_obj.is_digital
    

    
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request=request)

    print(f"Profil {billing_profile} ")
    
    print()
    
    if billing_profile is not None:
        address_qs = Adresse.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Orders.objects.new_or_get(billing=billing_profile, cart=cart_obj)
        shipping_address_qs = address_qs.filter(address_type="livraison").last()
        billing_address_qs = address_qs.filter(address_type="facturation")
        
        
        if livraison_address_id:
            order_obj.shipping_address = Adresse.objects.get(id=livraison_address_id)
            print(f"avant suppression {livraison_address_id}")
            del request.session["livraison_address_id"]
            print(f"apres suppression {livraison_address_id}")
        if facturation_address_id:
            order_obj.billing_address = Adresse.objects.get(id=facturation_address_id)
            print(f"avant suppression {facturation_address_id}")
            del request.session["facturation_address_id"]
            print(f"apres suppression {facturation_address_id}")
        if facturation_address_id or livraison_address_id:
            order_obj.save()
            
    
    if request.method == "POST":
        is_done = order_obj.check_done
        
        print(f"Terminé : {is_done}")
        
        if is_done:
            payment_done = order_obj.mark_paid
            if payment_done:
                print("Paiement effectué avec succès !!! ")
        
        request.session['cart_items'] = 0
        del request.session['cart_id']
        
        
        return redirect("cart:success")
    
    

    
    template_name = 'cart/checkout.html'
    context = {
        "object": order_obj,
        'billing_profile': billing_profile,
        'cart': cart_obj,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'billing_address_form': billing_address_form,
        "address_qs": address_qs,
        "last_shipping_address": shipping_address_qs,
        "facturation_address_required":facturation_address_required
    }
    
    
    return render(request, template_name, context)
    





def checkout_done(request):
    template_name = 'cart/checkout-done.html'
    context = {}
    return render(request, template_name, context)
    













