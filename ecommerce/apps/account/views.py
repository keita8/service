from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse_lazy

from ecommerce.apps.order.models import ProductPurchase
from .signals import *
from ecommerce.apps.order.models import Orders
from .forms import *
from .models import *
from django.views.generic import *
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.mail.message import EmailMessage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin





User = get_user_model()




    
class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'registration/account.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["orders"] = Orders.objects.by_request(self.request).not_created()
        context['is_digit'] = ProductPurchase.objects.products_by_request(self.request).order_by('-id')
        return context
    
        
    # def get_queryset(self):
    #     return Orders.objects.by_request(self.request).not_created()
    
    
    def get_object(self):
        return self.request.user









def register_page(request):
    if request.user.is_authenticated:
        return redirect('products:main')

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email    = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        confirm_password = form.cleaned_data.get("confirm_password")
        user  = authenticate(request, email=email, password=password, confirm_password=confirm_password)
        if user is not None:
            login(request, user)
            return redirect("products:main")
        else:
            print("Erreur")
    template_name = 'registration/register.html'
    context = {
        "form": form
    }
    return render(request, template_name, context)
    






  
def guest_login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None

    form = GuestForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        email = form.cleaned_data.get("email")
        new_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_email.id
        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("account:register")
        # else:
        #     print("Erreur")
    # template_name = 'account/login.html'
    context = {
        "form": form
    }
    return  redirect("account:register")
    # return render(request, template_name, context)
    










def login_page(request):
    if request.user.is_authenticated:
        return redirect('products:main')
    
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None

    form = UserLogin(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user  = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, "Votre compte n'a pas encore  été activé !")
                redirect("account:login")
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("account:dashboard")
        else:
            messages.error(request, "Vos identifiants sont incorrectes !")
            return redirect("account:login")
    template_name = 'registration/login.html'
    context = {
        "form": form
    }
    return render(request, template_name, context)
  
  
  
  
  
  
  
    
    

@login_required(login_url="account:login")
def logout_user(request):
    logout(request)
    return redirect("products:main")













class LoginUserView(FormView):
    form_class = UserLogin
    success_url = reverse_lazy('account:dashboard')
    template_name = 'registration/login.html'
    
    def form_valid(self, form) -> HttpResponse:
        request = self.request 
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user=user)
            # user_logged_in.send(user.__class__, instance=user, request=request)
            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("account:dashboard")
        
        
        return super(LoginUserView, self).form_valid(form)












class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'registration/user_form.html'
    
    def get_object(self):
        return self.request.user
    
    
    
    
    
