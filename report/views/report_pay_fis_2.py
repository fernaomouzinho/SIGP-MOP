from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from custom.models import Sector, Capital
from payment.models import Payment
from conf.utils import f_monthname_tet
from report.utils_pay_sec import f_sec_all, f_sec_year, f_sec_sum, f_sec_sum_tot, f_sec_sum_y, f_sec_sum_tot_y,\
	f_sec_sum_m, f_sec_sum_tot_m, f_sec_sum_y_det, f_sec_sum_m_det
from users.decorators import allowed_users
from sigp.utils import get_roles

### SECTOR
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisSecAll(request, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(Sector, pk=pk)
	objects = f_sec_all(obj, is_ann=False, is_fiscal=True)
	subtitle = f'Setor {obj.name}'
	context = {
		'group': group, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Fiskal', 'legend': f'Lista Pagamentu Fiskal'
	}
	return render(request, 'report_pay_fis/pay_all_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisSecYear(request, year, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(Sector, pk=pk)
	objects = f_sec_year(obj, year, is_ann=False, is_fiscal=True)
	subtitle = f'Setor {obj.name}'
	context = {
		'group': group, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Fiskal Tinan {year}', 'legend': f'Lista Pagamentu Fiskal Tinan {year}'
	}
	return render(request, 'report_pay_fis/pay_all_list.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisSecSum(request):
	group = get_roles(request)
	objects = f_sec_sum(is_ann=False, is_fiscal=True)	
	tot_a_1 = Payment.objects.filter(contract__is_fiscal=True).count()
	tot_a_2 = Payment.objects.filter(contract__is_fiscal=True).exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__is_fiscal=True).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = Sector.objects.filter().all()
	obj_b = f_sec_sum_tot(objs, is_ann=False, is_fiscal=True)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Setor"
	context = {
		'group': group, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'psec',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Fiskal Kada Tinan', 'legend': 'Sumariu Pagamentu Fiskal Kada Tinan'
	}
	return render(request, 'report_pay_fis/pay_sec_sum.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisSecSumYear(request, year):
	group = get_roles(request)
	objects = f_sec_sum_y(year, is_ann=False, is_fiscal=True)
	tot_a_1 = Payment.objects.filter(date__year=year, contract__is_fiscal=True).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, contract__is_fiscal=True).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, contract__is_fiscal=True).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Sector.objects.filter().all()
	tot_b = f_sec_sum_tot_y(objs, year, is_ann=False, is_fiscal=True)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'fis', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Fiskal Tuir Setor', 'legend': f'Sumariu Pagamentu Fiskal Tuir Setor'
	}
	return render(request, 'report_pay_fis/pay_sec_year.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisSecSumMonth(request, year, month):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	objects = f_sec_sum_m(year, month, is_ann=False, is_fiscal=True)
	tot_a_1 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=True).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=True).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=True).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Sector.objects.filter().all()
	tot_b = f_sec_sum_tot_m(objs, year, month, is_ann=False, is_fiscal=True)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'fis',
		'title': f'Sumariu Pagamentu Fiskal Tuir Setor', 'legend': f'Sumariu Pagamentu Fiskal Tuir Setor'
	}
	return render(request, 'report_pay_g/pay_sec_month.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisSecSumYearDet(request, year, pk):
	group = get_roles(request)
	obj = get_object_or_404(Sector, pk=pk)
	objects = f_sec_sum_y_det(obj, year, is_ann=False, is_fiscal=True)
	subtitle = f"{obj.name} Tinan {year}"
	context = {
		'group': group, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'fis',
		'title': f'Lista Pagamentu Fiskal Tuir Setor', 'legend': f'Lista Pagamentu Fiskal Tuir Setor'
	}
	return render(request, 'report_pay_g/pay_sec_det.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisSecSumMonthDet(request, year, month, pk):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	obj = get_object_or_404(Sector, pk=pk)
	objects = f_sec_sum_m_det(obj, year, month, is_ann=False, is_fiscal=True)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'fis', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Fiskal Setor', 'legend': f'Lista Pagamentu Fiskal Setor'
	}
	return render(request, 'report_pay_g/pay_sec_det.html', context)
### CAPITAL
from report.utils_pay_cap import f_cap_all, f_cap_year, f_cap_sum, f_cap_sum_tot, f_cap_sum_y, f_cap_sum_tot_y,\
	f_cap_sum_m, f_cap_sum_tot_m, f_cap_sum_y_det, f_cap_sum_m_det

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisCapAll(request, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(Capital, pk=pk)
	objects = f_cap_all(obj, is_ann=False, is_fiscal=True)
	subtitle = f'Capital {obj.name} ({obj.code})'
	context = {
		'group': group, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Fiskal', 'legend': f'Lista Pagamentu Fiskal'
	}
	return render(request, 'report_pay_fis/pay_all_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisCapYear(request, year, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(Capital, pk=pk)
	objects = f_cap_year(obj, year, is_ann=False, is_fiscal=True)
	subtitle = f'Capital {obj.name} ({obj.code})'
	context = {
		'group': group, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Fiskal Tinan {year}', 'legend': f'Lista Pagamentu Fiskal Tinan {year}'
	}
	return render(request, 'report_pay_fis/pay_all_list.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisCapSum(request):
	group = get_roles(request)
	objects = f_cap_sum(is_ann=False, is_fiscal=True)	
	tot_a_1 = Payment.objects.filter(contract__is_fiscal=True).count()
	tot_a_2 = Payment.objects.filter(contract__is_fiscal=True).exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__is_fiscal=True).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = Capital.objects.filter().all()
	obj_b = f_cap_sum_tot(objs, is_ann=False, is_fiscal=True)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Capital"
	context = {
		'group': group, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'pcat',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Fiskal Kada Tinan', 'legend': 'Sumariu Pagamentu Fiskal Kada Tinan'
	}
	return render(request, 'report_pay_fis/pay_cap_sum.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisCapSumYear(request, year):
	group = get_roles(request)
	objects = f_cap_sum_y(year, is_ann=False, is_fiscal=True)
	tot_a_1 = Payment.objects.filter(date__year=year, contract__is_fiscal=True).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, contract__is_fiscal=True).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, contract__is_fiscal=True).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Capital.objects.filter().all()
	tot_b = f_cap_sum_tot_y(objs, year, is_ann=False, is_fiscal=True)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'fis', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Fiskal Tuir Capital', 'legend': f'Sumariu Pagamentu Fiskal Tuir Capital'
	}
	return render(request, 'report_pay_fis/pay_cap_year.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisCapSumMonth(request, year, month):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	objects = f_cap_sum_m(year, month, is_ann=False, is_fiscal=True)
	tot_a_1 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=True).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=True).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=True).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Capital.objects.filter().all()
	tot_b = f_cap_sum_tot_m(objs, year, month, is_ann=False, is_fiscal=True)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'fis',
		'title': f'Sumariu Pagamentu Fiskal Tuir Capital', 'legend': f'Sumariu Pagamentu Fiskal Tuir Capital'
	}
	return render(request, 'report_pay_g/pay_cap_month.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisCapSumYearDet(request, year, pk):
	group = get_roles(request)
	obj = get_object_or_404(Capital, pk=pk)
	objects = f_cap_sum_y_det(obj, year, is_ann=False, is_fiscal=True)
	subtitle = f"{obj.name} ({obj.code}) Tinan {year}"
	context = {
		'group': group, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'fis',
		'title': f'Lista Pagamentu Fiskal Tuir Capital', 'legend': f'Lista Pagamentu Fiskal Tuir Capital'
	}
	return render(request, 'report_pay_g/pay_cap_det.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayFisCapSumMonthDet(request, year, month, pk):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	obj = get_object_or_404(Capital, pk=pk)
	objects = f_cap_sum_m_det(obj, year, month, is_ann=False, is_fiscal=True)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'fis', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Fiskal Capital', 'legend': f'Lista Pagamentu Fiskal Capital'
	}
	return render(request, 'report_pay_g/pay_cap_det.html', context)