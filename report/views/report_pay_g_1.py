from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles
from django.db.models import Sum
from contract.models import ContractYear
from payment.models import Payment
from custom.models import PCategory, Capital, Sector, PCat
from report.utils_pay import f_pay_cat, f_pay_sec, f_pay_cap, f_pay_mopcat


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGDash(request):
	group = get_roles(request)
	tot_cont = ContractYear.objects.filter(contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_paid = Payment.objects.filter(contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_bal = 0
	if tot_paid: tot_bal = tot_cont-tot_paid
	# 
	tot_mopcats = f_pay_mopcat(PCat, None, False)
	tot_cats = f_pay_cat(PCategory, None, False)
	tot_secs = f_pay_sec(Sector, None, False)
	tot_caps = f_pay_cap(Capital, None, False)
	years = ContractYear.objects.distinct().values('year').all().order_by('-year')
	context = {
		'group': group, 'tot_cont': tot_cont, 'tot_paid': tot_paid, 'tot_bal': tot_bal, 'years': years,
		'tot_cats': tot_cats, 'tot_secs': tot_secs, 'tot_caps': tot_caps, 'tot_mopcats':tot_mopcats,
		'page': 'pdash', 'subtitle': 'Projetu Foun no Reaproriasaun',
		'title': 'Sumariu Kontratu & Pagamentu Jeral', 'legend': 'Sumariu Kontratu & Pagamentu Jeral'
	}
	return render(request, 'report_pay_g/pay_dash.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGYear(request, year):
	group = get_roles(request)
	check = ContractYear.objects.filter(contract__is_fiscal=False, year=year).all()
	tot_cont, tot_paid, tot_bal, tot_mopcats, tot_cats, tot_secs, tot_caps = [],[],0,[],[],[],[]
	if check:
		tot_cont = ContractYear.objects.filter(contract__is_fiscal=False, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contract__is_fiscal=False, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if tot_paid: tot_bal = tot_cont-tot_paid
		# 
		tot_mopcats = f_pay_mopcat(PCat, year, False)
		tot_cats = f_pay_cat(PCategory, year, False)
		tot_secs = f_pay_sec(Sector, year, False)
		tot_caps = f_pay_cap(Capital, year, False)
		
	years = ContractYear.objects.distinct().values('year').all().order_by('-year')
	context = {
		'group': group, 'tot_cont': tot_cont, 'tot_paid': tot_paid, 'tot_bal': tot_bal, 'years': years,
		'tot_cats': tot_cats, 'tot_secs': tot_secs, 'tot_caps': tot_caps, 'tot_mopcats':tot_mopcats,
		'year': year, 'page': 'pyear', 'subtitle': 'Projetu Foun no Reaproriasaun',
		'title': f'Sumariu Pagamentu ba Kontratu Tinan {year}', 'legend': f'Sumariu Pagamentu ba Kontratu Tinan {year}'
	}
	return render(request, 'report_pay_g/pay_dash_year.html', context)
### CAT
from conf.utils import f_monthname_tet
from report.utils_pay_cat import f_cat_all, f_cat_year, f_cat_sum, f_cat_sum_tot, f_cat_sum_y, f_cat_sum_tot_y,\
	f_cat_sum_m, f_cat_sum_tot_m, f_cat_sum_y_det, f_cat_sum_m_det


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCatAll(request, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(PCategory, pk=pk)
	objects = f_cat_all(obj, is_ann=False, is_fiscal=False)
	subtitle = f'Kategoria {obj.name} ({obj.code})'
	context = {
		'group': group, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu', 'legend': f'Lista Pagamentu'
	}
	return render(request, 'report_pay_g/pay_all_list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCatYear(request, year, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(PCategory, pk=pk)
	objects = f_cat_year(obj, year, is_ann=False, is_fiscal=False)
	subtitle = f'Kategoria {obj.name} ({obj.code})'
	context = {
		'group': group, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Tinan {year}', 'legend': f'Lista Pagamentu Tinan {year}'
	}
	return render(request, 'report_pay_g/pay_all_list.html', context)
#

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCatSum(request):
	group = get_roles(request)
	objects = f_cat_sum(is_ann=False, is_fiscal=False)	
	tot_a_1 = Payment.objects.filter(contract__is_fiscal=False).count()
	tot_a_2 = Payment.objects.filter(contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = PCategory.objects.filter().all()
	obj_b = f_cat_sum_tot(objs, is_ann=False, is_fiscal=False)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Katagoria"
	context = {
		'group': group, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'pcat',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Kada Tinan', 'legend': 'Sumariu Pagamentu Kada Tinan'
	}
	return render(request, 'report_pay_g/pay_cat_sum.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCatSumYear(request, year):
	group = get_roles(request)
	objects = f_cat_sum_y(year, is_ann=False, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(date__year=year, contract__is_fiscal=False).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, contract__is_fiscal=False).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = PCategory.objects.filter().all()
	tot_b = f_cat_sum_tot_y(objs, year, is_ann=False, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'g', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Tuir Kategoria', 'legend': f'Sumariu Pagamentu Tuir Kategoria'
	}
	return render(request, 'report_pay_g/pay_cat_year.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCatSumMonth(request, year, month):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	objects = f_cat_sum_m(year, month, is_ann=False, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=False).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=False).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = PCategory.objects.filter().all()
	tot_b = f_cat_sum_tot_m(objs, year, month, is_ann=False, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'g',
		'title': f'Sumariu Pagamentu Tuir Kategoria', 'legend': f'Sumariu Pagamentu Tuir Kategoria'
	}
	return render(request, 'report_pay_g/pay_cat_month.html', context)
#

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCatSumYearDet(request, year, pk):
	group = get_roles(request)
	obj = get_object_or_404(PCategory, pk=pk)
	objects = f_cat_sum_y_det(obj, year, is_ann=False, is_fiscal=False)
	subtitle = f"{obj.name} ({obj.code}) Tinan {year}"
	context = {
		'group': group, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'g',
		'title': f'Lista Pagamentu Tuir Kategoria', 'legend': f'Lista Pagamentu Tuir Kategoria'
	}
	return render(request, 'report_pay_g/pay_cat_det.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGCatSumMonthDet(request, year, month, pk):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	obj = get_object_or_404(PCategory, pk=pk)
	objects = f_cat_sum_m_det(obj, year, month, is_ann=False, is_fiscal=False)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'g', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Kategoria', 'legend': f'Lista Pagamentu Kategoria'
	}
	return render(request, 'report_pay_g/pay_cat_det.html', context)
### MOPCAT
from conf.utils import f_monthname_tet
from report.utils_pay_mopcat import f_mopcat_all, f_mopcat_year, f_mopcat_sum, f_mopcat_sum_tot,\
	f_mopcat_sum_y, f_mopcat_sum_tot_y, f_mopcat_sum_m, f_mopcat_sum_tot_m, f_mopcat_sum_y_det, f_mopcat_sum_m_det


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGMopCatAll(request, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(PCat, pk=pk)
	objects = f_mopcat_all(obj, is_ann=False, is_fiscal=False)
	subtitle = f'Kategoria {obj.name} ({obj.code})'
	context = {
		'group': group, 'objects': objects, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu', 'legend': f'Lista Pagamentu'
	}
	return render(request, 'report_pay_g/pay_all_list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGMopCatYear(request, year, pk, page):
	group = get_roles(request)
	obj = get_object_or_404(PCat, pk=pk)
	objects = f_mopcat_year(obj, year, is_ann=False, is_fiscal=False)
	subtitle = f'Kategoria {obj.name} ({obj.code})'
	context = {
		'group': group, 'objects': objects, 'year': year, 'page': page,
		'subtitle': subtitle, 'title': f'Lista Pagamentu Tinan {year}', 'legend': f'Lista Pagamentu Tinan {year}'
	}
	return render(request, 'report_pay_g/pay_all_list.html', context)
#

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGMopCatSum(request):
	group = get_roles(request)
	objects = f_mopcat_sum(is_ann=False, is_fiscal=False)	
	tot_a_1 = Payment.objects.filter(contract__is_fiscal=False).count()
	tot_a_2 = Payment.objects.filter(contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a_4 = tot_a_2-tot_a_3
	obj_a = [tot_a_1,tot_a_2,tot_a_3,tot_a_4]
	objs = PCat.objects.filter().all()
	obj_b = f_mopcat_sum_tot(objs, is_ann=False, is_fiscal=False)
	totals = [obj_a,obj_b]
	subtitle = f"Tuir Katagoria"
	context = {
		'group': group, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'pcat',
		'subtitle': subtitle, 'title': 'Sumariu Pagamentu Kada Tinan', 'legend': 'Sumariu Pagamentu Kada Tinan'
	}
	return render(request, 'report_pay_g/pay_mopcat_sum.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGMopCatSumYear(request, year):
	group = get_roles(request)
	objects = f_mopcat_sum_y(year, is_ann=False, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(date__year=year, contract__is_fiscal=False).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, contract__is_fiscal=False).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = PCat.objects.filter().all()
	tot_b = f_mopcat_sum_tot_y(objs, year, is_ann=False, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Tinan {year}"
	context = {
		'group': group, 'year': year, 'objs': objs, 'objects': objects, 'totals': totals, 'page': 'g', 'subtitle': subtitle,
		'title': f'Sumariu Pagamentu Tuir Kategoria', 'legend': f'Sumariu Pagamentu Tuir Kategoria'
	}
	return render(request, 'report_pay_g/pay_mopcat_year.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGMopCatSumMonth(request, year, month):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	objects = f_mopcat_sum_m(year, month, is_ann=False, is_fiscal=False)
	tot_a_1 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=False).distinct().values('contract').count()
	tot_a_2 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=False).distinct().values('contract').exclude(total=0.00).aggregate(Sum('contract__amendment__total')).get('contract__amendment__total__sum', 0.00)
	tot_a_3 = Payment.objects.filter(date__year=year, date__month=month, contract__is_fiscal=False).exclude(total=0.00).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_a = [tot_a_1,tot_a_2,tot_a_3]
	objs = PCat.objects.filter().all()
	tot_b = f_mopcat_sum_tot_m(objs, year, month, is_ann=False, is_fiscal=False)
	totals = [tot_a,tot_b]
	subtitle = f"Fulan {monthname}/{year}"
	context = {
		'group': group, 'objs': objs, 'year': year, 'month': month, 'objects': objects, 'totals': totals,
		'subtitle': subtitle, 'page': 'g',
		'title': f'Sumariu Pagamentu Tuir Kategoria', 'legend': f'Sumariu Pagamentu Tuir Kategoria'
	}
	return render(request, 'report_pay_g/pay_mopcat_month.html', context)
#

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGMopCatSumYearDet(request, year, pk):
	group = get_roles(request)
	obj = get_object_or_404(PCat, pk=pk)
	objects = f_mopcat_sum_y_det(obj, year, is_ann=False, is_fiscal=False)
	subtitle = f"{obj.name} ({obj.code}) Tinan {year}"
	context = {
		'group': group, 'year': year, 'objects': objects, 'subtitle': subtitle, 'page1': 'g',
		'title': f'Lista Pagamentu Tuir Kategoria', 'legend': f'Lista Pagamentu Tuir Kategoria'
	}
	return render(request, 'report_pay_g/pay_mopcat_det.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayGMopCatSumMonthDet(request, year, month, pk):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	obj = get_object_or_404(PCat, pk=pk)
	objects = f_mopcat_sum_m_det(obj, year, month, is_ann=False, is_fiscal=False)
	subtitle = f"{obj.name} Fulan {month}/{year}"
	context = {
		'group': group, 'obj': obj, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page1': 'g', 'page2': 'month', 'subtitle': subtitle,
		'title': f'Lista Pagamentu Kategoria', 'legend': f'Lista Pagamentu Kategoria'
	}
	return render(request, 'report_pay_g/pay_mopcat_det.html', context)