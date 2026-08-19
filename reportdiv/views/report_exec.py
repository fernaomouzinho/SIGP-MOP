from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from contract.models import Amendment, ContractComp
from custom.models import Division
from payment.models import Payment
from conf.utils import f_monthname_tet
from users.decorators import allowed_users
from sigp.utils import get_roles


def rdivExecList(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = []
	for i in range(1,13):
		mname = f_monthname_tet(int(i))
		tot = 0
		pay = Payment.objects.filter(contract__project__owner=div, date__month=i).aggregate(Sum('total')).get('total__sum', 0.00)
		if pay: tot = pay
		objects.append([i,mname,tot])
	years = Payment.objects.distinct().values('date__year').all().order_by('-date__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div':div, 'objects': objects, 'years': years,
		'subtitle': subtitle, 'title': f'Sumariu Execusaun Kada Fulan', 'legend': f'Sumariu Execusaun Kada Fulan'
	}
	return render(request, 'reportdiv_pay/exec_list.html', context)


def rdivExecYearList(request, pk, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = []
	for i in range(1,13):
		mname = f_monthname_tet(int(i))
		tot = 0
		pay = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=i).aggregate(Sum('total')).get('total__sum', 0.00)
		if pay: tot = pay
		objects.append([i,mname,tot])
	years = Payment.objects.distinct().values('date__year').all().order_by('-date__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'year': year, 'objects': objects, 'years': years,
		'subtitle': subtitle, 'title': f'Sumariu Execusaun Tinan {year}', 'legend': f'Sumariu Execusaun Tinan {year}'
	}
	return render(request, 'reportdiv_pay/exec_year_list.html', context)
#

def rdivExecPayAllList(request, pk, month):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	mname = f_monthname_tet(int(month))
	pays = Payment.objects.filter(contract__project__owner=div, date__month=month).all()
	objects = []
	for i in pays:
		cont = i.contract
		proj = cont.project
		contyear = i.contyear.year
		comp = ContractComp.objects.filter(contract=cont).all()
		amd = Amendment.objects.filter(contract=cont).first()
		prog_pag = round(i.com_amount*100/amd.total,2)
		objects.append([proj,cont,comp,i,prog_pag,amd.total,contyear])
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'objects': objects, 'page': 'pall',
		'subtitle': subtitle, 'title': f'Sumariu Execusaun Fulan {mname}', 'legend': f'Sumariu Execusaun Fulan {mname}'
	}
	return render(request, 'reportdiv_pay/exec_pay_list.html', context)


def rdivExecPayYearList(request, pk, year, month):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	mname = f_monthname_tet(int(month))
	pays = Payment.objects.filter(contract__project__owner=div, date__year=year, date__month=month).all()
	objects = []
	for i in pays:
		cont = i.contract
		proj = cont.project
		contyear = i.contyear.year
		comp = ContractComp.objects.filter(contract=cont).all()
		amd = Amendment.objects.filter(contract=cont).first()
		prog_pag = round(i.com_amount*100/amd.total,2)
		objects.append([proj,cont,comp,i,prog_pag,amd.total,contyear])
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'year':year, 'objects': objects, 'page': 'pyear',
		'subtitle': subtitle, 'title': f'Sumariu Execusaun Fulan {mname}', 'legend': f'Sumariu Execusaun Fulan {mname}'
	}
	return render(request, 'reportdiv_pay/exec_pay_list.html', context)
