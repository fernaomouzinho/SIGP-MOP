from django.db import models
from django.contrib.auth.models import User
from project.models import Project
from contract.models import Contract
from invoice.models import Invoice
from .utils import upload_cpvreq, upload_cpv, upload_po, upload_cpv_let, upload_po_let,\
    upload_prt, upload_ev, upload_fin_files

class LetTo(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        template = '{0.name}'
        return template.format(self)

class CPVReq(models.Model):
    proj = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name="cpvreq", verbose_name="Projetu")
    subject = models.CharField(max_length=200, null=True, blank=True, verbose_name="Asuntu")
    number = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Numeru Rekizasaun CPV")
    date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to=upload_cpvreq, null=True, blank=True, verbose_name="Aneksu")
    is_send = models.BooleanField(default=False, null=True)
    is_read = models.BooleanField(default=False, null=True)
    is_back = models.BooleanField(default=False, null=True)
    is_appr = models.BooleanField(default=False, null=True)
    comment = models.CharField(max_length=200, null=True, blank=True)
    is_end = models.BooleanField(default=False, null=True)
    status = models.CharField(max_length=30, null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.proj.code} - {0.date}'
        return template.format(self)

class CPVReqTrack(models.Model):
    cpvreq = models.ForeignKey(CPVReq, on_delete=models.CASCADE, null=True, related_name="cpvreqtrack")
    is_dnof_out = models.BooleanField(default=False, null=True)
    date_dnof_out = models.DateField(null=True, blank=True)
    is_dgaf_in = models.BooleanField(default=False, null=True)
    date_dgaf_in = models.DateField(null=True, blank=True)
    is_appr = models.BooleanField(default=False, null=True)
    date_appr = models.DateField(null=True, blank=True)
    is_end = models.BooleanField(default=False, null=True)
    date_end = models.DateField(null=True, blank=True)
    stages = models.CharField(max_length=50, null=True, blank=True)
    percent = models.IntegerField(null=True, blank=True)
    def __str__(self):
        template = '{0.cpvreq.proj.code}-{0.stages} ({0.percent}%)'
        return template.format(self)

class CPV(models.Model):
    proj = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name="cpv", verbose_name="Projetu")
    number = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Numeru CPV")
    amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Montante")
    date = models.DateField(null=True, blank=True)
    line_item = models.IntegerField(null=True, blank=True)
    file = models.FileField(upload_to=upload_cpv, null=True, blank=True, verbose_name="Aneksu")
    is_dgaf = models.BooleanField(default=False, null=True)
    is_send = models.BooleanField(default=False, null=True)
    is_read = models.BooleanField(default=False, null=True)
    is_back = models.BooleanField(default=False, null=True)
    is_appr = models.BooleanField(default=False, null=True)
    is_commit = models.BooleanField(default=False, null=True)
    comment = models.CharField(max_length=200, null=True, blank=True)
    is_end = models.BooleanField(default=False, null=True)
    is_get_dna = models.BooleanField(default=False, null=True)
    group = models.CharField(max_length=5, null=True, blank=True)
    status = models.CharField(max_length=130, null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.number}'
        return template.format(self)

class CPVTrack(models.Model):
    cpv = models.ForeignKey(CPV, on_delete=models.CASCADE, null=True, related_name="cpvtrack")
    is_dnof_out = models.BooleanField(default=False, null=True)
    date_dnof_out = models.DateField(null=True, blank=True)
    is_dgaf_in = models.BooleanField(default=False, null=True)
    date_dgaf_in = models.DateField(null=True, blank=True)
    is_appr = models.BooleanField(default=False, null=True)
    date_appr = models.DateField(null=True, blank=True)
    is_dgaf_out = models.BooleanField(default=False, null=True)
    date_dgaf_out = models.DateField(null=True, blank=True)
    is_dnof_in = models.BooleanField(default=False, null=True)
    date_dnof_in = models.DateField(null=True, blank=True)
    is_end = models.BooleanField(default=False, null=True)
    date_end = models.DateField(null=True, blank=True)
    stages = models.CharField(max_length=50, null=True, blank=True)
    percent = models.IntegerField(null=True, blank=True)
    def __str__(self):
        template = '{0.cpv.number}-{0.stages} ({0.percent}%)'
        return template.format(self)

class CPVLetter(models.Model):
    cpv = models.ForeignKey(CPV, on_delete=models.CASCADE, null=True, related_name="cpvletter")
    number = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Numeru Referensia")
    subject = models.CharField(max_length=200, null=True, blank=True, verbose_name="Asuntu")
    date = models.DateField(null=True, blank=True)
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="Komentariu")
    file = models.FileField(upload_to=upload_cpv_let, null=True, blank=True, verbose_name="Aneksu")
    is_dgaf = models.BooleanField(default=False, null=True, blank=True)
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.cpv}: {0.subject}'
        return template.format(self)
