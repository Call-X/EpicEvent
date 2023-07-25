from django.db import models
from client.models import CustomClient
from core.models import CustomUser
from datetime import datetime
from EpicEvent import settings
from core.models import CustomUser


class Contract(models.Model):
    client = models.ForeignKey(
        to=CustomClient,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={"is_prospect":False}
    )

    sales_contact = models.ForeignKey(
        to=CustomUser,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"usergroup": "Sale"}
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
    payment_due = models.DateTimeField()

    STATUS = (("OPEN", "Open"), ("SIGNED", "Contract Signed"), ("ENDED", "Ended"))

    event_status = models.CharField(
        max_length=32,
        choices=STATUS,
        default="OPEN",
    )

    def __str__(self):
        simply_payment = str(self.payment_due).split(" ")[0]
        display_name = f"{self.client} - {simply_payment}"
        return display_name

class Event(models.Model):
    
    contract = models.OneToOneField(
        to=Contract,
        on_delete=models.CASCADE,
        null=True, blank=True,
        limit_choices_to={"status": "OPEN"},
        related_name="event",

    )
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"usergroup": CustomUser.UserGroupe.SUPPORT},
    )
    event_status = models.BooleanField(default=False, verbose_name="Completed")
    attendees = models.PositiveIntegerField()
    event_date = models.DateTimeField(blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        name = f"{self.contract.client.last_name} {self.contract.client.first_name}"
        date = self.event_date.strftime("%Y-%m-%d")
        if self.event_status is False:
            event_state = "ON GOING"
        else:
            event_state = "DONE"

        return f"Event #{self.id} : {name} | Date : {date} | ({event_state})"
