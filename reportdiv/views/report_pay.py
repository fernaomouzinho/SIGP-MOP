import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from contract.models import Contract, Amendment, ContractComp, ContractYear
from payment.models import Payment
from contract.models import Amendment, ContractComp
from custom.models import Division, PCategory, Capital, Sector
from conf.utils import f_monthname_tet
from conf.user_utils import c_user_div, c_user_dna, c_user_dnof
from reportdiv.utils_pay import f_pay_cat, f_pay_sec, f_pay_cap
from users.decorators import allowed_users
from sigp.utils import get_roles

@login_required
def rdivHome(request):
	group = get_roles(request)
	div = []
	if "sigp_dna" in group:
			div = c_user_dna(request.user)
	
	elif "sigp_dnof" in group:
		div = c_user_dnof(request.user)

	elif "sigp_div" in group:
		div = c_user_div(request.user)
	context = {
		'group': group, 'div': div, 'page': 'ppay', 'page2':'pg',
		'title': 'Sumariu Pagamentu', 'legend': 'Sumariu Pagamentu',
	}
	return render(request, 'reportdiv_t/dash_div.html', context)

@login_required
def rdivAnnHome(request):
	group = get_roles(request)
	div = []
	if group == "dna": div = c_user_dna(request.user)
	elif group == "dnof": div = c_user_dnof(request.user)
	elif group == "div": div = c_user_div(request.user)
	context = {
		'group': group, 'div': div, 'page': 'ppay', 'page2': 'pann',
		'title': 'Sumariu Pagamentu', 'legend': 'Sumariu Pagamentu',
	}
	return render(request, 'reportdiv_t/dash_div.html', context)
###
@login_required
def rdivPayDash(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	tot_cont_a = ContractYear.objects.filter(contract__project__owner=div, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_paid_a = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_bal_a = 0
	if tot_paid_a: tot_bal_a = tot_cont_a-tot_paid_a
	tot_cont_b = ContractYear.objects.filter(contract__project__owner=div, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_paid_b = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
	tot_bal_b = 0
	if tot_paid_b: tot_bal_b = tot_cont_b-tot_paid_b
	# 
	tot_cats_a = f_pay_cat(div, PCategory, None, False)
	tot_secs_a = f_pay_sec(div, Sector, None, False)
	tot_caps_a = f_pay_cap(div, Capital, None, False)
	tot_cats_b = f_pay_cat(div, PCategory, None, True)
	tot_secs_b = f_pay_sec(div, Sector, None, True)
	tot_caps_b = f_pay_cap(div, Capital, None, True)
	years = ContractYear.objects.distinct().values('year').all().order_by('-year')
	context = {
		'group': group, 'div': div, 'years': years,
		'tot_cont_a': tot_cont_a, 'tot_paid_a': tot_paid_a, 'tot_bal_a': tot_bal_a,
		'tot_cont_b': tot_cont_b, 'tot_paid_b': tot_paid_b, 'tot_bal_b': tot_bal_b,
		'tot_cats_a': tot_cats_a, 'tot_secs_a': tot_secs_a, 'tot_caps_a': tot_caps_a, 
		'tot_cats_b': tot_cats_b, 'tot_secs_b': tot_secs_b, 'tot_caps_b': tot_caps_b, 
		'page': 'pdash', 'subtitle': 'Projetu Foun no Reaproriasaun',
		'title': 'Sumariu Kontratu & Pagamentu Jeral', 'legend': 'Sumariu Kontratu & Pagamentu Jeral'
	}
	return render(request, 'reportdiv_pay/pay_dash.html', context)

@login_required
def rdivPayYear(request, pk, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	check = ContractYear.objects.filter(contract__project__owner=div, contract__is_fiscal=False, year=year).all()
	tot_cont_a, tot_paid_a, tot_bal_a, tot_cats_a, tot_secs_a, tot_caps_a = [],[],0,[],[],[]
	tot_cont_b, tot_paid_b, tot_bal_b, tot_cats_b, tot_secs_b, tot_caps_b = [],[],0,[],[],[]
	if check:
		tot_cont_a = ContractYear.objects.filter(contract__project__owner=div, contract__is_fiscal=False, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid_a = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=False, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if tot_paid_a: tot_bal_a = tot_cont_a-tot_paid_a
		tot_cont_b = ContractYear.objects.filter(contract__project__owner=div, contract__is_fiscal=True, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid_b = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=True, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		if tot_paid_b: tot_bal_b = tot_cont_b-tot_paid_b
		# 
		tot_cats_a = f_pay_cat(div, PCategory, year, False)
		tot_secs_a = f_pay_sec(div, Sector, year, False)
		tot_caps_a = f_pay_cap(div, Capital, year, False)
		tot_cats_b = f_pay_cat(div, PCategory, year, True)
		tot_secs_b = f_pay_sec(div, Sector, year, True)
		tot_caps_b = f_pay_cap(div, Capital, year, True)
	years = ContractYear.objects.distinct().values('year').all().order_by('-year')
	context = {
		'group': group, 'div':div, 'years': years,
		'tot_cont_a': tot_cont_a, 'tot_paid_a': tot_paid_a, 'tot_bal_a': tot_bal_a, 
		'tot_cont_b': tot_cont_b, 'tot_paid_b': tot_paid_b, 'tot_bal_b': tot_bal_b, 
		'tot_cats_a': tot_cats_a, 'tot_secs_a': tot_secs_a, 'tot_caps_a': tot_caps_a,
		'tot_cats_b': tot_cats_b, 'tot_secs_b': tot_secs_b, 'tot_caps_b': tot_caps_b,
		'year': year, 'page': 'pyear',
		'subtitle': 'Projetu Foun no Reaproriasaun',
		'title': f'Sumariu Pagamentu ba Kontratu Tinan {year}', 'legend': f'Sumariu Pagamentu ba Kontratu Tinan {year}'
	}
	return render(request, 'reportdiv_pay/pay_dash_year.html', context)
###
@login_required
def rdivPayDateList(request, pk, year, month, date, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	monthname = f_monthname_tet(int(month))
	pays = Payment.objects.filter(contract__project__owner=div, date=date).all()
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
		'group': group, 'div':div, 'year': year, 'month': month, 'date': date, 'objects': objects, 'months': months, 'monthname': monthname,
		'page': page, 'page2': 'pdate', 'subtitle': subtitle,
		'title': f'Relatoriu Pagamentu', 'legend': f'Relatoriu Pagamentu'
	}
	return render(request, 'reportdiv_pay/pay_all_detail.html', context)

@login_required
def rdivPayMonthList(request, pk, year, month, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	monthname = f_monthname_tet(int(month))
	pays = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month).distinct().values('contract').all()
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
		'group': group, 'div': div, 'year': year, 'month': month, 'objects': objects, 'monthname': monthname,
		'page': page, 'page2': 'pmonth', 'subtitle': subtitle,
		'title': f'Lista Pagamentu ', 'legend': f'Lista Pagamentu'
	}
	return render(request, 'reportdiv_pay/pay_all_detail.html', context)

@login_required
def rdivPayYearList(request, pk, year, page):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	pays = Payment.objects.filter(contract__project__owner=div, date__year=year).distinct().values('contract').all()
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
		'group': group, 'div':div, 'year': year, 'objects': objects, 'page': page, 'page2': 'pyear',
		'subtitle': subtitle, 
		'title': f'Lista Pagamentu', 'legend': f'Lista Pagamentu'
	}
	return render(request, 'reportdiv_pay/pay_all_detail.html', context)
###