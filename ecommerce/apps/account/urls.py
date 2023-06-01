from django.urls import include, path
from . import views
from django.contrib.auth.views import *
from django.views.generic import *
from django.urls import path
from django.contrib.auth import views as auth_views 
from ecommerce.apps.products.views import UserProductHistoryView
from ecommerce.apps.order.views import OrderDetailView, OrderListView, LibraryView, VerifyOwnership


app_name = 'account'

urlpatterns = [
    path('', views.AccountHomeView.as_view(), name='dashboard'),

    # path('profile/', views.)
    # path('', views.account_home_view, name='dashboard'),
    path("login/", views.login_page, name="login"),
    # path('login/', views.LoginUserView.as_view(), name='login'),
    
    
    path('login/', RedirectView.as_view(url='/login')),
    path("guest/", views.guest_login_page, name="guest_register"),
    path('logout/', views.logout_user, name='logout'),
    path("register/", views.register_page, name="register"),
    
    
    path('user/update/', views.UserDetailUpdateView.as_view(), name='user-update'),
    
    
    
    
    path("password/change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password/change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password/reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password/reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password/reset/complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),




    path('history/products/', UserProductHistoryView.as_view(), name='history-product'),
    
    path('', OrderListView.as_view(), name='orders'),
    path('order/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('digital/', LibraryView.as_view(), name='digital-items'),
    path('verify/ownership/', VerifyOwnership.as_view(), name='verify-ownership'),
]
