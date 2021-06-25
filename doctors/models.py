from time import timezone
from cv001.utils.uid import decode_id, encode_id
from django.db import models
from django.utils.translation import gettext_lazy as _


class doctor(models.Model):
    DOCID = models.CharField(_("DOCID"), primary_key=True, max_length=150)
    UID = models.CharField(
        _('UID'),
        max_length=150,
        help_text=('User id')
    )
    professional_statement = models.TextField(
        _('professional_statement'), null=True)  # detailed overview of the doctor’s qualifications
    # url for acessing this model
    slug = models.CharField(_("slug"), max_length=100, unique=True)
    # date from which the doctor is working in profession
    practicing_from = models.DateField(_('practicing from'), null=False)
    joined_at = models.DateTimeField(
        _("joined at"), auto_now=True)  # joining date

    def save(self, *args, **kwargs):
        phone = decode_id(self.UID)['p']
        docid = encode_id(p=phone, t='doc', ct=str(timezone.now()))
        self.DOCID = docid
        super(doctor, self).save(*args, **kwargs)


class specialization(models.Model):
    SPEID = models.CharField(_("specialization id"),
                             primary_key=True, max_length=150)
    name = models.CharField(
        _("specialization name"), null=False, max_length=150)

    def save(self, *args, **kwargs):
        id = encode_id(t='spec', ct=str(timezone.now()))
        self.SPEID = id
        super(specialization, self).save(*args, **kwargs)


class doc_specialization(models.Model):
    DOCID = models.CharField(_("doctor id"), null=False, max_length=150)
    SPEID = models.CharField(_("specialization id"),
                             null=False, max_length=150)


class qualification(models.Model):
    QID = models.CharField(_("Qualification id"),
                           primary_key=True, max_length=150)
    DOCID = models.CharField(_("doctor id"), null=False, max_length=150)
    name = models.CharField(_("Qualification name"),
                            null=False, max_length=150)
    institute = models.CharField(
        _("institute name"), null=False, max_length=150)
    year = models.DateField(_("procurement year"), null=False)

    def save(self, *args, **kwargs):
        phone = decode_id(self.DOCID)['p']
        qid = encode_id(p=phone, t='qual', ct=str(timezone.now()))
        self.QID = qid
        super(qualification, self).save(*args, **kwargs)


class hospital(models.Model):
    HOID = models.CharField(_("hospital id"), primary_key=True, max_length=150)
    DOCID = models.CharField(_("doctor id"), null=False, max_length=150)
    name = models.CharField(_("hospital name"), null=False, max_length=150)
    city = models.CharField(_("city"), max_length=150)
    start = models.DateField(_("start date"))
    end = models.DateField(_("end date"))

    def save(self, *args, **kwargs):
        phone = decode_id(self.DOCID)['p']
        hoid = encode_id(p=phone, t='hosp', ct=str(timezone.now()))
        self.HOID = hoid
        super(hospital, self).save(*args, **kwargs)
