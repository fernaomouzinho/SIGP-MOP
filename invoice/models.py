from django.db import models
from django.contrib.auth.models import User
from custom.models import Municipality
from contract.models import Contract
from .utils import upload_inv, upload_cert, upload_inv_let,upload_inv_let_dev_adn, upload_recom

class Invoice(models.Model):
    cont = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="Resibu")
    mun = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, blank=True, related_name="Resibu")
    number = models.CharField(max_length=255, unique=True, null=True, blank=False, verbose_name="Numeru Referensia")
    date = models.DateField(null=True, blank=True)
    phys_prog = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="Progresu")
    total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=False)
    file = models.FileField(upload_to=upload_inv, null=True, blank=True, verbose_name="Aneksu")
    desc = models.TextField(null=True, blank=True, verbose_name="Deskrisaun")
    is_adn = models.BooleanField(default=False, null=True, blank=True, verbose_name="Liu ADN")
    is_cna = models.BooleanField(default=False, null=True, blank=True, verbose_name="Liu CNA")
    is_sgp = models.BooleanField(default=False, null=True, blank=True, verbose_name="Liu SGP")
    is_insp = models.BooleanField(default=False, null=True, blank=True)
    is_lock = models.BooleanField(default=False, null=True)
    is_ready = models.BooleanField(default=False, null=True)
    is_appr = models.BooleanField(default=False, null=True)
    is_paid = models.BooleanField(default=False, null=True)
    is_end = models.BooleanField(default=False, null=True)	
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.cont}: {0.number}'
        return template.format(self)

class InvTrack(models.Model):
    inv = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, related_name="invtrack")
    is_sup_out = models.BooleanField(default=False, null=True)
    date_sup_out = models.DateField(null=True, blank=True)
    #
    is_uvip_in = models.BooleanField(default=False, null=True)
    date_uvip_in = models.DateField(null=True, blank=True)
    #
    is_insp_start = models.BooleanField(default=False, null=True)
    date_insp_start = models.DateField(null=True, blank=True)
    
    is_insp_end = models.BooleanField(default=False, null=True)
    date_insp_end = models.DateField(null=True, blank=True)
    #
    is_uvip_out_1 = models.BooleanField(default=False, null=True)
    date_uvip_out_1 = models.DateField(null=True, blank=True) # This is submission to ADN
    #
    is_adn_in = models.BooleanField(default=False, null=True) # Return from ADN, it is not submission to ADN
    date_adn_in = models.DateField(null=True, blank=True)
    #
    is_uvip_out_2 = models.BooleanField(default=False, null=True)
    date_uvip_out_2 = models.DateField(null=True, blank=True)
    #
    is_gab_in = models.BooleanField(default=False, null=True)
    date_gab_in = models.DateField(null=True, blank=True)
    
    is_gap_app = models.BooleanField(default=False, null=True)
    date_gab_app = models.DateField(null=True, blank=True)
    
    is_gab_out = models.BooleanField(default=False, null=True)
    date_gab_out = models.DateField(null=True, blank=True)
    #
    is_dgaf_in = models.BooleanField(default=False, null=True)
    date_dgaf_in = models.DateField(null=True, blank=True)
    
    is_dgaf_out = models.BooleanField(default=False, null=True)
    date_dgaf_out = models.DateField(null=True, blank=True)
    #
    is_dna_in = models.BooleanField(default=False, null=True)
    date_dna_in = models.DateField(null=True, blank=True)
    is_dna_out = models.BooleanField(default=False, null=True)
    date_dna_out = models.DateField(null=True, blank=True)
    #
    is_dnof_in = models.BooleanField(default=False, null=True)
    date_dnof_in = models.DateField(null=True, blank=True)
    
    is_dnof_out = models.BooleanField(default=False, null=True)
    date_dnof_out = models.DateField(null=True, blank=True)
    
    is_dnof_middle_out = models.BooleanField(default=False, null=True)
    date_dnof_middle_out = models.DateField(null=True, blank=True)

    is_dnof_back_in = models.BooleanField(default=False, null=True)
    date_dnof_back_in = models.DateField(null=True, blank=True)
    
    is_dnof_back_insp_start = models.BooleanField(default=False, null=True)
    date_dnof_back_insp_start = models.DateField(null=True, blank=True)

    is_dnof_back_insp_end = models.BooleanField(default=False, null=True)
    date_dnof_back_insp_end = models.DateField(null=True, blank=True)

    is_dnof_back_cre_start = models.BooleanField(default=False, null=True)
    date_dnof_back_cre_start = models.DateField(null=True, blank=True)

    is_dnof_back_cre_end = models.BooleanField(default=False, null=True)
    date_dnof_back_cre_end = models.DateField(null=True, blank=True)

    is_dnof_back_apr_start = models.BooleanField(default=False, null=True)
    date_dnof_back_apr_start= models.DateField(null=True, blank=True)
    is_dnof_back_apr_end = models.BooleanField(default=False, null=True)
    date_dnof_back_apr_end= models.DateField(null=True, blank=True)

    is_dnof_back_out = models.BooleanField(default=False, null=True)
    date_dnof_back_out = models.DateField(null=True, blank=True)
    #
    stages = models.CharField(default="SUP", max_length=50, null=True, blank=True)
    percent = models.IntegerField(default=0, null=True, blank=True)
    def __str__(self):
        template = '{0.inv}-{0.stages}'
        return template.format(self)
