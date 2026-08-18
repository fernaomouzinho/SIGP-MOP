from employee.models import Employee
from custom.models import Min
from company.models import Company

def c_user_div(user):
	objects = Employee.objects.filter(employeeuser__user=user)\
		.prefetch_related('employeeuser','employeediv','employeepos').first()
	obj = ""
	if objects:
		obj = objects.employeediv.div
	return obj

def c_user_dna(user):
	objects = Employee.objects.filter(employeeuser__user=user)\
		.prefetch_related('employeeuser','employeediv','employeepos').first()
	obj = ""
	if objects:
		obj = objects.employeediv.div
	return obj

def c_user_dnof(user):
	objects = Employee.objects.filter(employeeuser__user=user)\
		.prefetch_related('employeeuser','employeediv','employeepos').first()
	obj = ""
	if objects:
		obj = objects.employeediv.div
	return obj

def c_user_dgaf(user):
	objects = Employee.objects.filter(employeeuser__user=user)\
		.prefetch_related('employeeuser','employeediv','employeepos').first()
	obj = ""
	if objects:
		obj = objects.employeediv.dg
	return obj

def c_user_dg(user):
	objects = Employee.objects.filter(employeeuser__user=user)\
		.prefetch_related('employeeuser','employeediv','employeepos').first()
	obj = ""
	if objects:
		obj = objects.employeediv.dg
	return obj

def c_user_min(user):
	obj = Min.objects.filter(id=1).first()
	return obj

def c_user_vice(user):
	obj = Min.objects.filter(id=2).first()
	return obj

def c_user_dep(user):
	objects = Employee.objects.filter(employeeuser__user=user)\
		.prefetch_related('employeeuser','employeediv','employeepos').first()
	obj = ""
	if objects:
		obj = objects.employeediv.dep
	return obj

def c_user_sec(user):
	objects = Employee.objects.filter(employeeuser__user=user)\
		.prefetch_related('employeeuser','employeediv','employeepos').first()
	obj = ""
	if objects:
		obj = objects.employeediv.sec
	return obj

def c_user_eng(user):
	obj = Employee.objects.filter(employeeuser__user=user).prefetch_related('employeeuser').first()
	return obj

def c_user_sup(user):
	objects = Employee.objects.filter(employeeuser__user=user)\
		.prefetch_related('employeeuser','employeediv','employeepos').first()
	obj = ""
	if objects:
		obj = objects.employeediv.mun
	return obj

def c_user_pos(user):
	objects = Employee.objects.filter(employeeuser__user=user)\
		.prefetch_related('employeeuser','employeepos').first()
	obj = ""
	if objects:
		obj = objects.employeepos.cat
	return obj


def c_user_uvip(user):
	objects = Employee.objects.filter(employeeuser__user=user)\
		.prefetch_related('employeeuser','employeepos').first()
	obj = ""
	if objects:
		obj = objects.employeepos
	return obj

def c_user_comp(user):
	objects = Company.objects.filter(compuser__user=user).prefetch_related('compuser').first()
	obj = ""
	if objects:
		obj = objects.compuser.comp
	return obj
