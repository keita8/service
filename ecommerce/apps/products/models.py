from django.conf import settings
from django.core.validators import *
from django.utils.safestring import mark_safe
from django.db import models
from django.http import Http404
from django.urls import reverse
from tinymce.models import HTMLField
from django.db.models.signals import *
from djmoney.money import Money
from djmoney.models.fields import MoneyField
from phonenumber_field.phonenumber import PhoneNumber
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from .utils import *
import uuid
import random
import os
from django.db.models import F
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q
from mptt.models import MPTTModel, TreeForeignKey, TreeManager, TreeManyToManyField
from mptt import managers
from django.core.files.storage import FileSystemStorage


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f"products/{new_filename}/{final_filename}"


def upload_image_digital_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f"digital/items/{new_filename}/{final_filename}"


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    
    def in_solde(self):
        return self.filter(item_promo=True)
    
    
    def is_featured(self):
        return self.filter(featured=True)
    
    def search(self, query):
        lookups =( 
                   Q(title__icontains=query) 
                  |Q(description__icontains=query) 
                  |Q(price__icontains=query)
                )
        
        return self.filter(lookups).distinct()


class CategorieQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class CategorieManager(models.Manager):
    
    def get_queryset(self):
        return CategorieQuerySet(self.model, using=self._db)
    

    def all(self):
        return self.get_queryset().active()
    
    
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    
    
    def get_by_slug(self, slug):
        qs = self.get_queryset().active().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None


class ProductManager(models.Manager):
    
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    

    def all(self):
        return self.get_queryset().active()
    
    
    
    def features(self):
        return self.get_queryset().is_featured()
    
    
        
    def in_solde(self):
        return self.get_queryset().in_solde()
    
    
    
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    
    
    def get_by_slug(self, slug):
        qs = self.get_queryset().active().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None
    
    
    def search(self, query):
        return self.get_queryset().active().search(query=query)
    
       
class Category(MPTTModel):
    cat_cku   = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    parent    = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title     = models.CharField(max_length = 150, unique=True, verbose_name='categorie')
    slug      = models.SlugField(max_length=150, unique=True, null=True, blank=True)
    active    = models.BooleanField(default=False)
    image     = models.ImageField(upload_to=upload_image_path, blank=True, null=True, height_field=None, width_field=None, max_length=None)
    timestamp = models.DateTimeField("date de creation", auto_now_add=True)
    updated   = models.DateTimeField("date de modification", auto_now=True)
    
    # objects = CategorieMPTTManager()
    
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Category, self).save(*args, **kwargs)

    
    
    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['title']
        verbose_name ='categorie'
        
    def get_absolute_url(self):
         return reverse("products:categorie", kwargs={"slug": self.slug})
    
    
    
    def __str__(self):
        return f'{self.title}'
      
    
    
class Product(models.Model):
    category   = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='categorie', related_name='products', null=True, blank=True)
    cku         = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    reference   = models.CharField(max_length=10, unique=True, editable=False)
    title       = models.CharField(max_length = 150, unique=True, verbose_name='Article')
    slug        = models.SlugField(max_length=50, unique=True, blank=True, null=True, editable=False)
    overview    = models.CharField(max_length=180, help_text='petite description de l\'article', default='')
    description = HTMLField()
    price       = models.DecimalField(
        max_digits=20,
        decimal_places=2, 
        verbose_name='prix', 
        validators=[
            MaxValueValidator(1000000000000),
            MinValueValidator(100)
        ]
    )
    specification = models.ForeignKey('Specification', on_delete=models.CASCADE, blank=True, null=True)
    image       = models.ManyToManyField('Upload')
    is_active   = models.BooleanField(default=True, verbose_name='Disponible ?')
    in_stock    = models.BooleanField("En stock ?", default=True)
    timestamp   = models.DateTimeField(auto_now_add=True, verbose_name='date ajout')
    is_digit    = models.BooleanField(verbose_name="support digital", default=False)
    featured    = models.BooleanField(default=False, verbose_name='articles phares')
    item_promo  = models.BooleanField(verbose_name="en promo", default=False)
    
    
    
    
    def get_downloads(self):
        qs = self.digitalproductfile_set.all()
        return qs
    
    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})
    
    
    @property
    def categorie(self):
        if self.category:
            return self.category.title
        return ''
    
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.cku)
        if not self.reference:
            self.reference = random_string_generator().upper()
        return super(Product, self).save(*args, **kwargs)
    
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        
        
    objects = ProductManager()
    
    @property
    def related(self):
        try:
            if self.category:
                return self.category.products.all().exclude(pk=self.pk)
        except Product.DoesNotExist:
            raise Http404("Aucun article trouvé !")
        return None
    
    
    
    @property
    def imageurl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    @staticmethod
    def get_all_product_by_categories(categorie_slug):
        if categorie_slug:
            return Product.objects.filter(categories__slug=categorie_slug)
        else:
            return Product.objects.all()


    def __str__(self):
        return f'{self.title}'
    
    




def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = random_string_generator()
        
        

pre_save.connect(product_pre_save_receiver, sender=Product)




class Upload(models.Model):
    products = models.CharField(
        verbose_name='produit',
        max_length=120,
        default='produit'
    )
    image = models.ImageField(
        'Image',
        upload_to=upload_image_path,
    )
    height = models.PositiveIntegerField(
        'Image Height',
        blank=True,
        null=True
    )
    width = models.PositiveIntegerField(
        'Image Width',
        blank=True,
        null=True
    )

    
    def __str__(self):
        return f'{self.products}'
    

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Image'
        
        

def upload_product_file_loc(instance, filename):
    slug = instance.products.slug 
    if not slug:
        slug = unique_slug_generator(instance.products)
    location = f"digital/item/product/{slug}/"  
    return location + filename  
        


class DigitalProductFile(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='article')
    file      = models.FileField(verbose_name='fichier', upload_to=upload_product_file_loc, max_length=100, 
                                 storage=FileSystemStorage(location=settings.PROTECTED_ROOT))
    free     = models.BooleanField(verbose_name="en telechargement libre ?", default=False)
    user_required = models.BooleanField(verbose_name="proprietaire exigé", default=False)
    

    class Meta:
        verbose_name = "Fichier Article Digital"
        verbose_name_plural ="Fichiers Articles Digitaux"

    def __str__(self):
        return f'{self.products.title}'

    def get_download_url(self):
        return reverse("products:download", kwargs={"slug": self.products.slug, "pk":self.pk})
    
    def get_default_url(self):
        return self.products.get_absolute_url()

    @property
    def name(self):
        return self.file.name
    
    
    
    
class HeroSection(models.Model):
    name = models.CharField(max_length = 150, verbose_name="titre", blank=True, null=True, default='hero')
    image = models.ImageField( upload_to=upload_image_path, height_field=None, width_field=None, max_length=None)
    

    

    class Meta:
        verbose_name ="Hero Section"
        verbose_name_plural ="Hero Sections"
        ordering = ('-id', )

    def __str__(self):
        return f'{self.name}'




class Content(models.Model):
    name = models.CharField(max_length = 150, verbose_name='contenu', unique=True)
    

    class Meta:
        verbose_name = "Contenu"
        verbose_name_plural = "Contenus"

    def __str__(self):
        return self.name





class Specification(models.Model):
    name = models.CharField(max_length = 150, unique=True)
    content = models.ManyToManyField(Content, verbose_name="valeur")


    class Meta:
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"

    def __str__(self):
        return self.name

