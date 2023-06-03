from django.contrib import admin
from import_export import resources
from .models import *
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportActionMixin


class CartResource(resources.ModelResource):
    user = Field(column_name="Client")
    total = Field(column_name="Prix du panier")
    updated = Field(column_name="Modification")
    timestamp = Field(column_name="Date de creation")

    class Meta:
        model = Product
        fields = ("user", "total", "updated", "timestamp")
        export_order =("user", "total", "updated", "timestamp")

    def dehydrate_user(self, obj):
        return obj.user

    def dehydrate_total(self, obj):
        return f'{obj.total} GNF'


    def dehydrate_updated(self, obj):
        return obj.updated.strftime('%d-%m-%Y à %H:%M')


    def dehydrate_timestamp(self, obj):
        return obj.timestamp.strftime('%d-%m-%Y à %H:%M')




@admin.register(Cart)
class ProductAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_classes = [CartResource]
    list_display = ('id', 'total', 'updated', 'timestamp')
    list_display_links = ('id', 'total')
    list_filter = ('updated', 'timestamp')
    search_fields = ('id',  )
    readonly_fields = ("total", )