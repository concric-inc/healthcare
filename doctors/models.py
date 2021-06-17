from django.db import models
from django.db.models.base import Model
from django.utils.translation import gettext_lazy as _


class doctor(models.Modle):
    DOCID = models.CharField(_("DOCID"), primary_key=True)
    UID = models.CharField(
        _('UID'),
        max_length=150,
        help_text=('User id')
    )
    professional_statement = models.TextField(
        _('professional_statement'), null=True)
    practicing_from = models.DateField(_('practicing from'), null=False)
    joined_at = models.DateTimeField(_("joined at"), auto_now=True)


class specialization(models.Model):
    SPEID = models.CharField(_("specialization id"), primary_key=True)
    specialization_name = models.CharField(
        _("specialization name"), null=False)


class doc_specialization(models.Model):
    DOCID = models.CharField(_("doctor id"), null=False)
    SPEID = models.CharField(_("specialization id"), null=False)


class qualification(models.Model):
    QID = models.CharField(_("Qualification id"), primary_key=True)
    DOCID = models.CharField(_("doctor id"), null=False)
    name = models.CharField(_("Qualification name"), null=False)
    institute = models.CharField(_("institute name"), null=False)
    year = models.DateField(_("procurement year"), null=False)


class hospital(models.Model):
    HOID = models.CharField(_("hospital id"), primary_key=True)
    DOCID = models.CharField(_("doctor id"), null=False)
    name = models.CharField(_("hospital name"),null=False)
    city = models.CharField(_("city"))
    start = models.DateField(_("start date"))
    end = models.DateField(_("end date"))
