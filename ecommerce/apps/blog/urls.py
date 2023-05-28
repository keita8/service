from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('search/', views.BlogSearchListView.as_view(), name='result'),
    path('', views.BlogListView.as_view(), name='main'),
    path('<str:slug>/', views.BlogDetailView.as_view(), name='detail'),
    path("<categorie>/", views.CategoriesListView, name="categorie"),
    path('categorie/<int:id>/', views.post_by_categorie, name='post_by_categorie'),
    
    path('', views.addcomment, name='comment'),
]
