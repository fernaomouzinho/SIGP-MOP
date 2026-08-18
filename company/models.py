from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from custom.models import Municipality, Country

class Company(models.Model):
	name = models.CharField(max_length=200, verbose_name="Naran")
	reg_number = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nu. Registrasaun")
	start_date = models.DateField(null=True, blank=True)
	email = models.CharField(max_length=50, null=True, blank=True)
	phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Nu. Telemovel")
	website = models.CharField(max_length=50, null=True, blank=True)
	address = models.CharField(max_length=100, null=True, blank=True, verbose_name="Enderesu")
	type = models.CharField(choices=[('Nacional','Nacional'),('Internacional','Internacional')], max_length=15, null=True, blank=True, verbose_name="Kategoria")
	country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Nasaun")
	city = models.CharField(max_length=50, null=True, blank=True, verbose_name="Cidade")
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Municipiu")
	lat = models.CharField(max_length=20, null=True, blank=True, verbose_name="Latitude")
	lng = models.CharField(max_length=20, null=True, blank=True, verbose_name="Longitude")
	is_active = models.BooleanField(default=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	datetime = models.DateTimeField(null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class CompUser(models.Model):
	comp = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="compuser")
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		template = '{0.comp} - {0.user}'
		return template.format(self)
