from contracts.models import Contract
from rest_framework import serializers
from contracts.models import Event
from core.models import CustomUser

class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = [
            "id",
            "client",
            "client_name",
            "event_status",
            "sales_contact",
            "date_created",
            "date_updated",
            "amount",
            "payment_due",
        ]
        read_only_fields = ["id", "client", "client_name", "date_created"]
        
        def is_valid(self, data):
            if not CustomUser.objects.filter(
                    user=data['email'], contact=data['sales_contact']).exists():
                error_message = 'The sale_contact '\
                                + str(data['sales_contact'])\
                                + ' is not registered for the project.'
                raise serializers.ValidationError(error_message)
            return super().is_valid(data)
        
        def get_sales_contact_mail(self, obj):
            if obj.sales_contact is None:
                return "Not attributed yet"
            return obj.sales_contact.email

    sales_contact = serializers.SerializerMethodField("get_sales_contact_mail")
    client_name = serializers.SerializerMethodField("get_client_name")
    
    def get_client_name(self, obj):
        prettified_payment = str(obj.payment_due).split(" ")[0]
        display_name = f"{obj.client} - {prettified_payment}"
        return display_name

    def get_sales_contact_mail(self, obj):
        if obj.sales_contact is None:
            return "Not attributed yet"
        return (obj.sales_contact.email).is_valid()
    
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["id", "date_created", "date_updated", "support_contact", "event_status" ]