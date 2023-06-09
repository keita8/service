from django.contrib import admin
from import_export import resources
from .models import *
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportActionMixin

class ProductFileInline(admin.TabularInline):
    model = DigitalProductFile
    extra = 1


class ProductResource(resources.ModelResource):
    reference = Field(column_name="Reference")
    title = Field(column_name="Article")
    price = Field(column_name="Prix")
    is_active = Field(column_name="En stock")
    category = Field(column_name='categorie')
    timestamp = Field(column_name="Date")

    class Meta:
        model = Product
        fields = ("reference", "title", "price", "category", "is_active", "timestamp")
        export_order =("reference", "title", "price", "category", "is_active", "timestamp")


    def dehydrate_category(self, obj):
        return obj.category
    
    
    def dehydrate_reference(self, obj):
        return obj.reference

    def dehydrate_title(self, obj):
        return obj.title

    def dehydrate_price(self, obj):
        return f'{obj.price} GNF'

    def dehydrate_is_active(self, obj):
        if obj.is_active:
            return 'Oui'
        return 'Non'

    def dehydrate_timestamp(self, obj):
        return obj.timestamp.strftime('%d-%m-%Y à %H:%M')




@admin.register(Product)
class ProductAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_classes = [ProductResource]
    inlines = [ProductFileInline]
    list_display = ('reference', 'title', 'price', 'category', 'is_active', 'timestamp')
    list_display_links = ('reference', 'title')
    list_filter = ('is_active', )
    search_fields = ('title', )
    list_editable = ('is_active', 'category')
    
    




class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count','slug', 'active')
    list_display_links = ('indented_title', 'slug')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('active', )
    list_editable = ('active', )


    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'
    
admin.site.register(Category, CategoryAdmin)


admin.site.register(Upload)

admin.site.register(HeroSection)

admin.site.register(Specification)

admin.site.register(Content)