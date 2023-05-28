from django.contrib import admin
from .models import *

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'timestamp')
    list_display_links = ('name', )
    search_fields = ('name', 'email')
    readonly_fields = ('timestamp', )