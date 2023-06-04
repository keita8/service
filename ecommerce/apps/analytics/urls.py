from django.urls import *
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.SaleView.as_view(), name='sale'),
    path('sales/data/', views.SaleAjaxView.as_view(), name='data'),
]
