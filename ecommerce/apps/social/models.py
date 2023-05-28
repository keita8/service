from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Social(models.Model):
    facebook  = models.URLField("Facebook", max_length=300, blank=True, null=True)
    instagram = models.URLField("Instagram", max_length=300, blank=True, null=True)
    twitter   = models.URLField("Twitter", max_length=300, blank=True, null=True)
    whatsapp  = models.URLField("WhatsApp", max_length=300, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, verbose_name="Téléphone")
    email     = models.EmailField(max_length=254, default='example@gmail.com')
    address   = models.TextField(verbose_name="adresse", default="Conakry")
    
    class Meta:
        verbose_name = 'Reseau social'
        verbose_name_plural = 'Reseaux sociaux'
    
    def __str__(self):
        return f'{self.facebook}'
    