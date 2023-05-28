from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from ecommerce.apps.products.models import Product
from django.db.models.signals import *
from django.db.models import F
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q
from decimal import Decimal
# from core.apps.orders.models import *



User = settings.AUTH_USER_MODEL



class CartManager(models.Manager):
    

    def new_or_get(self, request):
        
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user 
                cart_obj.save()
        else:
            cart_obj =Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        
        return cart_obj, new_obj
            
    
    
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)






class Cart(models.Model):
    user       = models.ForeignKey(User, verbose_name="client", on_delete=models.CASCADE, null=True, blank=True, editable=False)
    products   = models.ManyToManyField(Product, verbose_name='articles', blank=True)
    subtotal   = models.DecimalField('total hors taxe', max_digits=100, decimal_places=2, default=0.00, validators=[MaxValueValidator(1000000000000),MinValueValidator(0)])
    total      = models.DecimalField('total ttc', max_digits=100, decimal_places=2, default=0.00, validators=[MaxValueValidator(1000000000000),MinValueValidator(0)])
    updated    = models.DateTimeField(auto_now=True, verbose_name='Modification')
    timestamp  = models.DateTimeField(auto_now_add=True, verbose_name='Creation')
    
    @staticmethod
    def commande(self):
        return f'{self.id}'
    
    @property
    def is_digital(self):
        qs = self.products.all()
        new_qs = qs.filter(is_digit=False)
        if new_qs.exists():
            return False 
        return True
    
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        
        
    objects = CartManager()
        
    
    def __str__(self):
        return f'Panier ({self.id})'
   
   
   



def m2m_changed_pre_save_cart_receiver(sender, instance, action, *args, **kwargs):

    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':

        products = instance.products.all()
        total = 0
        
        for x in products:
            total += x.price
            
        instance.total = total
        
        if instance.subtotal != total:
            instance.subtotal = total
            
            instance.save()
             
        print(instance.total)

 
    
    

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    
    TVA = 1.18
    if instance.subtotal > 0:
        instance.total = Decimal(instance.subtotal) * Decimal(TVA)
    else:
        instance.total = 0.00
    





pre_save.connect(pre_save_cart_receiver, sender=Cart)
m2m_changed.connect(m2m_changed_pre_save_cart_receiver, sender=Cart.products.through)








