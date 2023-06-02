from django.db import models
from core.models import CustomUser

class CustomClient(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True, max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    mobile = models.CharField(max_length=20, unique=True, blank=True, null=True)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        to=CustomUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"usergroup": "Sale"},
    )
    is_prospect = models.BooleanField(blank=True, default=True)
    
    def __str__(self) -> str:
        return self.company_name
