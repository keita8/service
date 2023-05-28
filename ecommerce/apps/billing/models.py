from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import *
from ecommerce.apps.account.models import GuestEmail

User = get_user_model()
# User = settings.AUTH_USER_MODEL

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
            
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(email=guest_email_obj.email)
    
        else:
            pass
        
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='client')
    email = models.EmailField(max_length=254)
    active = models.BooleanField(default=True)
    update = models.DateTimeField("dernière modification", auto_now=True)
    timestamp = models.DateTimeField("date de creation", auto_now_add=True)
    
    objects = BillingProfileManager()
    
    class Meta:
        verbose_name = "Facturation"
        verbose_name_plural = "Facturations"
    
    def __str__(self):
        return self.email
    
    
    


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)




post_save.connect(user_created_receiver, sender=User)