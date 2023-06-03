from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Social(models.Model):
    facebook  = models.URLField("Facebook", max_length=300, blank=True, null=True)
    instagram = models.URLField("Instagram", max_length=300, blank=True, null=True)
    twitter   = models.URLField("Twitter", max_length=300, blank=True, null=True)
    whatsapp  = models.URLField("WhatsApp", max_length=300, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, verbose_name="Téléphone", default="+224611111183")
    email     = models.EmailField(max_length=254, default='contact@itservices.com')
    address   = models.TextField(verbose_name="adresse", default="Taouya Petit carrefour petit lac commune de Ratoma, Conakry République de Guinée")
    website   = models.URLField(verbose_name="site web", max_length=200, default='www.itservicesgn.com')
    post_box  = models.IntegerField(verbose_name="boite postale", default='403')
    
    class Meta:
        verbose_name = 'Reseau social'
        verbose_name_plural = 'Reseaux sociaux'
    
    def __str__(self):
        return f'{self.email}'
    