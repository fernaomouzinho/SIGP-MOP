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
@login_required
def rdivPayAnnSecAll(request, pk, pk2, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Sector, pk=pk2)
	objects = f_sec_all(div, obj, is_ann=True, is_fiscal=False)
	subtitle = f'Setor {obj.name}'
	context = {
		'group': group, 'div':div, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Annual', 'legend': f'Lista Pagamentu Annual'
	}
	return render(request, 'reportdiv_pay_ann/pay_all_list.html', context)

@login_required
def rdivPayAnnSecYear(request, pk, year, pk2, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Sector, pk=pk2)
	objects = f_sec_year(div, obj, year, is_ann=True, is_fiscal=False)
	subtitle = f'Setor {obj.name}'
	context = {
		'group': group, 'div':div, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Annual Tinan {year}', 'legend': f'Lista Pagamentu Annual Tinan {year}'
	}
	return render(request, 'reportdiv_pay_ann/pay_all_list.html', context)
#
@login_required
def rdivPayAnnSecSum(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = f_sec_sum(div, is_ann=True, is_fiscal=False)	
	tot_a_1 = Payment.objects.filter(contract__project__owner=div).count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div).exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = Sector.objects.filter().all()
	obj_b = f_sec_sum_tot(div, objs, is_ann=True, is_fiscal=False)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Setor"
	context = {
		'group': group, 'div':div, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'psec',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Annual Kada Tinan', 'legend': 'Sumariu Pagamentu Annual Kada Tinan'
	}
	return render(request, 'reportdiv_pay_ann/pay_sec_sum.html', context)

@login_required
def rdivPayAnnSecSumYear(request, pk, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = f_sec_sum_y(div, year, is_ann=True, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, date__year=year).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, date__year=year).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, date__year=year).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Sector.objects.filter().all()
	tot_b = f_sec_sum_tot_y(div, objs, year, is_ann=True, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'div':div, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'ann', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Annual Tuir Setor', 'legend': f'Sumariu Pagamentu Annual Tuir Setor'
	}
	return render(request, 'reportdiv_pay_ann/pay_sec_year.html', context)

@login_required
def rdivPayAnnSecSumMonth(request, pk, year, month):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	div = get_object_or_404(Division, pk=pk)
	objects = f_sec_sum_m(year, month, is_ann=True, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Sector.objects.filter().all()
	tot_b = f_sec_sum_tot_m(div, objs, year, month, is_ann=True, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'div':div, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'ann',
		'title': f'Sumariu Pagamentu Annual Tuir Setor', 'legend': f'Sumariu Pagamentu Annual Tuir Setor'
	}
	return render(request, 'reportdiv_pay_g/pay_sec_month.html', context)
#
@login_required
def rdivPayAnnSecSumYearDet(request, pk, year, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Sector, pk=pk2)
	objects = f_sec_sum_y_det(div, obj, year, is_ann=True, is_fiscal=False)
	subtitle = f"{obj.name} Tinan {year}"
	context = {
		'group': group, 'div':div, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'ann',
		'title': f'Lista Pagamentu Annual Tuir Setor', 'legend': f'Lista Pagamentu Annual Tuir Setor'
	}
	return render(request, 'reportdiv_pay_g/pay_sec_det.html', context)

@login_required
def rdivPayAnnSecSumMonthDet(request, pk, year, month, pk2):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Sector, pk=pk2)
	objects = f_sec_sum_m_det(div, obj, year, month, is_ann=True, is_fiscal=False)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'div':div, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'ann', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Annual Setor', 'legend': f'Lista Pagamentu Annual Setor'
	}
	return render(request, 'reportdiv_pay_g/pay_sec_det.html', context)
### CAPITAL
from reportdiv.utils_pay_cap import f_cap_all, f_cap_year, f_cap_sum, f_cap_sum_tot, f_cap_sum_y, f_cap_sum_tot_y,\
	f_cap_sum_m, f_cap_sum_tot_m, f_cap_sum_y_det, f_cap_sum_m_det

