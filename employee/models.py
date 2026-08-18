from django.db import models
from django.contrib.auth.models import User
from custom.models import DG, Division, Department, Section, Position, Municipality

class Employee(models.Model):
    name = models.CharField(max_length=100, null=True)
    pob = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(choices=[('Male','Male'),('Female','Female')], max_length=6, null=True, blank=True)
    email = models.CharField(max_length=50, blank=True, null=True,unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True,unique=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    datetime = models.DateTimeField(null=True)
    hashed = models.CharField(max_length=32, null=True)
    def __str__(self):
        template = '{0.name}'
        return template.format(self)

class EmployeePos(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="employeepos")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, related_name="employeepos")
    cat = models.CharField(choices=[('Verifikasaun','Verifikasaun'),('Inspeksaun','Inspeksaun')], max_length=16, null=True, blank=True, verbose_name="Category")
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        template = '{0.employee} | {0.position} | {0.cat}'
        return template.format(self)

class EmployeeDiv(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="employeediv")
    dg = models.ForeignKey(DG, on_delete=models.CASCADE, null=True, blank=True, related_name="employeediv")
    div = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True, related_name="employeediv")
    dep = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name="employeediv")
    sec = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name="employeediv")
    mun = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, blank=True, related_name="employeediv")
    datetime = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        template = '{0.employee} | {0.dg} | {0.div} | {0.dep} | {0.sec}'
        return template.format(self)

class EmployeeUser(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="employeeuser")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        template = '{0.employee} - {0.user}'
        return template.format(self)
