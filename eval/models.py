from django.db import models
from django.contrib.auth.models import User
from custom.models import DG, Division
from project.models import Project
from eval.utils import *
import datetime

class Eval(models.Model):
    proj = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name="eval", verbose_name="Projetu")
    div = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True, related_name="eval")
    number = models.CharField(max_length=50, unique=True, null=True, verbose_name="Numeru Referensia")
    date = models.DateField(null=True, blank=False)
    desc = models.TextField(null=True, blank=True)
    is_adn = models.BooleanField(default=False, null=True, blank=True, verbose_name="Verifikasaun ADN")
    is_cna = models.BooleanField(default=False, null=True, blank=True, verbose_name="Ba CNA")
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True, blank=True)
    is_appr = models.BooleanField(default=False, null=True, blank=True)
    is_return = models.BooleanField(default=False, null=True, blank=True)
    return_comment = models.TextField(null=True, blank=True, verbose_name="Justifika Devolve")
    return_date = models.DateField(null=True, blank=False, verbose_name="Data Devolve")
    is_let_appr = models.BooleanField(default=False, null=True, blank=True)
    is_end = models.BooleanField(default=False, null=True)
    datetime = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hashed = models.CharField(max_length=32, null=True)
    def __str__(self):
        template = '{0.proj.code} - {0.number}'
        return template.format(self)

class EvalFile(models.Model):
    eval = models.ForeignKey(Eval, on_delete=models.CASCADE, null=True, related_name="evalfile")
    file_boq = models.FileField(upload_to=upload_boq, null=True, blank=False, verbose_name="Aneksu BOQ")
    file_design = models.FileField(upload_to=upload_design, null=True, blank=False, verbose_name="Aneksu Dezenu")
    file_spec = models.FileField(upload_to=upload_spec, null=True, blank=False, verbose_name="Aneksu Espesifikasaun")
    file_mapq = models.FileField(upload_to=upload_mapq, null=True, blank=False, verbose_name="Aneksu Mapa Quarry")
    file_docoth = models.FileField(upload_to=upload_docoth, null=True, blank=False, verbose_name="Aneksu Dokumentu Seluk")
    desc = models.CharField(max_length=200, null=True, blank=False, verbose_name="Deskrisaun")
    def __str__(self):
        template = '{0.eval}-{0.desc}'
        return template.format(self)

class EvalTrack(models.Model):
    eval = models.OneToOneField(Eval, on_delete=models.CASCADE, null=True, related_name="evaltrack")
    
    is_div_out = models.BooleanField(default=False, null=True)
    date_div_out = models.DateField(null=True, blank=True)
    
    is_uvip_in = models.BooleanField(default=False, null=True)
    date_uvip_in = models.DateField(null=True, blank=True)
    
    #
    is_ver_start = models.BooleanField(default=False, null=True)
    date_ver_start = models.DateField(null=True, blank=True)
    
    is_ver_end = models.BooleanField(default=False, null=True)
    date_ver_end = models.DateField(null=True, blank=True)
    
    #
    is_uvip_out_1 = models.BooleanField(default=False, null=True)
    date_uvip_out_1 = models.DateField(null=True, blank=True)
    
    #
    is_adn_in = models.BooleanField(default=False, null=True)
    date_adn_in = models.DateField(null=True, blank=True)
    
    #
    is_uvip_out_2 = models.BooleanField(default=False, null=True)
    date_uvip_out_2 = models.DateField(null=True, blank=True)
    
    #
    is_gab_in = models.BooleanField(default=False, null=True)
    date_gab_in = models.DateField(null=True, blank=True)
    
    #
    is_appr = models.BooleanField(default=False, null=True)
    date_appr = models.DateField(null=True, blank=True)
    
    #
    is_end = models.BooleanField(default=False, null=True)
    date_end = models.DateField(null=True, blank=True)
    
    stages = models.CharField(max_length=50, null=True)
    percent = models.IntegerField(null=True)
    def __str__(self):
        template = '{0.eval}-{0.stages} ({0.percent}%)'
        return template.format(self)


