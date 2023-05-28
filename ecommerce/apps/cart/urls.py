from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart, name='main'),
    path('api/cart/', cart_detail_api_view, name='api-cart'),
    path('update/', cart_update, name="update"),
    path('checkout/', chechout_homepage, name='checkout'),
    path('success/', checkout_done, name='success'),
    path('delete/', delete_cart, name='delete'),
]
