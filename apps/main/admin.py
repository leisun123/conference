from django.contrib import admin

# Register your models here.

from apps.main.models import SideBar, GenericTagContent

class SideBarAdmin(admin.ModelAdmin):
    pass
    
class GenericTagContentAdmin(admin.ModelAdmin):
    pass

admin.site.register(SideBar, SideBarAdmin)
admin.site.register(GenericTagContent, GenericTagContentAdmin)
