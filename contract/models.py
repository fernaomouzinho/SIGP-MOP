from django.db import models
from django.contrib.auth.models import User
from custom.models import CType, StatusImp, StatusProj, DG, Division, Min
from company.models import Company
from project.models import Project
from .utils import upload_cont, upload_inv, upload_inv_sp

class Contract(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=False, related_name='contract')
    status = models.ForeignKey(StatusImp, on_delete=models.CASCADE, null=True, related_name="contract")
    type = models.ForeignKey(CType, on_delete=models.CASCADE, null=True, related_name="contract", verbose_name="Tipu Aprovisionamentu")
    number = models.CharField(max_length=100, null=True, unique=True, verbose_name="Numeru Kontratu")
    total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=False, verbose_name="Montante Kontratu")
    start_date = models.DateField(null=True, blank=False)
    end_date = models.DateField(null=True, blank=True)
    proc_year = models.IntegerField(null=True, blank=True, verbose_name="Tinan Tender")
    company_type = models.CharField(choices=[('Single','Single'),('Joint Venture','Joint Venture')], max_length=16, null=True, blank=False)
    desc = models.TextField(null=True, blank=True, verbose_name="Deskrisaun")
    is_fiscal = models.BooleanField(default=False, null=True, blank=False, verbose_name="Kontratu Fiskal")
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_lock = models.BooleanField(default=False, null=True, blank=True)
    is_ready = models.BooleanField(default=False, null=True, blank=True)
    is_complete = models.BooleanField(default=False, null=True, blank=True)
    is_stop = models.BooleanField(default=False, null=True, blank=True)
    stop_date = models.DateField(null=True, blank=True)
    stop_comment = models.TextField(null=True, blank=True, verbose_name="Rajaun Hapara")
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.project.code} - {0.number}'
        return template.format(self)

class ContractYear(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True, related_name='contractyear')
    total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=False, verbose_name="Montante")
    year = models.IntegerField(null=True, blank=True, verbose_name="Tinan Kontrantu")
    is_end = models.BooleanField(default=False, null=True, blank=True)
    def __str__(self):
        template = '{0.contract.number} - {0.year} - {0.total}'
        return template.format(self)

class ContractComp(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True, related_name='contractcomp')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='contractcomp')
    is_main = models.BooleanField(default=False, null=True)
    def __str__(self):
        #template = '{0.contract} - {0.company} - {0.is_main}'
        template = '{0.company}'
        return template.format(self)

class ContractFiles(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True, related_name='contractfiles')
    desc = models.CharField(max_length=100, null=True, verbose_name="Deskrisaun")
    file = models.FileField(upload_to=upload_cont, null=True, blank=False, verbose_name="Aneksu")
    def __str__(self):
        template = '{0.contract}'
        return template.format(self)
###
class Amendment(models.Model):
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, related_name="amendment")
    number = models.CharField(max_length=100, unique=True, null=True)
    total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    end_date = models.DateField(null=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.contract} - {0.total}'
        return template.format(self)

class AmendmentPeriod(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name='amendmentperiod')
    number = models.CharField(max_length=100, null=True, unique=True, verbose_name="Numeru Kontratu Foun")
    end_date = models.DateField(null=True)
    desc = models.CharField(max_length=20, null=True, blank=True, verbose_name="Deskrisaun")
    is_confirm = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    datetime= models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.number} - {0.end_date}'
        return template.format(self)

class AmendmentAmount(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name='amendmentamount')
    number = models.CharField(max_length=100, null=True, verbose_name="Numeru")
    total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=False)
    desc = models.CharField(max_length=20, null=True, blank=True, verbose_name="Deskrisaun")
    is_confirm = models.BooleanField(default=False, null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.number} - {0.total}'
        return template.format(self)

class Deduction(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name='deduction')
    total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=False)
    desc = models.CharField(max_length=20, null=True, blank=True, verbose_name="Deskrisaun")
    is_confirm = models.BooleanField(default=False, null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.contract.number} - {0.total}'
        return template.format(self)
###
class ContPay(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="contpay")
    contractyear = models.ForeignKey(ContractYear, on_delete=models.CASCADE, null=True, blank=True, related_name="contpay")
    com_amount = models.DecimalField(default=0, max_digits=11, decimal_places=2, null=True, blank=True)
    com_percent = models.DecimalField(default=0, max_digits=5, decimal_places=2, null=True, blank=True)
    bal_amount = models.DecimalField(default=0, max_digits=11, decimal_places=2, null=True, blank=True)
    bal_percent = models.DecimalField(default=0, max_digits=5, decimal_places=2, null=True, blank=True)
    phys_prog = models.DecimalField(default=0, max_digits=5, decimal_places=2, null=True, blank=True)
    def __str__(self):
        template = '{0.contract} - {0.com_amount}'
        return template.format(self)

