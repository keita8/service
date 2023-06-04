from django.shortcuts import render
from django.http import *
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, PermissionRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from ecommerce.apps.order.models import Orders
from django.contrib.auth import logout
from django.db.models import *
import datetime
from django.utils import timezone


class LogoutIfNotStaffMixin(AccessMixin):
        def dispatch(self, request, *args, **kwargs):
            if not request.user.is_staff:
                logout(request)
                return self.handle_no_permission()
            return super(LogoutIfNotStaffMixin, self).dispatch(request, *args, **kwargs)







class SaleAjaxView(View):

    def dispatch(self, *args, **kwargs):

        user = self.request.user
        if not user.is_staff:
            template_name = 'analytics/400.html'
            return HttpResponseRedirect("/")
            return render(self.request, template_name, status=401)
            # return render(self.request, 'analytics/400.html', {})

            # return HttpResponse("Vous n'êtes pas autorisé", status=401)
        return super(SaleAjaxView, self).dispatch(*args, **kwargs)
    
    
    def get(self, request, *args, **kwargs):
        data = {}
        if request.user.is_staff:
            if request.GET.get('type') == "week":
                data['labels'] = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
                data['data'] = [298, 139, 405, 592, 822, 640, 375]
            if request.GET.get('type') == "4week":
                data['labels'] = ["Semaine dernière", "Il ya 2 semaines", "Il ya 3 semaines", "Il ya un mois"]
                data['data'] = [ 592, 822, 640, 375]
        return JsonResponse(data=data)

    








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

        qs = Orders.objects.all().by_week_range(weekend_ago=10, number_of_weeks=10)
        context['today'] = qs.by_range(start_date=timezone.now().date()).get_sales_breakdown()
        context['this_week'] = qs.by_week_range(weekend_ago=1, number_of_weeks=1).get_sales_breakdown()
        context['last_four_week'] = qs.by_week_range(weekend_ago=5, number_of_weeks=4).get_sales_breakdown()
        
        return context

    