from django.utils import timezone
from cv001.utils.uid import decode_id, encode_id
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Appointment(models.Model):
    APOINID = models.CharField(
        _("Appointment ID"), max_length=150, primary_key=True)
    UID = models.CharField(_("User ID"), max_length=150)
    OFID = models.CharField(_("Office ID"), max_length=150)
    actual_end_time = models.DateTimeField(
        _("Actual End Time"), blank=True, null=True)
    date = models.DateField()
    PST = models.TimeField(_('probable start time'))
    status= models.CharField(
        _("Status"), max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        phone = decode_id(self.UID)['p']
        apoind = encode_id(p=phone, t='appointment', ct=str(timezone.now()))
        self.APOINID = apoind
        super(Appointment, self).save(*args, **kwargs)


