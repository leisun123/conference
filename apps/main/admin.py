from django.contrib import admin

# Register your models here.

from apps.main.models import SideBar, GenericTagContent

class SideBarAdmin(admin.ModelAdmin):
    exclude = ['created_time, last_mod_time']
    
class GenericTagContentAdmin(admin.ModelAdmin):
    exclude = ['created_time, last_mod_time, status']

admin.site.register(SideBar, SideBarAdmin)
admin.site.register(GenericTagContent, GenericTagContentAdmin)
