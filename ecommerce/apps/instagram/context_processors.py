from .models import *

def instagramm(request):
    insta_shot = Insta.objects.all()[:6]
    return dict(insta=insta_shot)
    