from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles
from django.db.models import Sum
from custom.models import Sector, Capital
from payment.models import Payment
from conf.utils import f_monthname_tet
from report.utils_pay_sec import f_sec_all, f_sec_year, f_sec_sum, f_sec_sum_tot, f_sec_sum_y, f_sec_sum_tot_y,\
	f_sec_sum_m, f_sec_sum_tot_m, f_sec_sum_y_det, f_sec_sum_m_det

### SECTOR

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGSecAll(request, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(Sector, pk=pk)
	objects = f_sec_all(obj, is_ann=False, is_fiscal=False)
	subtitle = f'Setor {obj.name}'
	context = {
		'group': group, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu', 'legend': f'Lista Pagamentu'
	}
	return render(request, 'report_pay_g/pay_all_list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGSecYear(request, year, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(Sector, pk=pk)
	objects = f_sec_year(obj, year, is_ann=False, is_fiscal=False)
	subtitle = f'Setor {obj.name}'
	context = {
		'group': group, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Tinan {year}', 'legend': f'Lista Pagamentu Tinan {year}'
	}
	return render(request, 'report_pay_g/pay_all_list.html', context)
#
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGSecSum(request):
	group = get_roles(request)
	objects = f_sec_sum(is_ann=False, is_fiscal=False)	
	tot_a_1 = Payment.objects.filter(contract__is_fiscal=False).count()
	tot_a_2 = Payment.objects.filter(contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = Sector.objects.filter().all()
	obj_b = f_sec_sum_tot(objs, is_ann=False, is_fiscal=False)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Setor"
	context = {
		'group': group, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'psec',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Kada Tinan', 'legend': 'Sumariu Pagamentu Kada Tinan'
	}
	return render(request, 'report_pay_g/pay_sec_sum.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGSecSumYear(request, year):
	group = get_roles(request)
	objects = f_sec_sum_y(year, is_ann=False, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(date__year=year, contract__is_fiscal=False).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, contract__is_fiscal=False).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Sector.objects.filter().all()
	tot_b = f_sec_sum_tot_y(objs, year, is_ann=False, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'g', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Tuir Setor', 'legend': f'Sumariu Pagamentu Tuie Setor'
	}
	return render(request, 'report_pay_g/pay_sec_year.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGSecSumMonth(request, year, month):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	objects = f_sec_sum_m(year, month, is_ann=False, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=False).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=False).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Sector.objects.filter().all()
	tot_b = f_sec_sum_tot_m(objs, year, month, is_ann=False, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'g',
		'title': f'Sumariu Pagamentu Tuir Setor', 'legend': f'Sumariu Pagamentu Tuir Setor'
	}
	return render(request, 'report_pay_g/pay_sec_month.html', context)
#
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGSecSumYearDet(request, year, pk):
	group = get_roles(request)
	obj = get_object_or_404(Sector, pk=pk)
	objects = f_sec_sum_y_det(obj, year, is_ann=False, is_fiscal=False)
	subtitle = f"{obj.name} Tinan {year}"
	context = {
		'group': group, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'g',
		'title': f'Lista Pagamentu Tuir Setor', 'legend': f'Lista Pagamentu Tuir Setor'
	}
	return render(request, 'report_pay_g/pay_sec_det.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGSecSumMonthDet(request, year, month, pk):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	obj = get_object_or_404(Sector, pk=pk)
	objects = f_sec_sum_m_det(obj, year, month, is_ann=False, is_fiscal=False)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'g', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Setor', 'legend': f'Lista Pagamentu Setor'
	}
	return render(request, 'report_pay_g/pay_sec_det.html', context)
### CAPITAL
from report.utils_pay_cap import f_cap_all, f_cap_year, f_cap_sum, f_cap_sum_tot, f_cap_sum_y, f_cap_sum_tot_y,\
	f_cap_sum_m, f_cap_sum_tot_m, f_cap_sum_y_det, f_cap_sum_m_det

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCapAll(request, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(Capital, pk=pk)
	objects = f_cap_all(obj, is_ann=False, is_fiscal=False)
	subtitle = f'Capital {obj.name} ({obj.code})'
	context = {
		'group': group, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu', 'legend': f'Lista Pagamentu'
	}
	return render(request, 'report_pay_g/pay_all_list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCapYear(request, year, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(Capital, pk=pk)
	objects = f_cap_year(obj, year, is_ann=False, is_fiscal=False)
	subtitle = f'Capital {obj.name} ({obj.code})'
	context = {
		'group': group, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Tinan {year}', 'legend': f'Lista Pagamentu Tinan {year}'
	}
	return render(request, 'report_pay_g/pay_all_list.html', context)
#

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCapSum(request):
	group = get_roles(request)
	objects = f_cap_sum(is_ann=False, is_fiscal=False)	
	tot_a_1 = Payment.objects.filter(contract__is_fiscal=False).count()
	tot_a_2 = Payment.objects.filter(contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = Capital.objects.filter().all()
	obj_b = f_cap_sum_tot(objs, is_ann=False, is_fiscal=False)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Capital"
	context = {
		'group': group, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'pcat',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Kada Tinan', 'legend': 'Sumariu Pagamentu Kada Tinan'
	}
	return render(request, 'report_pay_g/pay_cap_sum.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCapSumYear(request, year):
	group = get_roles(request)
	objects = f_cap_sum_y(year, is_ann=False, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(date__year=year, contract__is_fiscal=False).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, contract__is_fiscal=False).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Capital.objects.filter().all()
	tot_b = f_cap_sum_tot_y(objs, year, is_ann=False, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'g', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Tuir Capital', 'legend': f'Sumariu Pagamentu Tuie Capital'
	}
	return render(request, 'report_pay_g/pay_cap_year.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCapSumMonth(request, year, month):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	objects = f_cap_sum_m(year, month, is_ann=False, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=False).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=False).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Capital.objects.filter().all()
	tot_b = f_cap_sum_tot_m(objs, year, month, is_ann=False, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'g',
		'title': f'Sumariu Pagamentu Tuir Capital', 'legend': f'Sumariu Pagamentu Tuir Capital'
	}
	return render(request, 'report_pay_g/pay_cap_month.html', context)
#

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCapSumYearDet(request, year, pk):
	group = get_roles(request)
	obj = get_object_or_404(Capital, pk=pk)
	objects = f_cap_sum_y_det(obj, year, is_ann=False, is_fiscal=False)
	subtitle = f"{obj.name} ({obj.code}) Tinan {year}"
	context = {
		'group': group, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'g',
		'title': f'Lista Pagamentu Tuir Capital', 'legend': f'Lista Pagamentu Tuir Capital'
	}
	return render(request, 'report_pay_g/pay_cap_det.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCapSumMonthDet(request, year, month, pk):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	obj = get_object_or_404(Capital, pk=pk)
	objects = f_cap_sum_m_det(obj, year, month, is_ann=False, is_fiscal=False)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'g', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Capital', 'legend': f'Lista Pagamentu Capital'
	}
	return render(request, 'report_pay_g/pay_cap_det.html', context)