@login_required
def rdivPayAnnCapAll(request, pk, pk2, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Capital, pk=pk2)
	objects = f_cap_all(div, obj, is_ann=True, is_fiscal=False)
	subtitle = f'Capital {obj.name} ({obj.code})'
	context = {
		'group': group, 'div':div, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Annual', 'legend': f'Lista Pagamentu Annual'
	}
	return render(request, 'reportdiv_pay_ann/pay_all_list.html', context)

@login_required
def rdivPayAnnCapYear(request, pk, year, pk2, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Capital, pk=pk2)
	objects = f_cap_year(div, obj, year, is_ann=True, is_fiscal=False)
	subtitle = f'Capital {obj.name} ({obj.code})'
	context = {
		'group': group, 'div':div, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Annual Tinan {year}', 'legend': f'Lista Pagamentu Annual Tinan {year}'
	}
	return render(request, 'reportdiv_pay_ann/pay_all_list.html', context)
#
@login_required
def rdivPayAnnCapSum(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = f_cap_sum(div, is_ann=True, is_fiscal=False)	
	tot_a_1 = Payment.objects.filter(contract__project__owner=div).count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div).exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = Capital.objects.filter().all()
	obj_b = f_cap_sum_tot(div, objs, is_ann=True, is_fiscal=False)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Capital"
	context = {
		'group': group, 'div':div, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'pcap',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Annual Kada Tinan', 'legend': 'Sumariu Pagamentu Annual Kada Tinan'
	}
	return render(request, 'reportdiv_pay_ann/pay_cap_sum.html', context)

@login_required
def rdivPayAnnCapSumYear(request, pk, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = f_cap_sum_y(div, year, is_ann=True, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, date__year=year).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, date__year=year).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, date__year=year).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Capital.objects.filter().all()
	tot_b = f_cap_sum_tot_y(div, objs, year, is_ann=True, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'div':div, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'ann', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Annual Tuir Capital', 'legend': f'Sumariu Pagamentu Annual Tuir Capital'
	}
	return render(request, 'reportdiv_pay_ann/pay_cap_year.html', context)

@login_required
def rdivPayAnnCapSumMonth(request, pk, year, month):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	div = get_object_or_404(Division, pk=pk)
	objects = f_cap_sum_m(div, year, month, is_ann=True, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Capital.objects.filter().all()
	tot_b = f_cap_sum_tot_m(div, objs, year, month, is_ann=True, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'div':div, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'ann',
		'title': f'Sumariu Pagamentu Annual Tuir Capital', 'legend': f'Sumariu Pagamentu Annual Tuir Capital'
	}
	return render(request, 'reportdiv_pay_g/pay_cap_month.html', context)
#
@login_required
def rdivPayAnnCapSumYearDet(request, pk, year, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Capital, pk=pk2)
	objects = f_cap_sum_y_det(div, obj, year, is_ann=True, is_fiscal=False)
	subtitle = f"{obj.name} ({obj.code}) Tinan {year}"
	context = {
		'group': group, 'div':div, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'ann',
		'title': f'Lista Pagamentu Annual Tuir Capital', 'legend': f'Lista Pagamentu Annual Tuir Capital'
	}
	return render(request, 'reportdiv_pay_g/pay_cap_det.html', context)

@login_required
def rdivPayAnnCapSumMonthDet(request, pk, year, month, pk2):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	div = get_object_or_404(Division, pk=pk)
	obj = get_object_or_404(Capital, pk=pk2)
	objects = f_cap_sum_m_det(div, obj, year, month, is_ann=True, is_fiscal=False)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'div':div, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'ann', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Annual Capital', 'legend': f'Lista Pagamentu Annual Capital'
	}
	return render(request, 'reportdiv_pay_g/pay_cap_det.html', context)