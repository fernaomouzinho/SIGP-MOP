from django.db import models
from django.contrib.auth.models import User
from contract.models import Contract, ContractYear
from invoice.models import Invoice
from custom.models import Program
from custom.models import Year, FiscalYear, Fund, Capital, PType, PCategory, PCat, Owner, CType

class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="payment")
    contyear = models.ForeignKey(ContractYear, on_delete=models.CASCADE, null=True, blank=True, related_name="payment")
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, null=True, blank=True, related_name="payment")
    phys_prog = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Progresu Fiziku")
    total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Montante")
    com_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    com_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bal_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    bal_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="Deskrisaun")
    is_lock = models.BooleanField(default=False, null=True)
    is_ready = models.BooleanField(default=False, null=True)
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.contract} - {0.total} - {0.date}'
        return template.format(self)

class PaymentHist(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="paymenthist")
    phys_prog = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    desc = models.CharField(max_length=20, null=True)
    total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    com_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    com_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    bal_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    bal_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    date = models.DateField(null=True, blank=True)
    info = models.CharField(max_length=20, null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.contract} - {0.total}'
        return template.format(self)
#
class PaymentFiscal(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="paymentfiscal")
    year = models.IntegerField(null=True, blank=True, verbose_name="Tinan Fiskal")
    com_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    com_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bal_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)   
    bal_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="Deskrisaun")
    is_active = models.BooleanField(default=False, null=True)
    is_end = models.BooleanField(default=False, null=True)
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        template = '{0.contract} - {0.year}'
        return template.format(self)


class PhysicalProgress(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="physicalprogress") 
    prog_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name="Progresu Fiziku Atual")
    date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        template = '{0.contract} - {0.year}'
        return template.format(self)
    
class PaymentPortal(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, related_name="paymentportal", verbose_name="Programa")
    pcategory = models.ForeignKey(PCategory, on_delete=models.CASCADE, null=True, related_name="paymentportal", verbose_name="Kategoria")
    amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Montante")
    percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Persentajem")
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True, blank=True, related_name="paymentportal", verbose_name="Tinan") 
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.program} - {0.year}'
        return template.format(self)
    