from django.db.models import Sum
from custom.models import Sector
from contract.models import Contract, ContractYear, ContractComp, Amendment
from payment.models import Payment
from conf.utils import f_monthname_tet

def f_sec_all(obj, is_ann=True, is_fiscal=False):
	if is_ann==True:
		conts = Contract.objects.filter(project__sector=obj).all()
	else:
		conts = Contract.objects.filter(project__sector=obj, is_fiscal=is_fiscal).all()
	objects = []
	for cont in conts:
		proj = cont.project
		comp = ContractComp.objects.filter(contract=cont).all()
		amd = Amendment.objects.get(contract=cont)
		pay = Payment.objects.filter(contract=cont).last()
		objects.append([cont,amd.total,pay,proj,comp])
	return objects

def f_sec_year(obj, year, is_ann=True, is_fiscal=False):
	if is_ann==True:
		conts = ContractYear.objects.filter(contract__project__sector=obj, year=year).all()
	else:
		conts = ContractYear.objects.filter(contract__project__sector=obj, year=year, contract__is_fiscal=is_fiscal).all()
	objects = []
	for cont in conts:
		cont2 = cont.contract
		proj = cont2.project
		comp = ContractComp.objects.filter(contract=cont2).all()
		if cont2.is_fiscal == False: 
			amd = Amendment.objects.get(contract=cont2)
			pay = Payment.objects.filter(contract=cont2).last()
		else: 
			amd = cont
			pay = Payment.objects.filter(contract=cont2, date__year=year).last()
		objects.append([cont,amd.total,pay,proj,comp])
	return objects
