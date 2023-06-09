from django.db import models
from tinymce.models import HTMLField
import uuid
import random
import os
from django.db.models import F
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q



def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_about_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f"about/{new_filename}/{final_filename}"




class About(models.Model):
    title = HTMLField(default="À PROPOS D'IT SERVICES")
    overview = HTMLField(help_text='brève description du service',  default="IT SERVICE SARL est un intégrateur système spécialisé dans le domaine réseaux et sécurité informatique. Immatricule au registre du commerce et du crédit immobilier sous la référence GC.KAL.2017.B.080 022")
    # title = models.CharField(max_length = 150, verbose_name='Titre')
    intervention = models.ManyToManyField("Intervention", blank=True)
    content = HTMLField(blank=True)
    reference = models.ManyToManyField("Reference", blank=True)

    class Meta:
        verbose_name ="A propos"
        verbose_name_plural = "A propos"
        
        

    def __str__(self):
        return self.title





class Intervention(models.Model):
    name = models.CharField(max_length = 150, verbose_name='intervention', unique=True)
    
    class Meta:
        verbose_name ="Domaine d'Intervention"
        verbose_name_plural ="Domaines d'Interventions"

    def __str__(self):
        return self.name







class Reference(models.Model):
    name = models.CharField(max_length = 150, verbose_name='partenaire', unique=True, default='ref')
    image = models.ImageField(upload_to=upload_about_path, height_field=None, width_field=None, max_length=100)
    url  = models.URLField(max_length = 200)
    

    class Meta:
        verbose_name ="Nos partenaire"
        verbose_name_plural ="Nos partenaires"

    def __str__(self):
        return f'{self.name}'

    # def get_absolute_url(self):
    #     return reverse("Reference_detail", kwargs={"pk": self.pk})






class FAQ(models.Model):
    title = models.CharField(max_length = 150, verbose_name='titre', default='')
    introduction = HTMLField(default='')
    question = models.CharField(max_length = 150)
    answer   = HTMLField(help_text='reponse à la question frequement posée')
    
    class Meta:
        verbose_name = 'Foire aux questions'
        verbose_name_plural = 'Foires aux questions'
    
    def __str__(self):
        return self.question
    
    