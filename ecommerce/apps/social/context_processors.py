from .models import *

def link(request):
    links = Social.objects.first()
    return dict(links=links)