from django.contrib import admin

from .models import *
from mptt.admin import *



@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','category', 'status', 'created_on', 'updated_on')
    search_fields = ('title', )
    list_filter = ('status', )
    list_editable = ('status', )
    
    
admin.site.register(Category)
admin.site.register(Comment, MPTTModelAdmin)
