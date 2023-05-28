from .models import *

def blog_latest(request):
    latest_post = BlogPost.objects.all().order_by('-id')
    queryset    = Category.objects.all().order_by('-id').filter(is_active=True)
    return dict(latest_post=latest_post, queryset=queryset)