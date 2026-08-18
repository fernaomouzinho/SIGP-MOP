import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles
from django.db.models import Sum
from contract.models import Contract, Amendment, ContractComp, ContractYear
from payment.models import Payment
from contract.models import Amendment, ContractComp
from custom.models import PCategory, Capital, Sector, PCat
from conf.utils import f_monthname_tet
from report.utils_pay import f_pay_cat, f_pay_sec, f_pay_cap, f_pay_mopcat

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayDash(request):
	group = get_roles(request)
	tot_cont_a = ContractYear.objects.filter(contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_paid_a = Payment.objects.filter(contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_bal_a = 0
	if tot_paid_a: tot_bal_a = tot_cont_a-tot_paid_a
	tot_cont_b = ContractYear.objects.filter(contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_paid_b = Payment.objects.filter(contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_bal_b = 0
	if tot_paid_b: tot_bal_b = tot_cont_b-tot_paid_b
	#
	tot_mopcats_a = f_pay_mopcat(PCat, None, False)
	tot_cats_a = f_pay_cat(PCategory, None, False)
	tot_secs_a = f_pay_sec(Sector, None, False)
	tot_caps_a = f_pay_cap(Capital, None, False)
	tot_mopcats_b = f_pay_mopcat(PCat, None, True)
	tot_cats_b = f_pay_cat(PCategory, None, True)
	tot_secs_b = f_pay_sec(Sector, None, True)
	tot_caps_b = f_pay_cap(Capital, None, True)
	years = ContractYear.objects.distinct().values('year').all().order_by('-year')
	context = {
		'group': group, 'years': years,
		'tot_cont_a': tot_cont_a, 'tot_paid_a': tot_paid_a, 'tot_bal_a': tot_bal_a,
		'tot_cont_b': tot_cont_b, 'tot_paid_b': tot_paid_b, 'tot_bal_b': tot_bal_b,
		'tot_cats_a': tot_cats_a, 'tot_secs_a': tot_secs_a, 'tot_caps_a': tot_caps_a, 
		'tot_cats_b': tot_cats_b, 'tot_secs_b': tot_secs_b, 'tot_caps_b': tot_caps_b, 
		'tot_mopcats_a':tot_mopcats_a, 'tot_mopcats_b':tot_mopcats_b,
		'page': 'pdash', 'subtitle': 'Projetu Foun no Reaproriasaun',
		'title': 'Sumariu Kontratu & Pagamentu Jeral', 'legend': 'Sumariu Kontratu & Pagamentu Jeral'
	}
	return render(request, 'report_pay/pay_dash.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayYear(request, year):
	group = get_roles(request)
	check = ContractYear.objects.filter(contract__is_fiscal=False, year=year).all()
	tot_cont_a, tot_paid_a, tot_bal_a, tot_cats_a, tot_secs_a, tot_caps_a = [],[],0,[],[],[]
	tot_cont_b, tot_paid_b, tot_bal_b, tot_cats_b, tot_secs_b, tot_caps_b = [],[],0,[],[],[]
	if check:
		tot_cont_a = ContractYear.objects.filter(contract__is_fiscal=False, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid_a = Payment.objects.filter(contract__is_fiscal=False, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if tot_paid_a: tot_bal_a = tot_cont_a-tot_paid_a
		tot_cont_b = ContractYear.objects.filter(contract__is_fiscal=True, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid_b = Payment.objects.filter(contract__is_fiscal=True, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if tot_paid_b: tot_bal_b = tot_cont_b-tot_paid_b
		# 
		tot_mopcats_a = f_pay_mopcat(PCat, year, False)
		tot_cats_a = f_pay_cat(PCategory, year, False)
		tot_secs_a = f_pay_sec(Sector, year, False)
		tot_caps_a = f_pay_cap(Capital, year, False)
		tot_mopcats_b = f_pay_mopcat(PCat, year, True)
		tot_cats_b = f_pay_cat(PCategory, year, True)
		tot_secs_b = f_pay_sec(Sector, year, True)
		tot_caps_b = f_pay_cap(Capital, year, True)
		
	years = ContractYear.objects.distinct().values('year').all().order_by('-year')
	context = {
		'group': group, 'years': years,
		'tot_cont_a': tot_cont_a, 'tot_paid_a': tot_paid_a, 'tot_bal_a': tot_bal_a, 
		'tot_cont_b': tot_cont_b, 'tot_paid_b': tot_paid_b, 'tot_bal_b': tot_bal_b, 
		'tot_cats_a': tot_cats_a, 'tot_secs_a': tot_secs_a, 'tot_caps_a': tot_caps_a,
		'tot_cats_b': tot_cats_b, 'tot_secs_b': tot_secs_b, 'tot_caps_b': tot_caps_b,
		'tot_mopcats_a':tot_mopcats_a, 'tot_mopcats_b':tot_mopcats_b,
		'year': year, 'page': 'pyear',
		'subtitle': 'Projetu Foun no Reaproriasaun',
		'title': f'Sumariu Pagamentu ba Kontratu Tinan {year}', 'legend': f'Sumariu Pagamentu ba Kontratu Tinan {year}'
	}
	return render(request, 'report_pay/pay_dash_year.html', context)
###
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayDateList(request, year, month, date, page):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	pays = Payment.objects.filter(date=date).all()
	objects = []
	for pay in pays:
		comp = ContractComp.objects.filter(contract=pay.contract).all()
		cont = pay.contract
		proj = cont.project
		amd = Amendment.objects.filter(contract=cont).first()
		pay = Payment.objects.filter(date=date, contract=cont).last()
		prog_pag = round(pay.com_amount*100/amd.total,2)
		objects.append([proj,cont,comp,pay,prog_pag,amd.total])
	m = Payment.objects.filter(date__year=year).distinct().values('date__month').order_by('date__month').exclude(com_amount=0)
	months = []
	for j in m:
		months.append([f_monthname_tet(int(j['date__month'])),j['date__month']])
	date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
	subtitle = f'Data {date}'
	context = {
		'group': group, 'year': year, 'month': month, 'date': date, 'objects': objects, 'months': months, 'monthname': monthname,
		'page': page, 'page2': 'pdate',
		'subtitle': subtitle, 'title': f'Relatoriu Pagamentu', 'legend': f'Relatoriu Pagamentu'
	}
	return render(request, 'report_pay/pay_all_detail.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayMonthList(request, year, month, page):
	group = get_roles(request)
	monthname = f_monthname_tet(int(month))
	pays = Payment.objects.filter(date__year=year, date__month=month).distinct().values('contract').all()
	objects = []
	for pay in pays:
		cont = Contract.objects.filter(id=pay['contract']).first()
		comp = ContractComp.objects.filter(contract=cont).all()
		proj = cont.project
		amd = Amendment.objects.filter(contract=cont).first()
		pay = Payment.objects.filter(date__year=year, date__month=month, contract=cont).last()
		prog_pag = round(pay.com_amount*100/amd.total,2)
		objects.append([proj,cont,comp,pay,prog_pag,amd.total])
	subtitle = f'Fulan {monthname}/{year}'
	context = {
		'group': group, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page': page, 'page2': 'pmonth',
		'subtitle': subtitle, 'title': f'Lista Pagamentu ', 'legend': f'Lista Pagamentu'
	}
	return render(request, 'report_pay/pay_all_detail.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPayYearList(request, year, page):
	group = get_roles(request)
	pays = Payment.objects.filter(date__year=year).distinct().values('contract').all()
	objects = []
	for pay in pays:
		cont = Contract.objects.filter(id=pay['contract']).first()
		proj = cont.project
		comp = ContractComp.objects.filter(contract=cont).all()
		amd = Amendment.objects.filter(contract=cont).first()
		pay = Payment.objects.filter(date__year=year, contract=cont).last()
		prog_pag = 0
		if pay:
			prog_pag = round(pay.com_amount*100/amd.total,2)
		objects.append([proj,cont,comp,pay,prog_pag,amd.total])
	subtitle = f'Tinan {year}'
	context = {
		'group': group, 'year': year, 'objects': objects, 'page': page, 'page2': 'pyear',
		'subtitle': subtitle, 'title': f'Lista Pagamentu', 'legend': f'Lista Pagamentu'
	}
	return render(request, 'report_pay/pay_all_detail.html', context)
###