from django.urls import *
from . import views

app_name = 'analytics'

urlpatterns = [
    path('sale/', views.SaleView.as_view(), name='sale'),
]
