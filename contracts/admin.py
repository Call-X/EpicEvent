from django.contrib import admin
from .models import Contract, Event
# Register your models here.
class ContractAdmin(admin.ModelAdmin):
    
    display_list = ("contract_info","sales_contact", "status")
    def contract_info(self, obj):
        return obj
        
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event)