class EvalFITrack(models.Model):
    eval = models.OneToOneField(Eval, on_delete=models.CASCADE, null=True, related_name="evalfitrack")
    is_div_out = models.BooleanField(default=False, null=True) # to uivp
    date_div_out = models.DateField(null=True, blank=True)
    
    is_uvip_in_1 = models.BooleanField(default=False, null=True) # from div
    date_uvip_in_1 = models.DateField(null=True, blank=True)
    
    is_uvip_out_1 = models.BooleanField(default=False, null=True) #to adn
    date_uvip_out_1 = models.DateField(null=True, blank=True)
    
    is_uvip_in_2 = models.BooleanField(default=False, null=True) # from Adn
    date_uvip_in_2 = models.DateField(null=True, blank=True)

    is_uvip_out_2 = models.BooleanField(default=False, null=True) # to gab
    date_uvip_out_2 = models.DateField(null=True, blank=True)
    
    is_gab_in_1 = models.BooleanField(default=False, null=True) # from uivp
    date_gab_in_1 = models.DateField(null=True, blank=True)
    
    is_appr = models.BooleanField(default=False, null=True) # to aprove
    date_appr = models.DateField(null=True, blank=True)
    
    is_gab_out_1 = models.BooleanField(default=False, null=True) # To sgp
    date_gab_out_1 = models.DateField(null=True, blank=True)
    
    is_gab_in_2 = models.BooleanField(default=False, null=True) # from sgp
    date_gab_in_2 = models.DateField(null=True, blank=True)
    
    is_gab_out_2 = models.BooleanField(default=False, null=True) # to uvip
    date_gab_out_2 = models.DateField(null=True, blank=True)
    
    is_uvip_in_3 = models.BooleanField(default=False, null=True) # from uivp
    date_uvip_in_3 = models.DateField(null=True, blank=True)
    
    is_uvip_check = models.BooleanField(default=False, null=True) # to check
    date_uvip_check = models.DateField(null=True, blank=True)
    
    is_uvip_out_3 = models.BooleanField(default=False, null=True) # to gab
    date_uvip_out_3 = models.DateField(null=True, blank=True)
    

    is_gab_in_3 = models.BooleanField(default=False, null=True) # from uvip
    date_gab_in_3 = models.DateField(null=True, blank=True)
    
    is_let_appr = models.BooleanField(default=False, null=True) # to approve Deliberation
    date_let_appr = models.DateField(null=True, blank=True)
    
    is_gab_out_3 = models.BooleanField(default=False, null=True) # to cna-sgp-cna
    date_gab_out_3 = models.DateField(null=True, blank=True)
    
    is_gab_in_4 = models.BooleanField(default=False, null=True) # from cna-sgp-cna
    date_gab_in_4 = models.DateField(null=True, blank=True)
    
    is_gab_out_4 = models.BooleanField(default=False, null=True) # to UIVP
    date_gab_out_4 = models.DateField(null=True, blank=True)
    
    
    is_uvip_in_4 = models.BooleanField(default=False, null=True) # from GAB
    date_uvip_in_4 = models.DateField(null=True, blank=True)
    
    is_uvip_sign = models.BooleanField(default=False, null=True) # to sign
    date_uvip_sign = models.DateField(null=True, blank=True)
    
    is_uvip_out_4 = models.BooleanField(default=False, null=True) # to gab
    date_uvip_out_4 = models.DateField(null=True, blank=True)
    
    
    is_gab_in_5 = models.BooleanField(default=False, null=True) # from UIVP
    date_gab_in_5 = models.DateField(null=True, blank=True)
    
    is_gab_sign = models.BooleanField(default=False, null=True) # to sign
    date_gab_sign = models.DateField(null=True, blank=True)
    
    is_gab_out_5 = models.BooleanField(default=False, null=True) # to UIVP
    date_gab_out_5 = models.DateField(null=True, blank=True)
    
    
    is_uvip_in_5 = models.BooleanField(default=False, null=True) # from gab
    date_uvip_in_5 = models.DateField(null=True, blank=True)
    
    is_uvip_out_5 = models.BooleanField(default=False, null=True) # to gab
    date_uvip_out_5 = models.DateField(null=True, blank=True)
    
    is_end = models.BooleanField(default=False, null=True, verbose_name="Termina")
    date_end = models.DateField(null=True, blank=True)
    stages = models.CharField(max_length=50, null=True)
    percent = models.IntegerField(null=True)
    
    def current_entity(self):
        if self.is_gab_in_4:
            return "MOP"
        elif self.is_gab_out_3:
            return "SGP"
        elif self.is_gab_in_2:
            return "MOP"
        elif self.is_gab_out_1:
            return "SGP"
        elif self.is_uvip_in_2:
            return "MOP"
        elif self.is_uvip_out_1:
            return "ADN"
        elif self.is_uvip_in_1:
            return "MOP"
        return None  # not assigned yet
    
    def __str__(self):
        template = '{0.eval}-{0.stages} ({0.percent}%)'
        return template.format(self)
    
    
