from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.db.models import Sum
from contract.models import Amendment, ContractComp
from payment.models import Payment
from conf.utils import f_monthname_tet
from users.decorators import allowed_users
from sigp.utils import get_roles


@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rExecList(request):
	group = get_roles(request)
	objects = []
	for i in range(1,13):
		mname = f_monthname_tet(int(i))
		tot = 0
		pay = Payment.objects.filter(date__month=i).aggregate(Sum('total')).get('total__sum', 0.00)
		if pay: tot = pay
		objects.append([i,mname,tot])
	years = Payment.objects.distinct().values('date__year').all().order_by('-date__year')
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Sumariu Execusaun Kada Fulan', 'legend': f'Sumariu Execusaun Kada Fulan'
	}
	return render(request, 'report_pay/exec_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rExecYearList(request, year):
	group = get_roles(request)
	objects = []
	for i in range(1,13):
		mname = f_monthname_tet(int(i))
		tot = 0
		pay = Payment.objects.filter(date__year=year, date__month=i).aggregate(Sum('total')).get('total__sum', 0.00)
		if pay: tot = pay
		objects.append([i,mname,tot])
	years = Payment.objects.distinct().values('date__year').all().order_by('-date__year')
	context = {
		'group': group, 'year': year, 'objects': objects, 'years': years,
		'title': f'Sumariu Execusaun Tinan {year}', 'legend': f'Sumariu Execusaun Tinan {year}'
	}
	return render(request, 'report_pay/exec_year_list.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_uivp'])
def rExecPayAllList(request, month):
	group = get_roles(request)
	mname = f_monthname_tet(int(month))
	pays = Payment.objects.filter(date__month=month).all()
	objects = []
	for i in pays:
		cont = i.contract
		proj = cont.project
		contyear = i.contyear.year
		comp = ContractComp.objects.filter(contract=cont).all()
		amd = Amendment.objects.filter(contract=cont).first()
		prog_pag = round(i.com_amount*100/amd.total,2)
		objects.append([proj,cont,comp,i,prog_pag,amd.total,contyear])
	context = {
		'group': group, 'objects': objects, 'page': 'pall',
		'title': f'Sumariu Execusaun Fulan {mname}', 'legend': f'Sumariu Execusaun Fulan {mname}'
	}
	return render(request, 'report_pay/exec_pay_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gab','sigp_uivp'])
def rExecPayYearList(request, year, month):
	group = get_roles(request)
	mname = f_monthname_tet(int(month))
	pays = Payment.objects.filter(date__year=year, date__month=month).all()
	objects = []
	for i in pays:
		cont = i.contract
		proj = cont.project
		contyear = i.contyear.year
		comp = ContractComp.objects.filter(contract=cont).all()
		amd = Amendment.objects.filter(contract=cont).first()
		prog_pag = round(i.com_amount*100/amd.total,2)
		objects.append([proj,cont,comp,i,prog_pag,amd.total,contyear])
	context = {
		'group': group, 'year':year, 'objects': objects, 'page': 'pyear',
		'title': f'Sumariu Execusaun Fulan {mname}', 'legend': f'Sumariu Execusaun Fulan {mname}'
	}
	return render(request, 'report_pay/exec_pay_list.html', context)
