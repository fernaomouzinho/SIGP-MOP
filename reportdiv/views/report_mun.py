from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from custom.models import Division, Municipality, Year
from project.models import Project, ProjectLoc
from contract.models import Contract, Amendment
from payment.models import Payment
from users.decorators import allowed_users
from sigp.utils import get_roles


def rdivPMunSum(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	muns = Municipality.objects.filter().all()
	years = Year.objects.filter().all()
	objects = []
	for i in years:
		obj = []
		for j in muns:
			j_a = ProjectLoc.objects.filter(project__owner=div, municipality=j, project__year=i).all().count()
			obj.append([j,j_a])
		objects.append([i,obj])
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'muns': muns, 'objects': objects,
		'subtitle': subtitle, 'title': f'Lista Projetu Tuir Municipiu', 'legend': f'Lista Projetu Tuir Municipiu',
	}
	return render(request, 'reportdiv_t/r_mun_sum.html', context)


def rdivPMunList(request, pk, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	mun = get_object_or_404(Municipality, pk=pk2)
	projs = Project.objects.filter(owner=div, projectloc__municipality=mun).all()
	objects = []
	for i in projs:
		c = Contract.objects.filter(project=i).last()
		a = Amendment.objects.filter(contract__project=i).first()
		p = Payment.objects.filter(contract=c).last()
		objects.append([i,c,a,p])
	years = Project.objects.filter(projectloc__municipality=mun).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'mun': mun, 'objects': objects, 'years': years,
		'subtitle': subtitle, 'title': f'Lista Projetu iha {mun}', 'legend': f'Lista Projetu iha {mun}',
	}
	return render(request, 'reportdiv_t/r_mun_list.html', context)


def rdivPMunYearList(request, pk, pk2, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	mun = get_object_or_404(Municipality, pk=pk2)
	projs = Project.objects.filter(owner=div, projectloc__municipality=mun, year__year=year).all()
	objects = []
	for i in projs:
		c = Contract.objects.filter(project=i).last()
		a = Amendment.objects.filter(contract__project=i).first()
		p = Payment.objects.filter(contract=c).last()
		objects.append([i,c,a,p])
	years = Project.objects.filter(projectloc__municipality=mun).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'mun': mun, 'objects': objects, 'years': years,
		'subtitle': subtitle, 'title': f'Lista Projetu iha {mun} Tinan {year}',
		'legend': f'Lista Projetu iha {mun} Tinan {year}',
	}
	return render(request, 'reportdiv_t/r_mun_list.html', context)