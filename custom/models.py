from django.db import models

class Year(models.Model):
    year = models.IntegerField()
    
    class Meta:
        ordering = ('-year',)
     
    def __str__(self):
        template = '{0.year}'
        return template.format(self)

class FiscalYear(models.Model):
    year = models.IntegerField()
    is_active = models.BooleanField(default=False, null=True, blank=True)
    def __str__(self):
        template = '{0.year}'
        return template.format(self)

class Fund(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Capital(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=5, null=True)
    def __str__(self):
        template = '{0.code} - {0.name}'
        return template.format(self)

class PType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class PTypes(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class PCategory(models.Model):
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=10, null=True)
    def __str__(self):
        template = '{0.code} - {0.name}'
        return template.format(self)

class PCat(models.Model):
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=10, null=True)
    def __str__(self):
        template = '{0.code} - {0.name}'
        return template.format(self)

class Owner(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class CType(models.Model): #contract type
    code = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        template = '{0.code} - {0.name}'
        return template.format(self)

class Book(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Sector(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class StatusProj(models.Model):
    code = models.CharField(max_length=2, null=True)
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class StatusPlan(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class StatusImp(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
##
class Country(models.Model):
    code = models.CharField(max_length=5, null=True)
    name = models.CharField(max_length=20, null=True)
    def __str__(self):
        template = '{0.name}'
        return template.format(self)

class Municipality(models.Model):
    code = models.CharField(max_length=5, null=True)
    name = models.CharField(max_length=20, null=True)
    hckey = models.CharField(max_length=10, null=True, blank=True)
    def __str__(self):
        template = '{0.name}'
        return template.format(self)

class AdministrativePost(models.Model):
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        template = '{0.municipality} - {0.name}'
        return template.format(self)

class Village(models.Model):
    administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        template = '{0.administrativepost} - {0.name}'
        return template.format(self)

class Aldeia(models.Model):
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        template = '{0.village} - {0.name}'
        return template.format(self)
###
class Ministery(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        template = '{0.name}'
        return template.format(self)

class Min(models.Model):
    code = models.CharField(max_length=5, null=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        template = '{0.name}'
        return template.format(self)

class DG(models.Model):
    code = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        template = '{0.name}'
        return template.format(self)

class Division(models.Model):
    dg = models.ForeignKey(DG, on_delete=models.CASCADE, null=True, related_name="division")
    code = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        template = '{0.name}'
        return template.format(self)

class Department(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, related_name="department")
    code = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        template = '{0.name}'
        return template.format(self)

class Section(models.Model):
    dep = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        template = '{0.name}'
        return template.format(self)
###
class Position(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        template = '{0.name}'
        return template.format(self)
    
class Program(models.Model):
    code = models.CharField(max_length=10, null=True, verbose_name="Kodigu")
    name = models.CharField(max_length=155, null=True, verbose_name="Programa")
    def __str__(self):
        template = '{0.name}'
        return template.format(self)
    
    

