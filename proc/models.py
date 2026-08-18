import datetime, os
from django.db import models
from django.contrib.auth.models import User
from project.models import Project
from .utils import upload_proc, upload_procfiles

class Proc(models.Model):
	proj = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name="proc", verbose_name="Projetu")
	number = models.CharField(max_length=50, unique=True, null=True, blank=False, verbose_name="Numeru Referensia")
	date = models.DateField(null=True, blank=True)
	desc = models.TextField(null=True, blank=True, verbose_name="Dekrisaun")
	is_lock = models.BooleanField(default=False, null=True)
	is_req_start = models.BooleanField(default=False, null=True)
	is_req_appr = models.BooleanField(default=False, null=True)
	is_req_end = models.BooleanField(default=False, null=True)
	is_res_start = models.BooleanField(default=False, null=True)
	is_res_appr = models.BooleanField(default=False, null=True)
	is_res_end = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.proj.code}'
		return template.format(self)

class ProcComp(models.Model):
	proc = models.ForeignKey(Proc, on_delete=models.CASCADE, null=True, related_name="proccomp")
	company = models.CharField(max_length=100, null=True, blank=True)
	submit_date = models.DateField(null=True, blank=True)
	best = models.IntegerField(null=True, blank=True)
	is_win = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.proc} - {0.company} - {0.best}'
		return template.format(self)

class ProcReqTrack(models.Model):
	proc = models.ForeignKey(Proc, on_delete=models.CASCADE, null=True, related_name="procreqtrack")
	is_start = models.BooleanField(default=False, null=True, blank=True)
	date_start = models.DateField(null=True, blank=True)
	is_dna_out = models.BooleanField(default=False, null=True, blank=True)
	date_dna_out = models.DateField(null=True, blank=True)
	is_dgaf_in_1 = models.BooleanField(default=False, null=True, blank=True)
	date_dgaf_in_1 = models.DateField(null=True, blank=True)
	is_dgaf_out_1 = models.BooleanField(default=False, null=True, blank=True)
	date_dgaf_out_1 = models.DateField(null=True, blank=True)
	is_gab_in = models.BooleanField(default=False, null=True, blank=True)
	date_gab_in = models.DateField(null=True, blank=True)
	is_gab_out = models.BooleanField(default=False, null=True, blank=True)
	date_gab_out = models.DateField(null=True, blank=True)
	is_dgaf_in_2 = models.BooleanField(default=False, null=True, blank=True)
	date_dgaf_in_2 = models.DateField(null=True, blank=True)
	is_dgaf_out_2 = models.BooleanField(default=False, null=True, blank=True)
	date_dgaf_out_2 = models.DateField(null=True, blank=True)
	is_dna_in = models.BooleanField(default=False, null=True, blank=True)
	date_dna_in = models.DateField(null=True, blank=True)
	is_end = models.BooleanField(default=False, null=True, blank=True)
	date_end = models.DateField(null=True, blank=True)
	stages = models.CharField(max_length=200, null=True)
	percent = models.IntegerField(null=True)
	def __str__(self):
		template = '{0.proc}-{0.stages} ({0.percent}%)'
		return template.format(self)

