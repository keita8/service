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
import random


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
            qs = Orders.objects.all().by_week_range(weekend_ago=5, number_of_weeks=5)
            if request.GET.get('type') == "week":
                
                days = 7
                start_date = timezone.now().today() - datetime.timedelta(days=days-1)
                datetime_list = []
                labels = []
                salesItems = []
                for x in range(0, days):
                    new_time = start_date + datetime.timedelta(days=x)
                    datetime_list.append(
                        new_time
                    )
                    labels.append(
                        new_time.strftime('%a')
                    )
                    
                    salesItems.append(
                        random.randint(3, 19291)
                    )
                    
                    

                # data['labels'] = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
                data['labels'] = labels
                data['data'] = salesItems
                # data['data'] = [298, 139, 405, 592, 822, 640, 375]
                
            if request.GET.get('type') == "4week":
                current = 4
                data['labels'] = ["Il ya 4 semaines", "Il ya 3 semaines", "Il ya 2 semaines", "Cette semaine"]
                data['data'] = []
                for x in range(0, 4):
                    new_qs = qs.by_week_range(weekend_ago=current, number_of_weeks=1)
                    sales_total = new_qs.totals_data()['total__sum']
                    if sales_total is None:
                        sales_total = 0
                    data['data'].append(sales_total)
                    current -= 1
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

    