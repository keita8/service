from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import LoginView, LogoutView
from ecommerce.apps.account.forms import GuestForm
from ecommerce.apps.account.models import GuestEmail
from ecommerce.apps.addresses.forms import AdressForm
from ecommerce.apps.billing.models import BillingProfile





def checkout_address_create_view(request):

    # next_ = request.GET.get("next")
    # next_post = request.POST.get("next")
    # redirect_path = next_ or next_post or None

    form = AdressForm(request.POST or None)
    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'livraison')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            
            request.session[address_type+"_address_id"] = instance.id
            print([address_type + "_address_id"])
            
            
            facturation_address_id = request.session.get("facturation_address_id", None)
            livraison_address_id = request.session.get("livraison_address_id", None)

        else:
            print("error")
            return redirect('cart:checkout')
        
        # if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
        #     return redirect(redirect_path)
        # else:
        #     return redirect("cart:checkout")
        # else:
        #     print("Erreur")
    # template_name = 'account/login.html'
    context = {
        "form": form
    }
    return  redirect("cart:checkout")
    # return render(request, template_name, context)
    
    