class LetTo(models.Model):
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        template = '{0.name}'
        return template.format(self)
    

class EvalLet(models.Model):
    eval = models.ForeignKey(Eval, on_delete=models.CASCADE, null=True, related_name="evalletter")
    to = models.ForeignKey(LetTo, on_delete=models.CASCADE, null=True, blank=False, related_name="evalletter", verbose_name="Diriji ba")
    number = models.CharField(max_length=100, unique=True, null=True, blank=False, verbose_name="Numeru Referensia")
    subject = models.CharField(max_length=200, null=True, blank=False, verbose_name="Asuntu")
    date = models.DateField(null=True, blank=True)
    desc = models.CharField(max_length=200, null=True, blank=True)
    file = models.FileField(upload_to=upload_eval, null=True, blank=True, verbose_name="Aneksu")
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True, blank=True)
    is_back = models.BooleanField(default=False, null=True, blank=True)
    comment = models.CharField(max_length=300, null=True, blank=True, verbose_name="Komentariu")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        #template = '{0.eval.id}-{0.eval}: {0.number}'
        template = '{0.id}'
        return template.format(self)

class EvalLetAdnBack(models.Model):
    evallet = models.ForeignKey(EvalLet, on_delete=models.CASCADE, null=True, related_name="evalletadnback")
    number = models.CharField(max_length=100, unique=True, null=True, blank=False, verbose_name="Numeru Referensia")
    subject = models.CharField(max_length=200, null=True, blank=False, verbose_name="Asuntu")
    date = models.DateField(null=True, blank=True, verbose_name="Data Karta")
    file = models.FileField(upload_to=upload_eval_adn, null=True, blank=True, verbose_name="Resibu Karta Simu")
    file_boq = models.FileField(upload_to=upload_eval_adn_boq, null=True, blank=False, verbose_name="Aneksu BOQ")
    file_design = models.FileField(upload_to=upload_eval_adn_design, null=True, blank=False, verbose_name="Aneksu Dezenu")
    file_spec = models.FileField(upload_to=upload_eval_adn_spec, null=True, blank=False, verbose_name="Aneksu Espesifikasaun")
    file_mapq = models.FileField(upload_to=upload_eval_adn_mapq, null=True, blank=False, verbose_name="Aneksu Mapa Quarry")
    file_docoth = models.FileField(upload_to=upload_eval_adn_docoth, null=True, blank=False, verbose_name="Aneksu Dokumentu Seluk")
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_back = models.BooleanField(default=False, null=True, blank=True)
    is_return = models.BooleanField(default=False, null=True, blank=True)
    is_result = models.BooleanField(default=False, null=True, blank=True)
    comment = models.CharField(max_length=300, null=True, blank=True, verbose_name="Komentariu")
    datetime = models.DateTimeField(null=True,verbose_name="Data Karta Simu")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    
    def __str__(self):
        template = '{0.evallet}: {0.number}'
        return template.format(self)
    
    
class EvalLetCNABack(models.Model):
    evallet = models.ForeignKey(EvalLet, on_delete=models.CASCADE, null=True, related_name="evalletcnaback")
    number = models.CharField(max_length=100, unique=True, null=True, blank=False, verbose_name="Numeru Referensia")
    subject = models.CharField(max_length=200, null=True, blank=False, verbose_name="Asuntu")
    date = models.DateField(null=True, blank=True, verbose_name="Data Karta")
    file = models.FileField(upload_to=upload_eval_adn, null=True, blank=True, verbose_name="Resibu Karta Simu")
    is_send = models.BooleanField(default=False, null=True, blank=True)
    is_back = models.BooleanField(default=False, null=True, blank=True)
    is_return = models.BooleanField(default=False, null=True, blank=True)
    is_result = models.BooleanField(default=False, null=True, blank=True)
    comment = models.CharField(max_length=300, null=True, blank=True, verbose_name="Komentariu")
    datetime = models.DateTimeField(null=True,verbose_name="Data Karta Simu")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hashed = models.CharField(max_length=32, null=True, blank=True)
    
    def __str__(self):
        template = '{0.evallet}: {0.number}'
        return template.format(self)

