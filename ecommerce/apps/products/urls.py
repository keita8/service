from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='main'),
    path('<slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('categorie/<int:id>/<slug:categorie_slug>/', views.categorie_products, name='categorie'),
    
]
