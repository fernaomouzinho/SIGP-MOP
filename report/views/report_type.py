from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles
from custom.models import PType, Year
from project.models import Project
from contract.models import Contract, Amendment
from payment.models import Payment

### TYPE
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPTypeSum(request):
	group = get_roles(request)
	ptypes = PType.objects.filter().all()
	years = Year.objects.filter().all()
	objects = []
	for i in years:
		obj = []
		for j in ptypes:
			j_a = Project.objects.filter(ptype=j, year=i).all().count()
			obj.append([j,j_a])
		objects.append([i,obj])
	th_w = round(100/float(ptypes.count()),2)
	context = {
		'group': group, 'ptypes': ptypes, 'objects': objects, 'th_w': th_w,
		'title': f'Lista Projetu Tuir Tipu', 'legend': f'Lista Projetu Tuir Tipu',
	}
	return render(request, 'report_t/r_ptype_sum.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPTypeList(request, pk):
	group = get_roles(request)
	ptype = get_object_or_404(PType, pk=pk)
	projs = Project.objects.filter(ptype=ptype).all()
	objects = []
	for i in projs:
		c = Contract.objects.filter(project=i).last()
		a = Amendment.objects.filter(contract__project=i).first()
		p = Payment.objects.filter(contract=c).last()
		objects.append([i,c,a,p])
	years = Project.objects.filter(ptype=ptype).distinct().values('year__year')
	subtitle = f'Tipu {ptype}'
	context = {
		'group': group, 'ptype': ptype, 'objects': objects, 'years': years,
		'subtitle': subtitle, 'title': f'Lista Projetu', 'legend': f'Lista Projetu',
	}
	return render(request, 'report_t/r_ptype_list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPTypeYearList(request, pk, year):
	group = get_roles(request)
	ptype = get_object_or_404(PType, pk=pk)
	projs = Project.objects.filter(ptype=ptype, year__year=year).all()
	objects = []
	for i in projs:
		c = Contract.objects.filter(project=i).last()
		a = Amendment.objects.filter(contract__project=i).first()
		p = Payment.objects.filter(contract=c).last()
		objects.append([i,c,a,p])
	years = Project.objects.filter(ptype=ptype).distinct().values('year__year')
	subtitle = f'Tipu {ptype} Tinan {year}'
	context = {
		'group': group, 'year': year, 'ptype': ptype, 'objects': objects, 'years': years, 'page': 'pyear',
		'subtitle': subtitle, 'title': f'Lista Projetu', 'legend': f'Lista Projetu',
	}
	return render(request, 'report_t/r_ptype_list.html', context)