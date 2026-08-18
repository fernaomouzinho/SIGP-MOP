from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
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
def rPayAnnSecAll(request, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(Sector, pk=pk)
	objects = f_sec_all(obj, is_ann=True, is_fiscal=False)
	subtitle = f'Setor {obj.name}'
	context = {
		'group': group, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Annual', 'legend': f'Lista Pagamentu Annual'
	}
	return render(request, 'report_pay_ann/pay_all_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayAnnSecYear(request, year, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(Sector, pk=pk)
	objects = f_sec_year(obj, year, is_ann=True, is_fiscal=False)
	subtitle = f'Setor {obj.name}'
	context = {
		'group': group, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Annual Tinan {year}', 'legend': f'Lista Pagamentu Annual Tinan {year}'
	}
	return render(request, 'report_pay_ann/pay_all_list.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayAnnSecSum(request):
	group = get_roles(request)
	objects = f_sec_sum(is_ann=True, is_fiscal=False)	
	tot_a_1 = Payment.objects.filter().count()
	tot_a_2 = Payment.objects.filter().exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter().exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = Sector.objects.filter().all()
	obj_b = f_sec_sum_tot(objs, is_ann=True, is_fiscal=False)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Setor"
	context = {
		'group': group, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'psec',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Annual Kada Tinan', 'legend': 'Sumariu Pagamentu Annual Kada Tinan'
	}
	return render(request, 'report_pay_ann/pay_sec_sum.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayAnnSecSumYear(request, year):
	group = get_roles(request)
	objects = f_sec_sum_y(year, is_ann=True, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(date__year=year).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Sector.objects.filter().all()
	tot_b = f_sec_sum_tot_y(objs, year, is_ann=True, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'ann', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Annual Tuir Setor', 'legend': f'Sumariu Pagamentu Annual Tuir Setor'
	}
	return render(request, 'report_pay_ann/pay_sec_year.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayAnnSecSumMonth(request, year, month):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	objects = f_sec_sum_m(year, month, is_ann=True, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(date__year=year, date__month=month).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, date__month=month).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, date__month=month).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Sector.objects.filter().all()
	tot_b = f_sec_sum_tot_m(objs, year, month, is_ann=True, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'ann',
		'title': f'Sumariu Pagamentu Annual Tuir Setor', 'legend': f'Sumariu Pagamentu Annual Tuir Setor'
	}
	return render(request, 'report_pay_g/pay_sec_month.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayAnnSecSumYearDet(request, year, pk):
	group = get_roles(request)
	obj = get_object_or_404(Sector, pk=pk)
	objects = f_sec_sum_y_det(obj, year, is_ann=True, is_fiscal=False)
	subtitle = f"{obj.name} Tinan {year}"
	context = {
		'group': group, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'ann',
		'title': f'Lista Pagamentu Annual Tuir Setor', 'legend': f'Lista Pagamentu Annual Tuir Setor'
	}
	return render(request, 'report_pay_g/pay_sec_det.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayAnnSecSumMonthDet(request, year, month, pk):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	obj = get_object_or_404(Sector, pk=pk)
	objects = f_sec_sum_m_det(obj, year, month, is_ann=True, is_fiscal=False)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'ann', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Annual Setor', 'legend': f'Lista Pagamentu Annual Setor'
	}
	return render(request, 'report_pay_g/pay_sec_det.html', context)
### CAPITAL
from report.utils_pay_cap import f_cap_all, f_cap_year, f_cap_sum, f_cap_sum_tot, f_cap_sum_y, f_cap_sum_tot_y,\
	f_cap_sum_m, f_cap_sum_tot_m, f_cap_sum_y_det, f_cap_sum_m_det

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayAnnCapAll(request, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(Capital, pk=pk)
	objects = f_cap_all(obj, is_ann=True, is_fiscal=False)
	subtitle = f'Capital {obj.name} ({obj.code})'
	context = {
		'group': group, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Annual', 'legend': f'Lista Pagamentu Annual'
	}
	return render(request, 'report_pay_ann/pay_all_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayAnnCapYear(request, year, pk, page):
	group = request.user.groups.all()[0].name
	obj = get_object_or_404(Capital, pk=pk)
	objects = f_cap_year(obj, year, is_ann=True, is_fiscal=False)
	subtitle = f'Capital {obj.name} ({obj.code})'
	context = {
		'group': group, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Annual Tinan {year}', 'legend': f'Lista Pagamentu Annual Tinan {year}'
	}
	return render(request, 'report_pay_ann/pay_all_list.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayAnnCapSum(request):
	group = get_roles(request)
	objects = f_cap_sum(is_ann=True, is_fiscal=False)	
	tot_a_1 = Payment.objects.filter().count()
	tot_a_2 = Payment.objects.filter().exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter().exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = Capital.objects.filter().all()
	obj_b = f_cap_sum_tot(objs, is_ann=True, is_fiscal=False)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Capital"
	context = {
		'group': group, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'pcap',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Annual Kada Tinan', 'legend': 'Sumariu Pagamentu Annual Kada Tinan'
	}
	return render(request, 'report_pay_ann/pay_cap_sum.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayAnnCapSumYear(request, year):
	group = get_roles(request)
	objects = f_cap_sum_y(year, is_ann=True, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(date__year=year).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Capital.objects.filter().all()
	tot_b = f_cap_sum_tot_y(objs, year, is_ann=True, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'ann', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Annual Tuir Capital', 'legend': f'Sumariu Pagamentu Annual Tuir Capital'
	}
	return render(request, 'report_pay_ann/pay_cap_year.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayAnnCapSumMonth(request, year, month):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	objects = f_cap_sum_m(year, month, is_ann=True, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(date__year=year, date__month=month).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, date__month=month).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, date__month=month).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = Capital.objects.filter().all()
	tot_b = f_cap_sum_tot_m(objs, year, month, is_ann=True, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'ann',
		'title': f'Sumariu Pagamentu Annual Tuir Capital', 'legend': f'Sumariu Pagamentu Annual Tuir Capital'
	}
	return render(request, 'report_pay_g/pay_cap_month.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayAnnCapSumYearDet(request, year, pk):
	group = get_roles(request)
	obj = get_object_or_404(Capital, pk=pk)
	objects = f_cap_sum_y_det(obj, year, is_ann=True, is_fiscal=False)
	subtitle = f"{obj.name} ({obj.code}) Tinan {year}"
	context = {
		'group': group, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'ann',
		'title': f'Lista Pagamentu Annual Tuir Capital', 'legend': f'Lista Pagamentu Annual Tuir Capital'
	}
	return render(request, 'report_pay_g/pay_cap_det.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayAnnCapSumMonthDet(request, year, month, pk):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	obj = get_object_or_404(Capital, pk=pk)
	objects = f_cap_sum_m_det(obj, year, month, is_ann=True, is_fiscal=False)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'ann', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Annual Capital', 'legend': f'Lista Pagamentu Annual Capital'
	}
	return render(request, 'report_pay_g/pay_cap_det.html', context)