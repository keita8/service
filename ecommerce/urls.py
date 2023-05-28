
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import dj_database_url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (handler400, handler403, handler404, handler500)
from ecommerce.apps.account.views import LoginView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns







urlpatterns = [
    

    path('accounts/', include('ecommerce.apps.account.urls', namespace='accounts')),
    path('analytics/', include('ecommerce.apps.analytics.urls', namespace='analytics')),
    path("checkout/address/", include("ecommerce.apps.addresses.urls", namespace="address")),
    path('contact/', include('ecommerce.apps.contact.urls', namespace='contact')),
    path('order/', include('ecommerce.apps.order.urls', namespace='order')),
    path('billing/', include("ecommerce.apps.billing.urls", namespace="billing")),
    path('marketing/', include('ecommerce.apps.marketing.urls', namespace='marketing')),
    path('blog/', include('ecommerce.apps.blog.urls', namespace='blog')),
    path('about-us/', include('ecommerce.apps.about.urls', namespace='about')),
    path('shop/', include('ecommerce.apps.shop.urls', namespace='shop')),
    path('cart/', include('ecommerce.apps.cart.urls', namespace='cart')),
    path('search/', include('ecommerce.apps.search.urls', namespace='search')),
    path('tinymce/', include('tinymce.urls')),
    path("admin/", admin.site.urls),
    path('', include('ecommerce.apps.products.urls', namespace='products')),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
urlpatterns += staticfiles_urlpatterns()
    
admin.site.site_header ='IT-SERVICES'                    # default: "Django Administration"
admin.site.index_title ="Interface d'administration"                 # default: "Site administration"
admin.site.site_title = 'IT-SERVICES'  # default: "Django site admin"



handler404 = "core.apps.products.views.handle404"

*
urlpatterns += staticfiles_urlpatterns()