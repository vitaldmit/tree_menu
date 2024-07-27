from django.contrib import admin
from .models import MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'url', 'named_url', 'menu_name')
    list_filter = ('menu_name',)
    search_fields = ('name', 'url')


admin.site.register(MenuItem, MenuItemAdmin)