###
def f_sec_sum(is_ann=True, is_fiscal=False):
	years = []
	if is_ann==True:
		years = Payment.objects.filter().distinct().values('date__year').order_by('-date__year').exclude(total=0)
	else:
		years = Payment.objects.filter(contract__is_fiscal=is_fiscal).distinct().values('date__year').order_by('-date__year').exclude(total=0)
	objects = []
	for i in years:
		if is_ann==True:
			tot_proj = Payment.objects.filter(date__year=i['date__year']).count()
			tot_cont = Payment.objects.filter(date__year=i['date__year']).exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
			tot_pay = Payment.objects.filter(date__year=i['date__year']).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		else:
			tot_proj = Payment.objects.filter(date__year=i['date__year'], contract__is_fiscal=is_fiscal).count()
			tot_cont = Payment.objects.filter(date__year=i['date__year'], contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
			tot_pay = Payment.objects.filter(date__year=i['date__year'], contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_bal = tot_cont-tot_pay
		obj_a = [tot_proj,tot_cont,tot_pay,tot_bal]
		#
		objs = Sector.objects.filter().all()
		obj_b = []
		for obj in objs:
			if is_ann==True:
				tot1 = Payment.objects.filter(date__year=i['date__year'], contract__project__sector=obj).count()
				tot2 = Payment.objects.filter(date__year=i['date__year'], contract__project__sector=obj).exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
				tot3 = Payment.objects.filter(date__year=i['date__year'], contract__project__sector=obj).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			else:
				tot1 = Payment.objects.filter(date__year=i['date__year'], contract__project__sector=obj, contract__is_fiscal=is_fiscal).count()
				tot2 = Payment.objects.filter(date__year=i['date__year'], contract__project__sector=obj, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
				tot3 = Payment.objects.filter(date__year=i['date__year'], contract__project__sector=obj, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			
			tot4 = 0.0
			if tot3: tot4 = tot2-tot3
			if tot2 == None: tot2 = 0.0
			if tot3 == None: tot3 = 0.0
			obj_b.append([obj,tot1,tot2,tot3,tot4])
		objects.append([i,obj_a,obj_b])
	return objects

def f_sec_sum_tot(objs, is_ann=True, is_fiscal=False):
	obj_b = []
	for j in objs:
		if is_ann==True:
			tot1 = Payment.objects.filter(contract__project__sector=j).count()
			tot2 = Payment.objects.filter(contract__project__sector=j).exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
			tot3 = Payment.objects.filter(contract__project__sector=j).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		else:
			tot1 = Payment.objects.filter(contract__project__sector=j, contract__is_fiscal=is_fiscal).count()
			tot2 = Payment.objects.filter(contract__project__sector=j, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
			tot3 = Payment.objects.filter(contract__project__sector=j, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot4 = 0.0
		if tot2 == None: tot2 = 0.0
		if tot3 == None: tot3 = 0.0
		if tot3: tot4 = tot2-tot3
		obj_b.append([tot1,tot2,tot3,tot4])
	return obj_b
# year
def f_sec_sum_y(year, is_ann=True, is_fiscal=False):
	months = []
	if is_ann==True:
		months = Payment.objects.filter(date__year=year).distinct().values('date__month').all().order_by('-date__month').exclude(total=0)
	else:
		months = Payment.objects.filter(date__year=year, contract__is_fiscal=is_fiscal).distinct().values('date__month').all().order_by('-date__month').exclude(total=0)
	objects = []
	for i in months:
		monthname = f_monthname_tet(int(i['date__month']))
		tot_cont,tot_pay = 0,0
		if is_ann==True:
			tot_proj = Payment.objects.filter(date__year=year, date__month=i['date__month']).distinct().values('contract').count()
			tot_cont2 = Payment.objects.filter(date__year=year, date__month=i['date__month']).distinct().values('contract').exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
			tot_pay2 = Payment.objects.filter(date__year=year, date__month=i['date__month']).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if tot_cont2: tot_cont = tot_cont2
			if tot_pay2: tot_pay = tot_pay2
		else:
			tot_proj = Payment.objects.filter(date__year=year, date__month=i['date__month'], contract__is_fiscal=is_fiscal).distinct().values('contract').count()
			tot_cont2 = Payment.objects.filter(date__year=year, date__month=i['date__month'], contract__is_fiscal=is_fiscal).distinct().values('contract').exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
			tot_pay2 = Payment.objects.filter(date__year=year, date__month=i['date__month'], contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if tot_cont2: tot_cont = tot_cont2
			if tot_pay2: tot_pay = tot_pay2
		tot_bal = tot_cont-tot_pay
		obj_a = [tot_proj,tot_cont,tot_pay,tot_bal]
		#
		objs = Sector.objects.filter().all()
		obj_b = []
		for obj in objs:
			if is_ann==True:
				tot1 = Payment.objects.filter(date__year=year, date__month=i['date__month'], contract__project__sector=obj).distinct().values('contract').count()
				tot2 = Payment.objects.filter(date__year=year, date__month=i['date__month'], contract__project__sector=obj).distinct().values('contract').exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
				tot3 = Payment.objects.filter(date__year=year, date__month=i['date__month'], contract__project__sector=obj).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			else:
				tot1 = Payment.objects.filter(date__year=year, date__month=i['date__month'], contract__project__sector=obj, contract__is_fiscal=is_fiscal).distinct().values('contract').count()
				tot2 = Payment.objects.filter(date__year=year, date__month=i['date__month'], contract__project__sector=obj, contract__is_fiscal=is_fiscal).distinct().values('contract').exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
				tot3 = Payment.objects.filter(date__year=year, date__month=i['date__month'], contract__project__sector=obj, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
				
			if tot2 == None: tot2 = 0.0
			if tot3 == None: tot3 = 0.0
			obj_b.append([obj,tot1,tot2,tot3])		
		m = [i['date__month'],monthname]
		objects.append([m,obj_a,obj_b])
	return objects

def f_sec_sum_tot_y(objs, year, is_ann=True, is_fiscal=False):
	tot_b = []
	for j in objs:
		tot_b_1,tot_b_2,tot_b_3 = 0,0,0
		if is_ann==True:
			tot_b_1a = Payment.objects.filter(date__year=year, contract__project__sector=j).distinct().values('contract').count()
			tot_b_2a = Payment.objects.filter(date__year=year, contract__project__sector=j).distinct().values('contract').exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
			tot_b_3a = Payment.objects.filter(date__year=year, contract__project__sector=j).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		else:
			tot_b_1a = Payment.objects.filter(date__year=year, contract__project__sector=j, contract__is_fiscal=is_fiscal).distinct().values('contract').count()
			tot_b_2a = Payment.objects.filter(date__year=year, contract__project__sector=j, contract__is_fiscal=is_fiscal).distinct().values('contract').exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
			tot_b_3a = Payment.objects.filter(date__year=year, contract__project__sector=j, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if tot_b_1a: tot_b_1 = tot_b_1a
		if tot_b_2a: tot_b_2 = tot_b_2a
		if tot_b_3a: tot_b_3 = tot_b_3a
		tot_b.append([tot_b_1,tot_b_2,tot_b_3])
	return tot_b
# month
def f_sec_sum_m(year, month, is_ann=True, is_fiscal=False):
	dates = []
	if is_ann==True:
		dates = Payment.objects.filter(date__year=year, date__month=month).distinct().values('date').order_by('date__month').all()
	else:
		dates = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=is_fiscal).distinct().values('date').order_by('date__month').all()
	objects = []
	for i in dates:
		if is_ann==True:
			tot_proj = Payment.objects.filter(date=i['date']).distinct().values('contract').count()
			tot_cont = Payment.objects.filter(date=i['date']).distinct().values('contract').exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
			tot_pay = Payment.objects.filter(date=i['date']).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		else:
			tot_proj = Payment.objects.filter(date=i['date'], contract__is_fiscal=is_fiscal).distinct().values('contract').count()
			tot_cont = Payment.objects.filter(date=i['date'], contract__is_fiscal=is_fiscal).distinct().values('contract').exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
			tot_pay = Payment.objects.filter(date=i['date'], contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		obj_a = [tot_proj,tot_cont,tot_pay]
		objs = Sector.objects.filter().all()
		obj_b = []
		for obj in objs:
			if is_ann==True:
				tot1 = Payment.objects.filter(date=i['date'], contract__project__sector=obj, contract__is_fiscal=False).distinct().values('contract').count()
				tot2 = Payment.objects.filter(date=i['date'], contract__project__sector=obj, contract__is_fiscal=False).distinct().values('contract').exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
				tot3 = Payment.objects.filter(date=i['date'], contract__project__sector=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			else:
				tot1 = Payment.objects.filter(date=i['date'], contract__project__sector=obj, contract__is_fiscal=False).distinct().values('contract').count()
				tot2 = Payment.objects.filter(date=i['date'], contract__project__sector=obj, contract__is_fiscal=False).distinct().values('contract').exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
				tot3 = Payment.objects.filter(date=i['date'], contract__project__sector=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if tot2 == None: tot2 = 0.0
			if tot3 == None: tot3 = 0.0
			obj_b.append([obj,tot1,tot2,tot3])
		objects.append([i['date'],obj_a,obj_b])
	return objects

def f_sec_sum_tot_m(objs, year, month, is_ann=True, is_fiscal=False):
	tot_b = []
	for j in objs:
		if is_ann==True:
			tot_b_1 = Payment.objects.filter(date__year=year, date__month=month, contract__project__sector=j).distinct().values('contract').count()
			tot_b_2 = Payment.objects.filter(date__year=year, date__month=month, contract__project__sector=j).distinct().values('contract').exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
			tot_b_3 = Payment.objects.filter(date__year=year, date__month=month, contract__project__sector=j).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		else:
			tot_b_1 = Payment.objects.filter(date__year=year, date__month=month, contract__project__sector=j, contract__is_fiscal=is_fiscal).distinct().values('contract').count()
			tot_b_2 = Payment.objects.filter(date__year=year, date__month=month, contract__project__sector=j, contract__is_fiscal=is_fiscal).distinct().values('contract').exclude(total=0).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
			tot_b_3 = Payment.objects.filter(date__year=year, date__month=month, contract__project__sector=j, contract__is_fiscal=is_fiscal).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_b.append([tot_b_1,tot_b_2,tot_b_3])
	return tot_b

def f_sec_sum_y_det(obj, year, is_ann=True, is_fiscal=False):
	if is_ann==True:
		pays = Payment.objects.filter(date__year=year, contract__project__sector=obj).all()
	else:
		pays = Payment.objects.filter(date__year=year, contract__project__sector=obj, contract__is_fiscal=is_fiscal).all()
	objects = []
	for pay in pays:
		cont = pay.contract
		proj = cont.project
		comp = ContractComp.objects.filter(contract=cont).all()
		amd = Amendment.objects.filter(contract=cont).first()
		pay = Payment.objects.filter(date__year=year, contract=cont).last()
		prog_pag = 0
		if pay:
			prog_pag = round(pay.com_amount*100/amd.total,2)
		objects.append([proj,cont,comp,pay,prog_pag,amd.total])
	return objects

def f_sec_sum_m_det(obj, year, month, is_ann=True, is_fiscal=False):
	if is_ann==True:
		objs = Payment.objects.filter(date__year=year, date__month=month, contract__project__sector=obj).exclude(total=0)\
			.distinct().values('contract').order_by('-date__month')
	else:
		objs = Payment.objects.filter(date__year=year, date__month=month, contract__project__sector=obj, contract__is_fiscal=is_fiscal).exclude(total=0)\
			.distinct().values('contract').order_by('-date__month')
	objects = []
	for i in objs:
		cont = Contract.objects.get(id=i['contract'])
		comp = ContractComp.objects.filter(contract=cont).all()
		proj = cont.project
		amd = Amendment.objects.filter(contract=cont).first()
		pay = Payment.objects.filter(date__year=year, contract=cont).last()
		prog_pag = 0
		if pay:
			prog_pag = round(pay.com_amount*100/amd.total,2)
		objects.append([proj,cont,comp,pay,prog_pag,amd.total])
	return objects