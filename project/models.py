from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from custom.models import Book, Capital, Division, Fund, Municipality, AdministrativePost,\
    PCategory, PType, Sector, StatusPlan, StatusProj, Village, Aldeia, Year, PCat, Program, PTypes

class Project(models.Model):
    code = models.CharField(max_length=15, unique=True, null=True, blank=False, verbose_name="Kodigu Projetu")
    code_act = models.CharField(max_length=15, unique=True, null=True, blank=False, verbose_name="Kodigu Aktividade")
    name = models.CharField(max_length=600, null=True, blank=False, verbose_name="Naran Projetu")
    name2 = models.CharField(max_length=600, null=True, blank=True, verbose_name="Naran Projetu-2")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True, related_name='project', verbose_name="Programa") 
    owner = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=False, related_name='project', verbose_name="Donu Projetu")
    capital = models.ForeignKey(Capital, on_delete=models.CASCADE, null=True, blank=True, related_name='project', verbose_name="Kapital")
    pcategory = models.ForeignKey(PCategory, on_delete=models.CASCADE, null=True, blank=False, related_name='project', verbose_name="Kategoria")
    pcat = models.ForeignKey(PCat, on_delete=models.CASCADE, null=True, blank=True, related_name='project', verbose_name="Kategoria MOP")
    statusproj = models.ForeignKey(StatusProj, on_delete=models.CASCADE, null=True, blank=True, related_name='project', verbose_name="Status Orsamentu")
    status = models.ForeignKey(StatusPlan, on_delete=models.CASCADE, null=True, blank=True, related_name='project', verbose_name="Status Planu")
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True, blank=True, related_name='project', verbose_name="Setor")
    ptype = models.ForeignKey(PType, on_delete=models.CASCADE, null=True, blank=True, related_name='project', verbose_name="Tipu")
    ptypes = models.ForeignKey(PTypes, on_delete=models.CASCADE, null=True, blank=True, related_name='project', verbose_name="Tipu Projetu")
    
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, null=True, blank=True, related_name='project', verbose_name="Fundus")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True, related_name='project', verbose_name="Livru")
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True, blank=False, related_name='project', verbose_name="Tinan Projetu")
    alocate_bd = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Alokasaun Orsamentu")
    YEAR_CHOICES = [(r,r) for r in range(2010, datetime.date.today().year+1)]
    year_alocate_bd = models.IntegerField(_('Tinan Alokasaun Orsamentu'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="Deskrisaun")
    is_active = models.BooleanField(default=True, null=True)
    is_read = models.BooleanField(default=False, null=True)
    is_lock = models.BooleanField(default=False, null=True)
    is_ready = models.BooleanField(default=False, null=True)
    is_eval = models.BooleanField(default=False, null=True)
    is_cont = models.BooleanField(default=False, null=True)
    is_adn = models.BooleanField(default=False, null=True, verbose_name="Verifika Liu ADN")
    is_end = models.BooleanField(default=False, null=True)
    datetime = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hashed = models.CharField(max_length=32, null=True)
    def __str__(self):
        template = '{0.code} - {0.name}'
        return template.format(self)

class ProjectLoc(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='projectloc')
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Munisipiu")
    administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Postu")
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Suku")
    aldeia = models.ForeignKey(Aldeia, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Aldeia")
    start_lat = models.CharField(max_length=20, null=True, blank=True)
    start_lng = models.CharField(max_length=20, null=True, blank=True)
    end_lat = models.CharField(max_length=20, null=True, blank=True)
    end_lng = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        template = '{0.project} - {0.municipality}'
        return template.format(self)

class ProjectEst(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='projectest')
    owner = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Estimasaun Donu")
    adn = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="ADN")
    balance = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    is_lock = models.BooleanField(default=False, null=True)
    is_ready = models.BooleanField(default=False, null=True)
    def __str__(self):
        template = '{0.project} - {0.owner}'
        return template.format(self)
    
class ProjectImg(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='projectimg')
    image = models.ImageField(upload_to = 'image_data', null=True, blank=True, default='adn.png')
    
    class Meta:
        verbose_name_plural = _("Project Galleria")

    def __str__(self):
        template = '{0.project.code}-{0.project.name}'
        return template.format(self)
    