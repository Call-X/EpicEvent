from client.models import CustomClient
from rest_framework import serializers

class CustomClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomClient
        fields = [
            "id",
            "sales_contact",
            "first_name",
            "last_name",
            "email",
            "company_name",
            "phone",
            "is_prospect"
        ]
        
    read_only_fields = ("id",)
    sales_contact = serializers.SerializerMethodField("get_sales_contact_email")
    
    def get_sales_contact_email(self, obj):
        if obj.sales_contact is None:
            return "Not attributed yet"
        return obj.sales_contact.email