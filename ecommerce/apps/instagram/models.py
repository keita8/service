from django.db import models
import os 
import random


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_insta_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f"products/{new_filename}/{final_filename}"



class Insta(models.Model):
    name  = models.CharField(max_length = 150, unique=True)
    link  = models.URLField(max_length = 200)
    image = models.ImageField(upload_to=upload_insta_image_path, height_field=None, width_field=None, max_length=None)
    
    def __str__(self):
        return self.name
    
    
    