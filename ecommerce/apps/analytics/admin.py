from django.contrib import admin
from .models import *



#vT2kE#!Q8Qbx!4Q


@admin.register(ObjectView)
class ObjectViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'content_object', 'ip_address', 'timestamp')
    readonly_fields = ('ip_address', )
    search_fields = ('user', )
    

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user','ip_address', 'session_key')
    readonly_fields = ('ip_address', 'session_key')
    search_fields = ('user', )
    list_filter = ('user', )