from .models import *

def about(request):
    about_us = About.objects.first()
    return dict(about=about_us)