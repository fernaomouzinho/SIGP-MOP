import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from contract.models import ContractYear
from payment.models import Payment
from custom.models import Division, PCategory, Capital, Sector
from reportdiv.utils_pay import f_pay_ann_cat, f_pay_ann_sec, f_pay_ann_cap
from users.decorators import allowed_users
from sigp.utils import get_roles

@login_required
def rdivPayAnnDash(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	this_year = datetime.date.today().year
	tot_cont = ContractYear.objects.filter(contract__project__owner=div, year=this_year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_paid = Payment.objects.filter(contract__project__owner=div, date__year=this_year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_bal = 0
	if tot_paid: tot_bal = tot_cont-tot_paid
	# 
	tot_cats = f_pay_ann_cat(div, PCategory, this_year)
	tot_secs = f_pay_ann_sec(div, Sector, this_year)
	tot_caps = f_pay_ann_cap(div, Capital, this_year)
	years = ContractYear.objects.distinct().values('year').all().order_by('-year')
	context = {
		'group': group, 'div':div, 'year': this_year, 'tot_cont': tot_cont, 'tot_paid': tot_paid, 'tot_bal': tot_bal, 'years': years,
		'tot_cats': tot_cats, 'tot_secs': tot_secs, 'tot_caps': tot_caps, 'page': 'pdash',
		'subtitle': f'Projetu Foun Tinan {this_year}',
		'title': 'Sumariu Kontratu & Pagamentu Annual', 'legend': 'Sumariu Kontratu & Pagamentu Annual'
	}
	return render(request, 'reportdiv_pay_ann/pay_dash.html', context)

@login_required
def rdivPayAnnYear(request, pk, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	check = ContractYear.objects.filter(contract__project__owner=div, year=year).all()
	tot_cont, tot_paid, tot_bal, tot_cats, tot_secs, tot_caps = [],[],0,[],[],[]
	if check:
		tot_cont = ContractYear.objects.filter(contract__project__owner=div, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contract__project__owner=div, contyear__year=year, date__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if tot_paid: tot_bal = tot_cont-tot_paid
		# 
		tot_cats = f_pay_ann_cat(div, PCategory, year)
		tot_secs = f_pay_ann_sec(div, Sector, year)
		tot_caps = f_pay_ann_cap(div, Capital, year)
		
	years = ContractYear.objects.distinct().values('year').all().order_by('-year')
	context = {
		'group': group, 'div':div, 'tot_cont': tot_cont, 'tot_paid': tot_paid, 'tot_bal': tot_bal, 'years': years,
		'tot_cats': tot_cats, 'tot_secs': tot_secs, 'tot_caps': tot_caps, 'year': year, 'page': 'pyear',
		'subtitle': f'Projetu Foun Tinan {year}',
		'title': 'Sumariu Kontratu & Pagamentu Annual', 'legend': 'Sumariu Kontratu & Pagamentu Annual'
	}
	return render(request, 'reportdiv_pay_ann/pay_dash.html', context)
### CAT
from conf.utils import f_monthname_tet
from reportdiv.utils_pay_cat import f_cat_all, f_cat_year, f_cat_sum, f_cat_sum_tot, f_cat_sum_y, f_cat_sum_tot_y,\
	f_cat_sum_m, f_cat_sum_tot_m, f_cat_sum_y_det, f_cat_sum_m_det

@login_required
def rdivPayAnnCatAll(request, pk, pk2, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(PCategory, pk=pk2)
	objects = f_cat_all(div, obj, is_ann=True, is_fiscal=False)
	subtitle = f'Kategoria {obj.name} ({obj.code})'
	context = {
		'group': group, 'div':div, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Annual', 'legend': f'Lista Pagamentu Annual'
	}
	return render(request, 'reportdiv_pay_ann/pay_all_list.html', context)

@login_required
def rdivPayAnnCatYear(request, pk, year, pk2, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(PCategory, pk=pk2)
	objects = f_cat_year(div, obj, year, is_ann=True, is_fiscal=False)
	subtitle = f'Kategoria {obj.name} ({obj.code})'
	context = {
		'group': group, 'div':div, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Annual Tinan {year}', 'legend': f'Lista Pagamentu Annual Tinan {year}'
	}
	return render(request, 'reportdiv_pay_ann/pay_all_list.html', context)
#
@login_required
def rdivPayAnnCatSum(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = f_cat_sum(div, is_ann=True, is_fiscal=False)	
	tot_a_1 = Payment.objects.filter(contract__project__owner=div).count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div).exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = PCategory.objects.filter().all()
	obj_b = f_cat_sum_tot(div, objs, is_ann=True, is_fiscal=False)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Katagoria"
	context = {
		'group': group, 'div':div, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'pcat',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Annual Kada Tinan', 'legend': 'Sumariu Pagamentu Annual Kada Tinan'
	}
	return render(request, 'reportdiv_pay_ann/pay_cat_sum.html', context)

@login_required
def rdivPayAnnCatSumYear(request, pk, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = f_cat_sum_y(div, year, is_ann=True, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, date__year=year).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, date__year=year).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, date__year=year).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = PCategory.objects.filter().all()
	tot_b = f_cat_sum_tot_y(div, objs, year, is_ann=True, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'div':div, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'ann', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Annual Tuir Kategoria', 'legend': f'Sumariu Pagamentu Annual Tuir Kategoria'
	}
	return render(request, 'reportdiv_pay_ann/pay_cat_year.html', context)

@login_required
def rdivPayAnnCatSumMonth(request, pk, year, month):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	div = get_object_or_404(Division, pk=pk)
	objects = f_cat_sum_m(div, year, month, is_ann=True, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = PCategory.objects.filter().all()
	tot_b = f_cat_sum_tot_m(div, objs, year, month, is_ann=True, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'div':div, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'ann',
		'title': f'Sumariu Pagamentu Annual Tuir Kategoria', 'legend': f'Sumariu Pagamentu Annual Tuir Kategoria'
	}
	return render(request, 'reportdiv_pay_g/pay_cat_month.html', context)
#
@login_required
def rdivPayAnnCatSumYearDet(request, pk, year, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(PCategory, pk=pk2)
	objects = f_cat_sum_y_det(div, obj, year, is_ann=True, is_fiscal=False)
	subtitle = f"{obj.name} ({obj.code}) Tinan {year}"
	context = {
		'group': group, 'div':div, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'ann',
		'title': f'Lista Pagamentu Annual Tuir Kategoria', 'legend': f'Lista Pagamentu Annual Tuir Kategoria'
	}
	return render(request, 'reportdiv_pay_g/pay_cat_det.html', context)

@login_required
def rdivPayAnnCatSumMonthDet(request, pk, year, month, pk2):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(PCategory, pk=pk2)
	objects = f_cat_sum_m_det(div, obj, year, month, is_ann=True, is_fiscal=False)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'div':div, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'ann', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Annual Kategoria', 'legend': f'Lista Pagamentu Annual Kategoria'
	}
	return render(request, 'reportdiv_pay_g/pay_cat_det.html', context)