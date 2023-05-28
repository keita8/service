from django.utils.text import slugify
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import os 
import random
from django.urls import reverse
from tinymce.models import HTMLField
from django.db.models import Q
from mptt.models import MPTTModel, TreeForeignKey

User = settings.AUTH_USER_MODEL
#User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, verbose_name='redacteur', on_delete=models.CASCADE)

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def blog_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f"blog/{new_filename}/{final_filename}"





class BlogQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(status=1)
    
    def search(self, query):
        lookups =( 
                   Q(title__icontains=query) 
                  |Q(description__icontains=query) 
                  |Q(content__icontains=query)
                  |Q(keywords__icontains=query)
                )
        
        return self.filter(lookups).distinct()





class BlogManager(models.Manager):
    
    def get_queryset(self):
        return BlogQuerySet(self.model, using=self._db)
    

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
    
    
    def search(self, query):
        return self.get_queryset().active().search(query=query)
    
    





STATUS = (
    (0, "Brouillon"),
    (1, "Publié")
)


class Category(models.Model): #Category for the Article
    title = models.CharField(max_length=200) #Title of the Category
    created_on = models.DateTimeField(auto_now_add=True) #Date of creation
    is_active  = models.BooleanField("activé", default=True)

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='titre') #Title of the Article
    slug = models.SlugField(max_length=200, unique=True, editable=False, blank=True, null=True) #Unique identifier for the article
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='redacteur') #Author of the Article
    description = models.CharField(max_length=100) #Short Description of the article
    content = HTMLField(verbose_name="contenu") #Content of the article, you need to install CKEditor
    category = models.ForeignKey('Category', related_name='category', on_delete=models.CASCADE, verbose_name='categorie') #Category of the article
    keywords = models.CharField(max_length=250, verbose_name='mot clé') #Keywords to be used in SEO
    cover = models.ImageField(upload_to=blog_image_path, verbose_name='image') #Cover Image of the article
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='date de creation') #Date of creation
    updated_on = models.DateTimeField(auto_now=True, verbose_name='date de modification') #Date of updation
    status = models.IntegerField(choices=STATUS, default=0) #Status of the Article either Draft or Published


    objects = BlogManager()
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        return super(BlogPost, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", args=[str(self.slug)])



class Comment(MPTTModel):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments', verbose_name='article')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length = 150, verbose_name='nom')
    email = models.EmailField(max_length=254)
    content = models.TextField(help_text='message', verbose_name='contenu')
    publish = models.DateTimeField("publication", auto_now_add=True)
    
    
    
    class MPTTMeta:
        order_insertion_by = ['publish']
        
    
    def __str__(self):
        return self.name
    
    