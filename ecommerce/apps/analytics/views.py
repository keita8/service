from django.shortcuts import render
from django.http import *
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, PermissionRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from ecommerce.apps.order.models import Orders
from django.contrib.auth import logout
from django.db.models import *



class LogoutIfNotStaffMixin(AccessMixin):
        def dispatch(self, request, *args, **kwargs):
            if not request.user.is_staff:
                logout(request)
                return self.handle_no_permission()
            return super(LogoutIfNotStaffMixin, self).dispatch(request, *args, **kwargs)

class SaleView( PermissionRequiredMixin, LogoutIfNotStaffMixin, LoginRequiredMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'analytics/sale.html'
    
    def dispatch(self, *args, **kwargs):

        user = self.request.user
        if not user.is_staff:
            template_name = 'analytics/400.html'
            return HttpResponseRedirect("/")
            return render(self.request, template_name, status=401)
            # return render(self.request, 'analytics/400.html', {})

            # return HttpResponse("Vous n'êtes pas autorisé", status=401)
        return super(SaleView, self).dispatch(*args, **kwargs)

    
    def get_context_data(self, *args, **kwargs):
        context = super(SaleView, self).get_context_data(*args, **kwargs)
        qs = Orders.objects.all()
        print(qs)
        context["orders"] = qs
        context['recent_orders'] = qs.recent().not_refunded()[:5]
        recent_orders_total = 0
        for i in context['recent_orders']:
            print(i)
            # recent_orders_total += i.get_cart_items
            recent_orders_total += i.total
            
        context['recent_orders_total'] = context['recent_orders'].aggregate(
                                                                        Sum('total'), 
                                                                        Avg('total'), 
                                                                        # Avg('cart__products__price'), 
                                                                        # Count("cart__products")
                                                                        )
        
        
        context['recent_orders_cart'] = context['recent_orders'].aggregate(
                                                                        Sum('cart__products__price'),
                                                                        Avg('cart__products__price'), 
                                                                        Count("cart__products")
                                                                        )
        context['shipped_orders'] = qs.recent().not_refunded().by_status(status='shipped')[:5]
        context['paid_orders'] = qs.recent().not_refunded().by_status(status='paid')[:5]

        print(qs)
        return context

    