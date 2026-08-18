from django.db import models
from django.contrib.auth.models import User
from custom.models import Section
from employee.models import Employee
from proc.models import Proc
from finance.models import CPVReq, CPV, PO
from eval.models import Eval
from invoice.models import Invoice
from ver.models import Ver
from insp.models import Insp

class CPVReqJustify(models.Model):
	cpvreq = models.ForeignKey(CPVReq, on_delete=models.CASCADE, null=True, related_name="cpvreqjust")
	comment = models.TextField(null=True, blank=True, verbose_name="Justifikasaun")
	is_dnof = models.BooleanField(default=False, null=True)
	is_dgaf = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		template = '{0.cpvreq}-{0.comment}'
		return template.format(self)

class CPVJustify(models.Model):
	cpv = models.ForeignKey(CPV, on_delete=models.CASCADE, null=True, related_name="cpvjustify")
	comment = models.TextField(null=True, blank=True, verbose_name="Justifikasaun")
	is_dnof = models.BooleanField(default=False, null=True)
	is_dgaf = models.BooleanField(default=False, null=True)
	is_gab = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		template = '{0.cpv}-{0.comment}'
		return template.format(self)

class POJustify(models.Model):
	po = models.ForeignKey(PO, on_delete=models.CASCADE, null=True, related_name="pojustify")
	comment = models.TextField(null=True, blank=True, verbose_name="Justifikasaun")
	is_dna = models.BooleanField(default=False, null=True)
	is_dgaf = models.BooleanField(default=False, null=True)
	is_gab = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		template = '{0.cpv}-{0.comment}'
		return template.format(self)
#
class EvalJustify(models.Model):
	eval = models.ForeignKey(Eval, on_delete=models.CASCADE, null=True, related_name="evaljustify")
	comment = models.TextField(null=True, blank=True)
	is_uvip = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		template = '{0.eval}-{0.comment}'
		return template.format(self)

class ProcJustify(models.Model):
	proc = models.ForeignKey(Proc, on_delete=models.CASCADE, null=True, related_name="procjustify")
	comment = models.TextField(null=True, blank=True, verbose_name="Justifikasaun")
	is_dna = models.BooleanField(default=False, null=True)
	is_dgaf = models.BooleanField(default=False, null=True)
	is_gab = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		template = '{0.proc}-{0.div}/{0.dg}-{0.comment}'
		return template.format(self)

class InvJustify(models.Model):
	inv = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, related_name="invjustify")
	comment = models.TextField(null=True, blank=True, verbose_name="Justifikasaun")
	is_sup = models.BooleanField(default=False, null=True)
	is_uvip = models.BooleanField(default=False, null=True)
	is_gab = models.BooleanField(default=False, null=True)
	is_dgaf = models.BooleanField(default=False, null=True)
	is_dna = models.BooleanField(default=False, null=True)
	is_dnof = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		template = '{0.inv}-{0.comment}'
		return template.format(self)

class VerJustify(models.Model):
	ver = models.ForeignKey(Ver, on_delete=models.CASCADE, null=True, related_name="verjustify")
	sec = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name="verjustify")
	eng = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="verjustify")
	comment = models.TextField(null=True, blank=True, verbose_name="Justifikasaun")
	is_uvip = models.BooleanField(default=False, null=True)
	is_sec = models.BooleanField(default=False, null=True)
	is_eng = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		template = '{0.verdiv}-{0.div}/{0.dep}/{0.sec}/{0.eng}-{0.comment}'
		return template.format(self)

class VerJustify2(models.Model):
	ver = models.ForeignKey(Ver, on_delete=models.CASCADE, null=True, related_name="verjustify2")
	sec = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name="verjustify2")
	eng = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="verjustify2")
	comment = models.TextField(null=True, blank=True, verbose_name="Justifikasaun")
	is_uvip = models.BooleanField(default=False, null=True)
	is_sec = models.BooleanField(default=False, null=True)
	is_eng = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		template = '{0.ver}-{0.sec}/{0.eng}-{0.comment}'
		return template.format(self)


class InspJustify(models.Model):
	insp = models.ForeignKey(Insp, on_delete=models.CASCADE, null=True, related_name="inspjustify")
	sec = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name="inspjustify")
	eng = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="inspjustify")
	comment = models.TextField(null=True, blank=True, verbose_name="Justifikasaun")
	is_uvip = models.BooleanField(default=False, null=True)
	is_sec = models.BooleanField(default=False, null=True)
	is_eng = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		template = '{0.insp}-{0.div}/{0.dep}/{0.sec}/{0.eng}-{0.comment}'
		return template.format(self)

class InspJustify2(models.Model):
	insp = models.ForeignKey(Insp, on_delete=models.CASCADE, null=True, related_name="inspjustify2")
	sec = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True, related_name="inspjustify2")
	eng = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name="inspjustify2")
	comment = models.TextField(null=True, blank=True, verbose_name="Justifikasaun")
	is_uvip = models.BooleanField(default=False, null=True)
	is_sec = models.BooleanField(default=False, null=True)
	is_eng = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		template = '{0.insp}-{0.sec}/{0.eng}-{0.comment}'
		return template.format(self)
