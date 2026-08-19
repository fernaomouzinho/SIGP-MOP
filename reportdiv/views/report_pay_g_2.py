from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from custom.models import Division, Sector, Capital
from payment.models import Payment
from conf.utils import f_monthname_tet
from reportdiv.utils_pay_sec import f_sec_all, f_sec_year, f_sec_sum, f_sec_sum_tot, f_sec_sum_y, f_sec_sum_tot_y,\
	f_sec_sum_m, f_sec_sum_tot_m, f_sec_sum_y_det, f_sec_sum_m_det
from users.decorators import allowed_users
from sigp.utils import get_roles

### SECTOR

def rdivPayGSecAll(request, pk, pk2, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Sector, pk=pk2)
	objects = f_sec_all(div, obj, is_ann=False, is_fiscal=False)
	subtitle = f'Setor {obj.name}'
	context = {
		'group': group, 'div':div, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu', 'legend': f'Lista Pagamentu'
	}
	return render(request, 'reportdiv_pay_g/pay_all_list.html', context)


def rdivPayGSecYear(request, pk, year, pk2, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Sector, pk=pk2)
	objects = f_sec_year(div, obj, year, is_ann=False, is_fiscal=False)
	subtitle = f'Setor {obj.name}'
	context = {
		'group': group, 'div':div, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Tinan {year}', 'legend': f'Lista Pagamentu Tinan {year}'
	}
	return render(request, 'reportdiv_pay_g/pay_all_list.html', context)
#

def rdivPayGSecSum(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = f_sec_sum(div, is_ann=False, is_fiscal=False)	
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=False).count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = Sector.objects.filter().all()
	obj_b = f_sec_sum_tot(div, objs, is_ann=False, is_fiscal=False)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Setor"
	context = {
		'group': group, 'div':div, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'psec',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Kada Tinan', 'legend': 'Sumariu Pagamentu Kada Tinan'
	}
	return render(request, 'reportdiv_pay_g/pay_sec_sum.html', context)


def rdivPayGSecSumYear(request, pk,  year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = f_sec_sum_y(div, year, is_ann=False, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, date__year=year, contract__is_fiscal=False).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, date__year=year, contract__is_fiscal=False).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, date__year=year, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Sector.objects.filter().all()
	tot_b = f_sec_sum_tot_y(div, objs, year, is_ann=False, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'div':div, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'g', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Tuir Setor', 'legend': f'Sumariu Pagamentu Tuie Setor'
	}
	return render(request, 'reportdiv_pay_g/pay_sec_year.html', context)


def rdivPayGSecSumMonth(request, pk, year, month):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	monthname = f_monthname_tet(int(month))
	objects = f_sec_sum_m(div, year, month, is_ann=False, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month, contract__is_fiscal=False).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month, contract__is_fiscal=False).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Sector.objects.filter().all()
	tot_b = f_sec_sum_tot_m(div, objs, year, month, is_ann=False, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'div':div, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'g',
		'title': f'Sumariu Pagamentu Tuir Setor', 'legend': f'Sumariu Pagamentu Tuir Setor'
	}
	return render(request, 'reportdiv_pay_g/pay_sec_month.html', context)
#

def rdivPayGSecSumYearDet(request, pk, year, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Sector, pk=pk2)
	objects = f_sec_sum_y_det(div, obj, year, is_ann=False, is_fiscal=False)
	subtitle = f"{obj.name} Tinan {year}"
	context = {
		'group': group, 'div':div, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'g',
		'title': f'Lista Pagamentu Tuir Setor', 'legend': f'Lista Pagamentu Tuir Setor'
	}
	return render(request, 'reportdiv_pay_g/pay_sec_det.html', context)


def rdivPayGSecSumMonthDet(request, pk, year, month, pk2):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Sector, pk=pk2)
	objects = f_sec_sum_m_det(div, obj, year, month, is_ann=False, is_fiscal=False)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'div':div, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'g', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Setor', 'legend': f'Lista Pagamentu Setor'
	}
	return render(request, 'reportdiv_pay_g/pay_sec_det.html', context)
