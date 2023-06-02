from django.contrib import admin

# Register your models here.
from .models import CustomClient


class ClientAdmin(admin.ModelAdmin):
    list_display = ("company_name", "sales_contact", "first_name", "last_name", "is_prospect", "id")
    list_filter = ("sales_contact", "first_name", "last_name", "is_prospect")


admin.site.register(CustomClient, ClientAdmin)
