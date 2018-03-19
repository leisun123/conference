from django.contrib import admin

# Register your models here.

from apps.accounts.models import Scholar

class ScholarAdmin(admin.ModelAdmin):
    exclude = ['password', 'is_staff', 'is_active', 'date_joined', 'avatar']
    
admin.site.register(Scholar ,ScholarAdmin)