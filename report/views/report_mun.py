from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from custom.models import Municipality, Year
from project.models import Project, ProjectLoc
from contract.models import Contract, Amendment
from payment.models import Payment
from users.decorators import allowed_users
from sigp.utils import get_roles

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPMunSum(request):
	group = get_roles(request)
	muns = Municipality.objects.filter().all()
	years = Year.objects.filter().all()
	objects = []
	for i in years:
		obj = []
		for j in muns:
			j_a = ProjectLoc.objects.filter(municipality=j, project__year=i).all().count()
			obj.append([j,j_a])
		objects.append([i,obj])
	context = {
		'group': group, 'muns': muns, 'objects': objects,
		'title': f'Lista Projetu Tuir Municipiu', 'legend': f'Lista Projetu Tuir Municipiu',
	}
	return render(request, 'report_t/r_mun_sum.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPMunList(request, pk):
	group = get_roles(request)
	mun = get_object_or_404(Municipality, pk=pk)
	projs = Project.objects.filter(projectloc__municipality=mun).all()
	objects = []
	for i in projs:
		c = Contract.objects.filter(project=i).last()
		a = Amendment.objects.filter(contract__project=i).first()
		p = Payment.objects.filter(contract=c).last()
		objects.append([i,c,a,p])
	years = Project.objects.filter(projectloc__municipality=mun).distinct().values('year__year')
	subtitle = f'Municipiu {mun}'
	context = {
		'group': group, 'mun': mun, 'objects': objects, 'years': years,
		'subtitle': subtitle, 'title': f'Lista Projetu', 'legend': f'Lista Projetu',
	}
	return render(request, 'report_t/r_mun_list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPMunYearList(request, pk, year):
	group = get_roles(request)
	mun = get_object_or_404(Municipality, pk=pk)
	projs = Project.objects.filter(projectloc__municipality=mun, year__year=year).all()
	objects = []
	for i in projs:
		c = Contract.objects.filter(project=i).last()
		a = Amendment.objects.filter(contract__project=i).first()
		p = Payment.objects.filter(contract=c).last()
		objects.append([i,c,a,p])
	years = Project.objects.filter(projectloc__municipality=mun).distinct().values('year__year')
	subtitle = f'Municipiu {mun} Tinan {year}'
	context = {
		'group': group, 'mun': mun, 'objects': objects, 'years': years,
		'subtitle': subtitle, 'title': f'Lista Projetu', 'legend': f'Lista Projetu',
	}
	return render(request, 'report_t/r_mun_list.html', context)