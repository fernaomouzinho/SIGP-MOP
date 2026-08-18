from django.db import models
from django.contrib.auth.models import User
from contract.models import Contract
from custom.models import Section
from invoice.models import Invoice
from employee.models import Employee, EmployeePos
from .utils import upload_insp, upload_inspsec

class Insp(models.Model):
    cont = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="insp")
    inv = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True, related_name="insp")
    sec = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name="insp", verbose_name="Seksaun")
    epos = models.ForeignKey(EmployeePos, on_delete=models.CASCADE, null=True, blank=True, related_name="insp", verbose_name="Pozisaun")
    number = models.CharField(max_length=50, null=True, blank=False, verbose_name="Numeru")
    subject = models.CharField(max_length=200, null=True, blank=False, verbose_name="Asuntu")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True, verbose_name="Data Ikus")
    file = models.FileField(upload_to=upload_insp, null=True, blank=True, verbose_name="Aneksu")
    comments = models.TextField(null=True, blank=True, verbose_name="Komentariu UVIP")
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True, blank=True)
    is_back = models.BooleanField(default=False, null=True, blank=True)
    back_comment = models.TextField(null=True, blank=True, verbose_name="Komentariu")
    is_end = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.cont}: {0.number}'
        return template.format(self)


class InspSecEng(models.Model):
    insp = models.ForeignKey(Insp, on_delete=models.CASCADE, null=True, related_name="inspseceng")
    sec = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name="inspseceng")
    to = models.ManyToManyField(Employee, null=True, through='InspSecEngEmployee', related_name="inspseceng", verbose_name="Ba")
    number = models.CharField(max_length=50, null=True, blank=False, verbose_name="Numeru")
    subject = models.CharField(max_length=200, null=True, blank=False, verbose_name="Asuntu")
    date = models.DateField(null=True, blank=True)
    desc = models.TextField(null=True, blank=True, verbose_name="Deskrisaun")
    file = models.FileField(upload_to=upload_inspsec, null=True, blank=True, verbose_name="Aneksu")
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_send_read = models.BooleanField(default=False, null=True, blank=True)
    is_back = models.BooleanField(default=False, null=True, blank=True)
    is_back_read = models.BooleanField(default=False, null=True, blank=True)
    #
    is_eng_back = models.BooleanField(default=False, null=True, blank=True)
    is_eng_read = models.BooleanField(default=False, null=True, blank=True)
    eng_comments = models.TextField(null=True, blank=True, verbose_name="Komentariu Enje&ntilde;eiru")
    file2 = models.FileField(upload_to=upload_inspsec, null=True, blank=True, verbose_name="Aneksu")
    #
    sec_comments = models.TextField(null=True, blank=True, verbose_name="Komentariu Xefe Seksaun")
    file3 = models.FileField(upload_to=upload_inspsec, null=True, blank=True, verbose_name="Aneksu")
    is_end = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.number}-{0.subject}'
        return template.format(self)

class InspSecEngEmployee(models.Model):
    inspseceng = models.ForeignKey(InspSecEng, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
   
    def __str__(self):
        template = '{0.inspseceng}'
        return template.format(self)

class InspTracks(models.Model):
    insp = models.ForeignKey(Insp, on_delete=models.CASCADE, null=True, related_name="insptracks")
    is_start = models.BooleanField(default=False, null=True, blank=True)
    date_start = models.DateField(null=True, blank=True)
    is_uvip_out = models.BooleanField(default=False, null=True, blank=True)
    date_uvip_out = models.DateField(null=True, blank=True)
    is_sec_in_1 = models.BooleanField(default=False, null=True, blank=True)
    date_sec_in_1 = models.DateField(null=True, blank=True)
    is_sec_out_1 = models.BooleanField(default=False, null=True, blank=True)
    date_sec_out_1 = models.DateField(null=True, blank=True)
    is_eng_in = models.BooleanField(default=False, null=True, blank=True)
    date_eng_in = models.DateField(null=True, blank=True)
    is_eng_out = models.BooleanField(default=False, null=True, blank=True)
    date_eng_out = models.DateField(null=True, blank=True)
    is_sec_in_2 = models.BooleanField(default=False, null=True, blank=True)
    date_sec_in_2 = models.DateField(null=True, blank=True)
    is_sec_out_2 = models.BooleanField(default=False, null=True, blank=True)
    date_sec_out_2 = models.DateField(null=True, blank=True)
    is_uvip_in = models.BooleanField(default=False, null=True, blank=True)
    date_uvip_in = models.DateField(null=True, blank=True)	
    is_end = models.BooleanField(default=False, null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    stages = models.CharField(max_length=250, null=True, blank=True)
    percent = models.IntegerField(null=True, blank=True)
    def __str__(self):
        template = '{0.insp}-{0.stages}'
        return template.format(self)