class ProcResTrack(models.Model):
	proc = models.ForeignKey(Proc, on_delete=models.CASCADE, null=True, related_name="procrestrack")
	is_start = models.BooleanField(default=False, null=True, blank=True)
	date_start = models.DateField(null=True, blank=True)
	is_dna_out = models.BooleanField(default=False, null=True, blank=True)
	date_dna_out = models.DateField(null=True, blank=True)
	is_dgaf_in_1 = models.BooleanField(default=False, null=True, blank=True)
	date_dgaf_in_1 = models.DateField(null=True, blank=True)
	is_dgaf_out_1 = models.BooleanField(default=False, null=True, blank=True)
	date_dgaf_out_1 = models.DateField(null=True, blank=True)
	is_gab_in = models.BooleanField(default=False, null=True, blank=True)
	date_gab_in = models.DateField(null=True, blank=True)
	is_gab_out = models.BooleanField(default=False, null=True, blank=True)
	date_gab_out = models.DateField(null=True, blank=True)
	is_dgaf_in_2 = models.BooleanField(default=False, null=True, blank=True)
	date_dgaf_in_2 = models.DateField(null=True, blank=True)
	is_dgaf_out_2 = models.BooleanField(default=False, null=True, blank=True)
	date_dgaf_out_2 = models.DateField(null=True, blank=True)
	is_dna_in = models.BooleanField(default=False, null=True, blank=True)
	date_dna_in = models.DateField(null=True, blank=True)
	is_end = models.BooleanField(default=False, null=True, blank=True)
	date_end = models.DateField(null=True, blank=True)
	stages = models.CharField(max_length=200, null=True)
	percent = models.IntegerField(null=True)
	def __str__(self):
		template = '{0.proc}-{0.stages} ({0.percent}%)'
		return template.format(self)

class ProcTrack(models.Model):
	proc = models.ForeignKey(Proc, on_delete=models.CASCADE, null=True, related_name="proctrack")
	is_announce = models.BooleanField(default=False, null=True, blank=True, verbose_name="Anunsia")
	date_announce = models.DateField(null=True, blank=True)
	is_open = models.BooleanField(default=False, null=True, blank=True, verbose_name="Open Bid")
	date_open = models.DateField(null=True, blank=True)
	is_eval = models.BooleanField(default=False, null=True, blank=True, verbose_name="Avaliasaun")
	date_eval = models.DateField(null=True, blank=True)
	is_result = models.BooleanField(default=False, null=True, blank=True, verbose_name="Rezultadu")
	date_result = models.DateField(null=True, blank=True)
	stages = models.CharField(max_length=200, null=True)
	percent = models.IntegerField(null=True)
	def __str__(self):
		template = '{0.proc}-{0.stages}'
		return template.format(self)
###
class LetTo(models.Model):
	name = models.CharField(max_length=50, null=True, blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class ProcLet(models.Model):
	proc = models.ForeignKey(Proc, on_delete=models.CASCADE, null=True, related_name="proclet")
	to = models.ForeignKey(LetTo, on_delete=models.CASCADE, null=True, blank=False, related_name="proclet",verbose_name="Diriji ba")
	number = models.CharField(max_length=50,  unique=True, null=True, blank=False, verbose_name="Numeru Referensia")
	subject = models.CharField(max_length=200, null=True, blank=False, verbose_name="Asuntu")
	date = models.DateField(null=True, blank=True)
	desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="Deskrisaun")
	file = models.FileField(upload_to=upload_proc, null=True, blank=True, verbose_name="Aneksu (.pdf)")
	is_req = models.BooleanField(default=False, null=True, blank=True)
	is_dgaf = models.BooleanField(default=False, null=True, blank=True)
	is_send = models.BooleanField(default=False, null=True, blank=True)
	is_read = models.BooleanField(default=False, null=True, blank=True)
	is_back = models.BooleanField(default=False, null=True, blank=True)
	comment = models.CharField(max_length=300, null=True, blank=True, verbose_name="Komentariu")
	status = models.CharField(max_length=50, null=True, blank=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.proc} - {0.number}'
		return template.format(self)

class ProcFiles(models.Model):
	proc = models.ForeignKey(Proc, on_delete=models.CASCADE, null=True, related_name="procfiles")
	desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="Dekrisaun Aneksu")
	file = models.FileField(upload_to=upload_procfiles, null=True, blank=False, verbose_name="Aneksu (.pdf)")
	is_lock = models.BooleanField(default=False, null=True, blank=True)
	datetime = models.DateTimeField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	hashed = models.CharField(max_length=32, null=True, blank=True)
	def __str__(self):
		template = '{0.proc}-{0.desc}'
		return template.format(self)