###
class PO(models.Model):
    cont = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True, related_name="po")
    cpv = models.ForeignKey(CPV, on_delete=models.CASCADE, null=True, blank=False, related_name="po")
    inv = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True, related_name="po", verbose_name="Invoice")
    number = models.CharField(max_length=50, unique=True, null=True, blank=False, verbose_name="Numeru PO")
    amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Montante")
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="Deskrisaun")
    date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to=upload_po, null=True, blank=True, verbose_name="Aneksu")
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True, blank=True)
    is_back = models.BooleanField(default=False, null=True, blank=True)
    is_appr = models.BooleanField(default=False, null=True)
    comment = models.CharField(max_length=200, null=True, blank=True)
    is_end = models.BooleanField(default=False, null=True)
    status = models.CharField(max_length=30, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.number}'
        return template.format(self)

class POTrack(models.Model):
    po = models.ForeignKey(PO, on_delete=models.CASCADE, null=True, related_name="potrack")
    is_dna_out = models.BooleanField(default=False, null=True)
    date_dna_out = models.DateField(null=True, blank=True)
    is_dgaf_in = models.BooleanField(default=False, null=True)
    date_dgaf_in = models.DateField(null=True, blank=True)
    is_appr = models.BooleanField(default=False, null=True)
    date_appr = models.DateField(null=True, blank=True)
    is_dgaf_out = models.BooleanField(default=False, null=True)
    date_dgaf_out = models.DateField(null=True, blank=True)
    is_dna_in = models.BooleanField(default=False, null=True)
    date_dna_in = models.DateField(null=True, blank=True)
    is_end = models.BooleanField(default=False, null=True)
    date_end = models.DateField(null=True, blank=True)
    stages = models.CharField(max_length=50, null=True, blank=True)
    percent = models.IntegerField(null=True, blank=True)
    def __str__(self):
        template = '{0.po.number}-{0.stages} ({0.percent}%)'
        return template.format(self)

class POLetter(models.Model):
    po = models.ForeignKey(PO, on_delete=models.CASCADE, null=True, related_name="poletter")
    number = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Numeru")
    subject = models.CharField(max_length=200, null=True, blank=True, verbose_name="Asuntu")
    date = models.DateField(null=True, blank=True)
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="Komentariu")
    file = models.FileField(upload_to=upload_po_let, null=True, blank=True, verbose_name="Aneksu")
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.po}: {0.subject}'
        return template.format(self)
###
class PRT(models.Model):
    cont = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="prt")
    inv = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True, related_name="prt")
    number = models.CharField(max_length=50, unique=True, null=True, blank=False, verbose_name="Numeru")
    date = models.DateField(null=True, blank=True)
    total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Montante")
    percent = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    file = models.FileField(upload_to=upload_prt, null=True, blank=True, verbose_name="Aneksu")
    is_ready = models.BooleanField(default=False, null=True)
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.cont}-{0.number}'
        return template.format(self)
###
class EV(models.Model):
    cont = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="ev")
    inv = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True, related_name="ev")
    prt = models.ForeignKey(PRT, on_delete=models.CASCADE, null=True, blank=True, related_name="ev")
    number = models.CharField(max_length=50, unique=True, null=True, blank=False, verbose_name="Numeru")
    date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to=upload_ev, null=True, blank=True, verbose_name="Aneksu")
    is_ready = models.BooleanField(default=False, null=True)
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_receive = models.BooleanField(default=False, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True)
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.prt}-{0.number}'
        return template.format(self)
###
class TPO(models.Model):
    proj = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name="tpo")
    cont = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="tpo")
    inv = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, related_name="tpo")
    number = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Numeru")
    date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Montante")
    is_ready = models.BooleanField(default=False, null=True)
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.proj}-{0.number}'
        return template.format(self)
###
class FinFiles(models.Model):
    proj = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name="finfiles")
    cont = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="finfiles")
    inv = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, related_name="finfiles")
    desc = models.CharField(max_length=200, null=True, blank=False, verbose_name="Deskrisaun")
    file = models.FileField(upload_to=upload_fin_files, null=True, blank=False, verbose_name="Aneksu")
    is_lock = models.BooleanField(default=False, null=True, blank=True)
    is_ready = models.BooleanField(default=False, null=True, blank=True)
    is_dna = models.BooleanField(default=False, null=True, blank=True)
    is_dnof = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        template = '{0.inv}-{0.desc}'
        return template.format(self)