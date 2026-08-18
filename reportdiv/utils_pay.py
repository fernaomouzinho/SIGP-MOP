from django.db.models import Sum, Count, Q
from contract.models import ContractYear
from payment.models import Payment

def f_pay_cat(div, table, year, is_fiscal=False):
	objs = table.objects.all()
	tot_objs = []
	for obj in objs:
		obja, objb = 0,0
		if year == None:
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		else:
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, year=year, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, contyear__year=year, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if obj_a: obja = obj_a
		if obj_b: objb = obj_b
		objc = obja-objb
		tot_objs.append([obj,obja,objb,objc])
	return tot_objs

def f_pay_sec(div, table, year, is_fiscal=False):
	objs = table.objects.all()
	tot_objs = []
	for obj in objs:
		obja, objb = 0,0
		if year == None:
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__sector=obj, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__sector=obj, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		else:
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__sector=obj, year=year, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__sector=obj, contyear__year=year, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if obj_a: obja = obj_a
		if obj_b: objb = obj_b
		objc = obja-objb
		tot_objs.append([obj,obja,objb,objc])
	return tot_objs

def f_pay_cap(div, table, year, is_fiscal=False):
	objs = table.objects.all()
	tot_objs = []
	for obj in objs:
		obja, objb = 0,0
		if year == None:
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__capital=obj, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__capital=obj, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		else:
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__capital=obj, year=year, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__capital=obj, contyear__year=year, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if obj_a: obja = obj_a
		if obj_b: objb = obj_b
		objc = obja-objb
		tot_objs.append([obj,obja,objb,objc])
	return tot_objs
###
def f_pay_ann_cat(div, table, year):
	objs = table.objects.all()
	tot_objs = []
	for obj in objs:
		obja, objb = 0,0
		obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, date__year=year, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if obj_a: obja = obj_a
		if obj_b: objb = obj_b
		objc = obja-objb
		tot_objs.append([obj,obja,objb,objc])
	return tot_objs

def f_pay_ann_sec(div, table, year):
	objs = table.objects.all()
	tot_objs = []
	for obj in objs:
		obja, objb = 0,0
		obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__sector=obj, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__sector=obj, date__year=year, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if obj_a: obja = obj_a
		if obj_b: objb = obj_b
		objc = obja-objb
		tot_objs.append([obj,obja,objb,objc])
	return tot_objs

def f_pay_ann_cap(div, table, year):
	objs = table.objects.all()
	tot_objs = []
	for obj in objs:
		obja, objb = 0,0
		obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__capital=obj, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__capital=obj, date__year=year, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if obj_a: obja = obj_a
		if obj_b: objb = obj_b
		objc = obja-objb
		tot_objs.append([obj,obja,objb,objc])
	return tot_objs