### CAPITAL
from reportdiv.utils_pay_cap import f_cap_all, f_cap_year, f_cap_sum, f_cap_sum_tot, f_cap_sum_y, f_cap_sum_tot_y,\
	f_cap_sum_m, f_cap_sum_tot_m, f_cap_sum_y_det, f_cap_sum_m_det


def rdivPayGCapAll(request, pk, pk2, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Capital, pk=pk2)
	objects = f_cap_all(div, obj, is_ann=False, is_fiscal=False)
	subtitle = f'Capital {obj.name} ({obj.code})'
	context = {
		'group': group, 'div':div, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu', 'legend': f'Lista Pagamentu'
	}
	return render(request, 'reportdiv_pay_g/pay_all_list.html', context)


def rdivPayGCapYear(request, pk, year, pk2, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Capital, pk=pk2)
	objects = f_cap_year(div, obj, year, is_ann=False, is_fiscal=False)
	subtitle = f'Capital {obj.name} ({obj.code})'
	context = {
		'group': group, 'div':div, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Tinan {year}', 'legend': f'Lista Pagamentu Tinan {year}'
	}
	return render(request, 'reportdiv_pay_g/pay_all_list.html', context)
#

def rdivPayGCapSum(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = f_cap_sum(div, is_ann=False, is_fiscal=False)	
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=False).count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = Capital.objects.filter().all()
	obj_b = f_cap_sum_tot(div, objs, is_ann=False, is_fiscal=False)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Capital"
	context = {
		'group': group, 'div':div, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'pcat',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Kada Tinan', 'legend': 'Sumariu Pagamentu Kada Tinan'
	}
	return render(request, 'reportdiv_pay_g/pay_cap_sum.html', context)


def rdivPayGCapSumYear(request, pk, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = f_cap_sum_y(div, year, is_ann=False, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, date__year=year, contract__is_fiscal=False).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, date__year=year, contract__is_fiscal=False).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, date__year=year, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Capital.objects.filter().all()
	tot_b = f_cap_sum_tot_y(div, objs, year, is_ann=False, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'div':div, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'g', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Tuir Capital', 'legend': f'Sumariu Pagamentu Tuie Capital'
	}
	return render(request, 'reportdiv_pay_g/pay_cap_year.html', context)


def rdivPayGCapSumMonth(request, pk, year, month):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	monthname = f_monthname_tet(int(month))
	objects = f_cap_sum_m(div, year, month, is_ann=False, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month, contract__is_fiscal=False).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month, contract__is_fiscal=False).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Capital.objects.filter().all()
	tot_b = f_cap_sum_tot_m(div, objs, year, month, is_ann=False, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'div':div, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'g',
		'title': f'Sumariu Pagamentu Tuir Capital', 'legend': f'Sumariu Pagamentu Tuir Capital'
	}
	return render(request, 'reportdiv_pay_g/pay_cap_month.html', context)
#

def rdivPayGCapSumYearDet(request, pk, year, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Capital, pk=pk2)
	objects = f_cap_sum_y_det(div, obj, year, is_ann=False, is_fiscal=False)
	subtitle = f"{obj.name} ({obj.code}) Tinan {year}"
	context = {
		'group': group, 'div':div, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'g',
		'title': f'Lista Pagamentu Tuir Capital', 'legend': f'Lista Pagamentu Tuir Capital'
	}
	return render(request, 'reportdiv_pay_g/pay_cap_det.html', context)


def rdivPayGCapSumMonthDet(request, pk, year, month, pk2):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Capital, pk=pk2)
	objects = f_cap_sum_m_det(div, obj, year, month, is_ann=False, is_fiscal=False)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'div':div, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'g', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Capital', 'legend': f'Lista Pagamentu Capital'
	}
	return render(request, 'reportdiv_pay_g/pay_cap_det.html', context)