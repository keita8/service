from django.contrib import admin
from import_export import resources
from .models import *
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportActionMixin


class OrderResource(resources.ModelResource):
    order_id = Field(column_name="N° de commande")
    cart = Field(column_name="Panier")
    status = Field(column_name="Status")
    total = Field(column_name="Total")
    timestamp = Field(column_name="Date de creation")

    class Meta:
        model = Orders
        fields = ("order_id", "cart", "status", "total", "timestamp")
        export_order =("order_id", "cart", "status", "total", "timestamp")

    def dehydrate_order_id(self, obj):
        return obj.order_id

    # def dehydrate_cart(self, obj):
    #     return obj.cart

    def dehydrate_status(self, obj):
        if obj.status == "created":
            return "créée"
        elif obj.status == "paid":
            return "payée"
        elif obj.status == "shipped":
            return "livrée"
        else:
            return "remboursée"

    
    def dehydrate_total(self, obj):
        return f"{obj.total} GNF"
    
    
    def dehydrate_timestamp(self, obj):
        return obj.timestamp.strftime('%d-%m-%Y à %H:%M')



# class OrderItemResource(resources.ModelResource):
#     order = Field(column_name="N° de commande")
#     product = Field(column_name="article")
#     quantity = Field(column_name="quantity")
#     date_added = Field(column_name="date d'ajout")

#     class Meta:
#         model = OrderItem
#         fields = ("order", "product", "quantity", "date_added")
#         export_order =("order", "product", "quantity", "date_added")

#     def dehydrate_order(self, obj):
#         return obj.order


#     def dehydrate_product(self, obj):
#         return obj.product


    
#     def dehydrate_quantity(self, obj):
#         return obj.quantity
    
    
#     def dehydrate_date_added(self, obj):
#         return obj.date_added.strftime('%d-%m-%Y à %H:%M')




# @admin.register(OrderItem)
# class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
#     resource_classes = [OrderItemResource]
#     list_display = ("order", "product", "quantity", "date_added")
#     list_display_links =("order", "product")
#     list_filter =("order", "date_added", )
#     search_fields = ('order', )
#     readonly_fields = (  "date_added",)
    

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('transaction_id', 'customer', 'completed', 'date_ordered')
#     search_fields = ('transaction_id', )
#     list_filter = ('completed', 'transaction_id', 'date_ordered')
#     readonly_fields = ('transaction_id', "completed", "status")


#     order_id       = models.CharField(max_length = 150, verbose_name='N° commande', blank=True)
#     cart           = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='panier')
#     status         = models.CharField(max_length = 150, choices=ORDER_STATUS, default="created")
#     shipping_total = models.DecimalField(max_digits=100, decimal_places=2, default=9.99, verbose_name="frais de livraison")
#     total          = models.DecimalField(max_digits=100, decimal_places=2, default=0.00, verbose_name="total")
#     timestamp      = models.DateTimeField(verbose_name="date de creation", default=now)
#     active         = models.BooleanField(default=True)
    
    
    
    
    
    
@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'cart', 'get_status', 'total', 'timestamp', 'active')
    search_fields = ('order_id', 'status')
    list_filter = ( 'status', )
    exclude = ('billing_address', )
    readonly_fields = ('order_id','cart', 'total', 'timestamp', )




@admin.register(ProductPurchase)
class ProductPurchaseAdmin(admin.ModelAdmin):
    list_display = ('order','product', 'refunded', )
    list_display_links = ('order', 'product')
    readonly_fields = ('order', 'product')
    search_fields = ('order', 'refunded')