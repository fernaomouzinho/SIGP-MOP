from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from custom.models import PType, Year, Division
from project.models import Project
from contract.models import Contract, Amendment
from payment.models import Payment
from users.decorators import allowed_users
from sigp.utils import get_roles

### TYPE
@login_required
def rdivPTypeSum(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	ptypes = PType.objects.filter().all()
	years = Year.objects.filter().all()
	objects = []
	for i in years:
		obj = []
		for j in ptypes:
			j_a = Project.objects.filter(owner=div, ptype=j, year=i).all().count()
			obj.append([j,j_a])
		objects.append([i,obj])
	th_w = round(100/float(ptypes.count()),2)
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'ptypes': ptypes, 'objects': objects, 'th_w': th_w,
		'subtitle': subtitle, 'title': f'Lista Projetu Tuir Tipu', 'legend': f'Lista Projetu Tuir Tipu',
	}
	return render(request, 'reportdiv_t/r_ptype_sum.html', context)

@login_required
def rdivPTypeList(request, pk, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	ptype = get_object_or_404(PType, pk=pk2)
	projs = Project.objects.filter(owner=div, ptype=ptype).all()
	objects = []
	for i in projs:
		c = Contract.objects.filter(project=i).last()
		a = Amendment.objects.filter(contract__project=i).first()
		p = Payment.objects.filter(contract=c).last()
		objects.append([i,c,a,p])
	years = Project.objects.filter(ptype=ptype).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'ptype': ptype, 'objects': objects, 'years': years,
		'subtitle': subtitle, 'title': f'Lista Projetu {ptype}', 'legend': f'Lista Projetu {ptype}',
	}
	return render(request, 'reportdiv_t/r_ptype_list.html', context)

@login_required
def rdivPTypeYearList(request, pk, pk2, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	ptype = get_object_or_404(PType, pk=pk2)
	projs = Project.objects.filter(owner=div, ptype=ptype, year__year=year).all()
	objects = []
	for i in projs:
		c = Contract.objects.filter(project=i).last()
		a = Amendment.objects.filter(contract__project=i).first()
		p = Payment.objects.filter(contract=c).last()
		objects.append([i,c,a,p])
	years = Project.objects.filter(ptype=ptype).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'year': year, 'ptype': ptype, 'objects': objects, 'years': years, 'page': 'pyear',
		'subtitle': subtitle, 'title': f'Lista Projetu {ptype} Tinan {year}',
		'legend': f'Lista Projetu {ptype} Tinan {year}',
	}
	return render(request, 'reportdiv_t/r_ptype_list.html', context)