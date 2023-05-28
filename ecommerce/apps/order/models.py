from django.db import models
import math
from django.db.models.query import QuerySet
from django.urls import reverse
from ecommerce.apps.cart.models import Cart
from django.db.models.signals import *
from ecommerce.apps.products.models import Product
from ecommerce.apps.addresses.models import Adresse
from .utils import *
from django.utils.timezone import now
from django.conf import settings
from decimal import Decimal
from ecommerce.apps.billing.models import *
from ecommerce.apps.products.models import Product



User = settings.AUTH_USER_MODEL




ORDER_STATUS = (
    ("created", "commande créée"),
    ("paid", "paiement effectué"),
    ("shipped", "commande livrée"),
    ("refunded", "commande remboursée")
)



class OrderManagerQuerySet(models.query.QuerySet):
    
    def recent(self):
        return self.order_by('-timestamp')
    
    
    def by_status(self, status="shipped"):
        return self.filter(status=status)
    

    
    def not_refunded(self):
        return self.exclude(status='refunded')
    
    
    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request=request)
        return self.filter(billing=billing_profile)
    
    def not_created(self):
        return self.exclude(status='created')
    
    def new_or_get(self, billing, cart):
        created = False
        qs = self.get_queryset().filter(
            billing=billing,
            cart=cart
        )
        
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing=billing
            )
            created = True
        return obj, created
    
    
    
    
   
    

class OrderManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return OrderManagerQuerySet(self.model, using=self._db)
    
    
    
    def recent(self):
        return self.get_queryset().recent()
    
    
    
    def by_request(self, request):
        return self.get_queryset().by_request(request)
    
    
    
    
    def new_or_get(self, billing, cart):
        created = False
        qs = self.get_queryset().filter(billing=billing, cart=cart, status="created")
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing=billing, cart=cart)
            created = True
        
        return obj, created
            





class Orders(models.Model):
    billing                 = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name='client')
    order_id                = models.CharField(max_length = 150, verbose_name='N° commande', blank=True)
    shipping_address        = models.ForeignKey(Adresse, on_delete=models.CASCADE, verbose_name='adresse livraison', related_name='shipping_address', null=True, blank=True)
    billing_address         = models.ForeignKey(Adresse, on_delete=models.CASCADE, verbose_name='adresse de facturation', related_name='billing_address', null=True, blank=True)
    shipping_address        = models.ForeignKey(Adresse, on_delete=models.CASCADE, blank=True, null=True, verbose_name="adresse de livraison")
    cart                    = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='panier')
    status                  = models.CharField(max_length = 150, choices=ORDER_STATUS, default="created")
    shipping_total          = models.DecimalField(max_digits=100, decimal_places=2, default=9.99, verbose_name="frais de livraison")
    total                   = models.DecimalField(max_digits=100, decimal_places=2, default=0.00, verbose_name="total")
    timestamp               = models.DateTimeField(verbose_name="date de creation", default=now)
    active                  = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"
        ordering = ("-id", )
        
    objects = OrderManager()
    
    @property 
    def get_status(self):
        if self.status == "refunded":
            return "Commande retournée"
        elif self.status == "shipped":
            return "Commande livrée"
        return "Livraison en cours"
        
    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total
    
    

    def __str__(self):
        return f'{self.billing}'
    
    
    @property
    def check_done(self):
        
        shipping_done = False
        
        facturation_address_required = not self.cart.is_digital
        
        if facturation_address_required and self.shipping_address:
            shipping_done = True
        elif facturation_address_required and not self.shipping_address:
            shipping_done = False
        else:
            shipping_done = True
            
            
        # if not facturation_address_required and not self.shipping_address:
        #     shipping_done = True
        # if facturation_address_required and not self.shipping_address:
        #     shipping_done = False
            
        billing_profile = self.billing
        shipping_address = self.shipping_address
        # billing_address = self.billing_address
        total = self.total 
        return True if billing_profile and shipping_done and total > 0 else False

        # return True if billing_profile and shipping_address and total > 0 else False

    def update_purchases(self):
        for p in self.cart.products.all():
            obj, created = ProductPurchase.objects.get_or_create(
                order=self.order_id,
                product=p,
                billing_profile=self.billing
            )
        return ProductPurchase.objects.filter(order=self.order_id).count()
    
    @property
    def mark_paid(self):
        if self.check_done:
            self.status = "paid"
            # self.active = False
            self.save()
            self.update_purchases()
                
                # obj.refunded = False
                # obj.save()

        return self.status



def pre_save_create_order_id(sender, instance, *args, **kwargs):
    
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance=instance)
        
    qs = Orders.objects.filter(cart=instance.cart).exclude(billing=instance.billing)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Orders)



def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total 
        cart_id = cart_obj.id 
        qs = Orders.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()
    
    
    
    
    
def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()
        
        

post_save.connect(post_save_cart_total, sender=Cart)
post_save.connect(post_save_order, sender=Orders)


class ProductPurchaseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(refunded=False)
    
    def digital(self):
        return self.filter(product__is_digit=True)
    
    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request=request)
        return self.filter(billing_profile=billing_profile)
        





class ProductPurchaseManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return ProductPurchaseQuerySet(self.model, using=self._db)
    
    
    def all(self):
        return self.get_queryset().active()
    
    def digital(self):
        return self.get_queryset().active().digital()


    def by_request(self, request):
        return self.get_queryset().by_request(request)
    
    
    






class ProductPurchase(models.Model):
    # user           = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name='client')
    order          = models.CharField(max_length=120, verbose_name='N commande')
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE, verbose_name='adresse de livraison')
    product        = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='produit')
    refunded       = models.BooleanField(verbose_name="article retourné ?", default=False)
    timestamp      = models.DateTimeField(verbose_name="Date", auto_now_add=True)
    update         = models.DateTimeField(verbose_name="Modification", auto_now=True)
   
   
    objects        = ProductPurchaseManager()

    class Meta:
        verbose_name ="Produit acheté"
        verbose_name_plural = "Produits achetés"

    def __str__(self):
        return f'{self.product.title}'

    # def get_absolute_url(self):
    #     return reverse("ProductPurchase_detail", kwargs={"pk": self.pk})