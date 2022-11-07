from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Advertise(models.Model):
    class StatusChoice(models.IntegerChoices):
        PENDING = 0, _("Pending")
        ACCEPTED = 1, _("Accepted")
        REJECTED = 2, _("REJECTED")


    description = models.CharField(max_length=1024, null=False, blank=False)
    email = models.CharField(max_length=32, null=False, blank=False)
    status = models.IntegerField(choices=StatusChoice.choices, default=StatusChoice.PENDING)
    category = models.CharField(max_length=256, null=True, blank=True)
    imageId = models.CharField(max_length=1024, null=True, blank=True)