###
class LetTo(models.Model):
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        template = '{0.name}'
        return template.format(self)

class InvLet(models.Model):
    inv = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, related_name="invlet")
    mun = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, blank=True, related_name="invlet")
    to = models.ForeignKey(LetTo, on_delete=models.CASCADE, null=True, blank=False, related_name="invlet", verbose_name="Ba")
    number = models.CharField(max_length=255, unique=True, null=True, blank=False, verbose_name="Numeru Referensia")
    subject = models.CharField(max_length=200, null=True, blank=False, verbose_name="Asuntu")
    date = models.DateField(null=True, blank=True)
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="Deskrisaun")
    file = models.FileField(upload_to=upload_inv_let, null=True, blank=True, verbose_name="Aneksu Dokumentu (.pdf)")
    is_sup = models.BooleanField(default=False, null=True, blank=True)
    is_uvip = models.BooleanField(default=False, null=True, blank=True)
    is_gab = models.BooleanField(default=False, null=True, blank=True)
    is_dgaf = models.BooleanField(default=False, null=True, blank=True)
    is_dna = models.BooleanField(default=False, null=True, blank=True)
    is_dnof = models.BooleanField(default=False, null=True, blank=True)
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True, blank=True)
    is_back = models.BooleanField(default=False, null=True, blank=True)
    is_adn_back = models.BooleanField(default=False, null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.inv.cont.project.code}: {0.number}-{0.subject}'
        return template.format(self)
    
class InvLetAdnBack(models.Model):
    invlet = models.ForeignKey(InvLet, on_delete=models.CASCADE, null=True, related_name="invletadnback")
    number = models.CharField(max_length=100, unique=True, null=True, blank=False, verbose_name="Numeru Referensia ADN")
    subject = models.CharField(max_length=200, null=True, blank=False, verbose_name="Asuntu")
    date = models.DateField(null=True, blank=True, verbose_name="Data Karta")
    file = models.FileField(upload_to=upload_inv_let_dev_adn, null=True, blank=True, verbose_name="Aneksu Dokumentu (.pdf)")
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_back = models.BooleanField(default=False, null=True, blank=True)
    is_return = models.BooleanField(default=False, null=True, blank=True)
    comment = models.CharField(max_length=300, null=True, blank=True, verbose_name="Komentariu")
    datetime = models.DateTimeField(null=True,verbose_name="Data Karta Simu")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    
    def __str__(self):
        template = '{0.invlet}: {0.number}'
        return template.format(self)
    
#
class CertPay(models.Model):
    inv = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, related_name="certpay")
    number = models.CharField(max_length=255, unique=True, null=True, blank=False, verbose_name="Numeru Referensia")
    number_req = models.CharField(max_length=4, unique=True, null=True, blank=False, verbose_name="Numeru Serifikadu")
    date = models.DateField(null=True, blank=True)
    phys_prog = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="Progresu Fiziku")
    total = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=False, verbose_name="Montante Pagamentu")
    type = models.CharField(choices=[('Initial','Initial'),('Final','Final')], max_length=10, null=True, blank=True, verbose_name="Tipu")
    desc = models.TextField(null=True, blank=True, verbose_name="Deskrisaun")
    file = models.FileField(upload_to=upload_cert, null=True, blank=False, verbose_name="Aneksu Dokumentu(.pdf)")
    is_lock = models.BooleanField(default=False, null=True)
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.inv}-{0.total}'
        return template.format(self)

class PayRecom(models.Model):
    cont = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="payrecom")
    inv = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, related_name="payrecom")
    term = models.CharField(max_length=3, null=True, blank=False, verbose_name="Numeru Resibu/IPC")
    number = models.CharField(max_length=255, unique=True, null=True, blank=False, verbose_name="Numeru Referensia")
    date = models.DateField(null=True, blank=True)
    phys_prog = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=False, verbose_name="Progresu Fiziku")
    amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=False, verbose_name="Montante Pagamentu")
    desc = models.TextField(null=True, blank=True, verbose_name="Deskrisaun")
    file = models.FileField(upload_to=upload_recom, null=True, blank=True, verbose_name="Aneksu Sertifikadu Pagamentu (.pdf)")
    is_lock = models.BooleanField(default=False, null=True)
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        template = '{0.inv}-{0.amount}'
        return template.format(self)
    
        