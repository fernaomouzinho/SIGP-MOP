from django.db import models
from django.contrib.auth.models import User
from custom.models import Section,Position
from eval.models import Eval
from employee.models import Employee, EmployeePos
from .utils import upload_ver, upload_versec

class Ver(models.Model):
    eval = models.ForeignKey(Eval, on_delete=models.CASCADE, null=True, blank=True, related_name="ver")
    sec = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name="ver", verbose_name="Seksaun")
    epos = models.ForeignKey(EmployeePos, on_delete=models.CASCADE, null=True, blank=True, related_name="ver", verbose_name="Pozisaun")
    number = models.CharField(max_length=50, null=True, blank=False, verbose_name="Numeru")
    subject = models.CharField(max_length=200, null=True, blank=False, verbose_name="Asuntu")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True, verbose_name="Data Ikus")
    file = models.FileField(upload_to=upload_ver, null=True, blank=True, verbose_name="Aneksu")
    comments = models.TextField(null=True, blank=True, verbose_name="Komentariu UVIP")
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True, blank=True)
    is_back = models.BooleanField(default=False, null=True, blank=True)
    back_comment = models.TextField(null=True, blank=True, verbose_name="Komentariu")
    is_end = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.eval}: {0.number}'
        return template.format(self)

class VerSecEng(models.Model):
    ver = models.ForeignKey(Ver, on_delete=models.CASCADE, null=True, related_name="verseceng")
    sec = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name="verseceng")
    epos = models.ForeignKey(EmployeePos, on_delete=models.CASCADE, null=True, blank=True, related_name="verseceng", verbose_name="Pozisaun")
    to = models.ManyToManyField(Employee, null=True, through='VerSecEngEmployee', related_name="verseceng", verbose_name="Ba")
    number = models.CharField(max_length=50, null=True, blank=False, verbose_name="Numeru")
    subject = models.CharField(max_length=200, null=True, blank=False, verbose_name="Asuntu")
    date = models.DateField(null=True, blank=True)
    desc = models.TextField(null=True, blank=True, verbose_name="Deskrisaun")
    file = models.FileField(upload_to=upload_versec, null=True, blank=True, verbose_name="Aneksu")
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_send_read = models.BooleanField(default=False, null=True, blank=True)
    
    is_back = models.BooleanField(default=False, null=True, blank=True)
    is_back_read = models.BooleanField(default=False, null=True, blank=True)
    #
    is_eng_back = models.BooleanField(default=False, null=True, blank=True)
    is_eng_read = models.BooleanField(default=False, null=True, blank=True)
    
    STATUS_CHOICES = [
        ('PASA', 'Pasa'),
        ('DEVOLVE', 'Devolve'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PASA', verbose_name="Rezultadu Verifikasaun"
    )
    
    eng_comments = models.TextField(null=True, blank=True, verbose_name="Komentariu Enje&ntilde;eiru")
    file2 = models.FileField(upload_to=upload_versec, null=True, blank=True, verbose_name="Aneksu")
    #
    sec_comments = models.TextField(null=True, blank=True, verbose_name="Komentariu Xefe Seksaun")
    file3 = models.FileField(upload_to=upload_versec, null=True, blank=True, verbose_name="Aneksu")
    is_end = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.number}-{0.subject}'
        return template.format(self)

class VerSecEngEmployee(models.Model):
    verseceng = models.ForeignKey(VerSecEng, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
   
    def __str__(self):
        template = '{0.verseceng}'
        return template.format(self)

class VerTracks(models.Model):
    ver = models.ForeignKey(Ver, on_delete=models.CASCADE, null=True, related_name="vertracks")
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
        template = '{0.ver}-{0.stages}'
        return template.format(self)