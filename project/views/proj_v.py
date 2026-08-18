import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from custom.models import Year
from project.models import Project, ProjectLoc, ProjectEst
from users.decorators import allowed_users
from sigp.utils import get_roles
from conf.user_utils import c_user_div, c_user_dna, c_user_dnof, c_user_sup

@allowed_users(allowed_roles=['sigp_admin'])
def ProjList(request):
	group = get_roles(request)
	if group == "div":
		div = c_user_div(request.user)
		objects = Project.objects.filter(owner=div).all().order_by("-year",'id')
	else:
		objects = Project.objects.all().order_by("-year",'id')
	years = Project.objects.filter().distinct().values('year__year').all().order_by('year__year')
	context = {
		'group': group, 'objects': objects, 'years': years,
		'module_name': 'Modulu Projetu', 'title': 'Lista Projetu', 'legend': 'Lista Projetu'
	}
	return render(request, 'project/list.html', context)

@allowed_users(allowed_roles=['sigp_admin'])
def ProjDetail(request, hashid):
	group = get_roles(request)
	proj = get_object_or_404(Project, hashed=hashid)
	loc = ProjectLoc.objects.filter(project=proj).first()
	est = ProjectEst.objects.filter(project=proj).first()
	context = {
		'group': group, 'proj': proj, 'loc': loc, 'est': est,
		'title': 'Detallu Projetu', 'legend': 'Detallu Projetu',
	}
	return render(request, 'project/detail.html', context)


# div
@allowed_users(allowed_roles=['sigp_div','sigp_dna','sigp_dnof'])
def divProjDetail(request, hashid):
	group = get_roles(request)
	if 'sigp_div' in group: div = c_user_div(request.user)
	elif 'sigp_dna' in group: div = c_user_dna(request.user)
	elif 'sigp_dnof' in group: div = c_user_dnof(request.user)
	proj = get_object_or_404(Project, hashed=hashid)
	loc = ProjectLoc.objects.filter(project=proj).first()
	est = ProjectEst.objects.filter(project=proj).first()
	context = {
		'group': group, 'div': div, 'proj': proj, 'loc': loc, 'est': est, 'page': 'pdet',
		'title': 'Detallu Projetu', 'legend': 'Detallu Projetu',
	}
	return render(request, 'project/div_detail.html', context)
#
@allowed_users(allowed_roles=['sigp_admin'])
def ProjYearAll(request):
	group = get_roles(request)
	objects = Project.objects.filter().all().order_by("-year","id")
	years = Project.objects.filter().distinct().values('year__year').all().order_by('year__year')
	context = {
		'group': group, 'objects': objects, 'years': years,
		'module_name': 'Modulu Projetu', 'title': f'Lista Projetu', 'legend': f'Lista Projetu'
	}
	return render(request, 'project/list_year.html', context)

@allowed_users(allowed_roles=['sigp_admin'])
def ProjYearList(request, year):
	group = get_roles(request)
	objects = Project.objects.filter(year__year=year).all().order_by("-year","id")
	years = Project.objects.filter().distinct().values('year__year').all().order_by('year__year')
	context = {
		'group': group, 'objects': objects, 'years': years,
		'module_name': 'Modulu Projetu', 'title': f'Lista Projetu Tinan {year}', 'legend': f'Lista Projetu Tinan {year}'
	}
	return render(request, 'project/list_year.html', context)
#
@allowed_users(allowed_roles=['sigp_admin'])
def ProjLocList(request):
	group = get_roles(request)
	objects = ProjectLoc.objects.filter().all().order_by("project__name")
	context = {
		'group': group, 'objects': objects,
		'module_name': 'Modulu Projetu', 'title': f'Localizasaun Projetu', 'legend': f'Localizasaun Projetu'
	}
	return render(request, 'project/list_loc.html', context)
###
@allowed_users(allowed_roles=['sigp_admin'])
def supProjList(request):
	group = get_roles(request)
	mun = c_user_sup(request.user)
	objects = Project.objects.filter(projectloc__municipality=mun).all().order_by("-year",'id')
	context = {
		'group': group, 'objects': objects,
		'module_name': 'Modulu Projetu', 'title': f'Lista Projetu Municipiu {mun}', 'legend': f'Lista Projetu Munisipiu {mun}'
	}
	return render(request, 'project/sup_list.html', context)

@allowed_users(allowed_roles=['sigp_sup'])
def supProjDetail(request, hashid):
	group = get_roles(request)
	proj = get_object_or_404(Project, hashed=hashid)
	loc = ProjectLoc.objects.filter(project=proj).first()
	est = ProjectEst.objects.filter(project=proj).first()
	context = {
		'group': group,'proj': proj, 'loc': loc, 'est': est, 'page': 'pdet',
		'title': 'Detallu Projetu', 'legend': 'Detallu Projetu',
	}
	return render(request, 'project/div_detail.html', context)