import datetime
from datetime import datetime
from django.db import models
from datetime import timedelta
import math
from django.db.models import Count, Sum, Avg
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
from django.utils import timezone



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
    
    def get_sales_breakdown(self):
        recent = self.recent().not_refunded()
        recent_data = recent.totals_data()
        recent_cart_data = recent.cart_data()
        shipped = recent.not_refunded().by_status(status="shipped")
        shipped_data = shipped.totals_data()
        paid = recent.by_status(status="paid")
        paid_data = paid.totals_data()
        data = {
            'recent': recent,
            'recent_data': recent_data,
            'recent_cart_data': recent_cart_data,
            'shipped': shipped,
            'shipped_data': shipped_data,
            'paid':paid,
            'paid_data':paid_data
        }
        
        return data
        
  

    
    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(updated__gte=start_date)
        return self.filter(updated__gte=start_date).filter(updated__lte=end_date)
    
    
    def by_date(self):
        now = timezone.now() - datetime.timedelta(days=9)
        return self.filter(updated__day__gte=now.day)
    
    
    def by_week_range(self, weekend_ago=1, number_of_weeks=1):
        if number_of_weeks > weekend_ago:
            number_of_weeks = weekend_ago
        days_ago_start = weekend_ago * 7
        days_ago_end = days_ago_start  - (number_of_weeks * 7)
        start_date = timezone.now() - timedelta(days=days_ago_start)
        end_date = timezone.now() - timedelta(days=days_ago_end)
        print(days_ago_start, days_ago_end)
        return self.by_range(start_date=start_date, end_date=end_date)
    

    def by_status(self, status="shipped"):
        return self.filter(status=status)
    
    
    def totals_data(self):
        return self.aggregate(Sum('total'), Avg('total') )
        
    
    def cart_data(self):
        return self.aggregate(Sum('cart__products__price'),Avg('cart__products__price'), Count("cart__products"))

    
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
    
    
    def not_created(self):
        return self.get_queryset().not_created()
    
        
    def by_date(self):
        return self.get_queryset().by_date()
    
    
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
    total                   = models.DecimalField(max_digits=100, decimal_places=2, default=0.00, verbose_name="total")
    timestamp               = models.DateTimeField(verbose_name="date de creation", default=now)
    updated                 = models.DateTimeField("dernière modification", auto_now=True)
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
        new_total = math.fsum([cart_total,0])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total
    
    

    def __str__(self):
        return f'{self.billing}'
    
    
    
    def get_absolute_url(self):
        return reverse("account:order-detail", kwargs={"pk": self.pk})
    
    
    
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
    
    def products_by_id(self, request):
        qs = self.by_request(request=request).digital()
        ids_ = [x.product.id for x in qs]
        return ids_

    def by_request(self, request):
        return self.get_queryset().by_request(request)
    
    
    
    def products_by_request(self, request):
        ids_ = self.products_by_id(request=request)
        products_qs = Product.objects.filter(id__in=ids_).distinct()
        return products_qs
    






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
