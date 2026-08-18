from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from contract.models import ContractYear
from payment.models import Payment
from custom.models import Division, PCategory, Capital, Sector
from reportdiv.utils_pay import f_pay_cat, f_pay_sec, f_pay_cap
from users.decorators import allowed_users
from sigp.utils import get_roles

@login_required
def rdivPayFisDash(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	tot_cont = ContractYear.objects.filter(contract__project__owner=div, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_paid = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_bal = 0
	if tot_paid: tot_bal = tot_cont-tot_paid
	# 
	tot_cats = f_pay_cat(div, PCategory, None, True)
	tot_secs = f_pay_sec(div, Sector, None, True)
	tot_caps = f_pay_cap(div, Capital, None, True)
	years = ContractYear.objects.distinct().values('year').all().order_by('-year')
	context = {
		'group': group, 'div':div, 'tot_cont': tot_cont, 'tot_paid': tot_paid, 'tot_bal': tot_bal, 'years': years,
		'tot_cats': tot_cats, 'tot_secs': tot_secs, 'tot_caps': tot_caps, 'page': 'pdash',
		'subtitle': 'Projetu Foun no Reaproriasaun',
		'title': 'Sumariu Kontratu & Pagamentu Fiskal', 'legend': 'Sumariu Kontratu & Pagamentu Fiskal'
	}
	return render(request, 'reportdiv_pay_fis/pay_dash.html', context)

@login_required
def rdivPayFisYear(request, pk, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	check = ContractYear.objects.filter(contract__project__owner=div, contract__is_fiscal=True, year=year).all()
	tot_cont, tot_paid, tot_bal, tot_cats, tot_secs, tot_caps = [],[],0,[],[],[]
	if check:
		tot_cont = ContractYear.objects.filter(contract__project__owner=div, contract__is_fiscal=True, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=True, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if tot_paid: tot_bal = tot_cont-tot_paid
		# 
		tot_cats = f_pay_cat(div, PCategory, year, True)
		tot_secs = f_pay_sec(div, Sector, year, True)
		tot_caps = f_pay_cap(div, Capital, year, True)
	years = ContractYear.objects.distinct().values('year').all().order_by('-year')
	context = {
		'group': group, 'div':div, 'tot_cont': tot_cont, 'tot_paid': tot_paid, 'tot_bal': tot_bal, 'years': years,
		'tot_cats': tot_cats, 'tot_secs': tot_secs, 'tot_caps': tot_caps, 'year': year, 'page': 'pyear',
		'subtitle': 'Projetu Foun no Reaproriasaun',
		'title': f'Sumariu Pagamentu ba Kontratu Tinan {year}', 'legend': f'Sumariu Pagamentu ba Kontratu Tinan {year}'
	}
	return render(request, 'reportdiv_pay_fis/pay_dash_year.html', context)
### CAT
from conf.utils import f_monthname_tet
from reportdiv.utils_pay_cat import f_cat_all, f_cat_year, f_cat_sum, f_cat_sum_tot, f_cat_sum_y, f_cat_sum_tot_y,\
	f_cat_sum_m, f_cat_sum_tot_m, f_cat_sum_y_det, f_cat_sum_m_det

@login_required
def rdivPayFisCatAll(request, pk, pk2, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(PCategory, pk=pk2)
	objects = f_cat_all(div, obj, is_ann=False, is_fiscal=True)
	subtitle = f'Kategoria {obj.name} ({obj.code})'
	context = {
		'group': group, 'div':div, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Fiskal', 'legend': f'Lista Pagamentu Fiskal'
	}
	return render(request, 'reportdiv_pay_fis/pay_all_list.html', context)

@login_required
def rdivPayFisCatYear(request, pk, year, pk2, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(PCategory, pk=pk2)
	objects = f_cat_year(div, obj, year, is_ann=False, is_fiscal=True)
	subtitle = f'Kategoria {obj.name} ({obj.code})'
	context = {
		'group': group, 'div':div, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Fiskal Tinan {year}', 'legend': f'Lista Pagamentu Fiskal Tinan {year}'
	}
	return render(request, 'reportdiv_pay_fis/pay_all_list.html', context)
#
@login_required
def rdivPayFisCatSum(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = f_cat_sum(div, is_ann=False, is_fiscal=True)	
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=True).count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=True).exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=True).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = PCategory.objects.filter().all()
	obj_b = f_cat_sum_tot(div, objs, is_ann=False, is_fiscal=True)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Katagoria"
	context = {
		'group': group, 'div':div, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'pcat',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Fiskal Kada Tinan', 'legend': 'Sumariu Pagamentu Fiskal Kada Tinan'
	}
	return render(request, 'reportdiv_pay_fis/pay_cat_sum.html', context)

@login_required
def rdivPayFisCatSumYear(request, pk, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = f_cat_sum_y(div, year, is_ann=False, is_fiscal=True)
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, date__year=year, contract__is_fiscal=True).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, date__year=year, contract__is_fiscal=True).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, date__year=year, contract__is_fiscal=True).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = PCategory.objects.filter().all()
	tot_b = f_cat_sum_tot_y(div, objs, year, is_ann=False, is_fiscal=True)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'div':div, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'fis', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Fiskal Tuir Kategoria', 'legend': f'Sumariu Pagamentu Fiskal Tuir Kategoria'
	}
	return render(request, 'reportdiv_pay_fis/pay_cat_year.html', context)

@login_required
def rdivPayFisCatSumMonth(request, pk, year, month):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	div = get_object_or_404(Division, pk=pk)
	objects = f_cat_sum_m(div, year, month, is_ann=False, is_fiscal=True)
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month, contract__is_fiscal=True).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month, contract__is_fiscal=True).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month, contract__is_fiscal=True).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = PCategory.objects.filter().all()
	tot_b = f_cat_sum_tot_m(div, objs, year, month, is_ann=False, is_fiscal=True)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'div':div, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'fis',
		'title': f'Sumariu Pagamentu Fiskal Tuir Kategoria', 'legend': f'Sumariu Pagamentu Fiskal Tuir Kategoria'
	}
	return render(request, 'reportdiv_pay_g/pay_cat_month.html', context)
###
@login_required
def rdivPayFisCatSumYearDet(request, pk, year, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(PCategory, pk=pk2)
	objects = f_cat_sum_y_det(div, obj, year, is_ann=False, is_fiscal=True)
	subtitle = f"{obj.name} ({obj.code}) Tinan {year}"
	context = {
		'group': group, 'div':div, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'fis',
		'title': f'Lista Pagamentu Fiskal Tuir Kategoria', 'legend': f'Lista Pagamentu Fiskal Tuir Kategoria'
	}
	return render(request, 'reportdiv_pay_g/pay_cat_det.html', context)

@login_required
def rdivPayFisCatSumMonthDet(request, pk, year, month, pk2):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(PCategory, pk=pk2)
	objects = f_cat_sum_m_det(div, obj, year, month, is_ann=False, is_fiscal=True)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'div':div, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'fis', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Fiskal Tuir Kategoria', 'legend': f'Lista Pagamentu Fiskal Tuir Kategoria'
	}
	return render(request, 'reportdiv_pay_g/pay_cat_det.html', context)