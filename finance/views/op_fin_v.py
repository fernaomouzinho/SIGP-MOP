import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from users.decorators import allowed_users
from sigp.utils import get_roles
from django.db.models import Sum, Count, Q
from contract.models import Contract
from project.models import Project, ProjectEst
from finance.models import CPV, EV, PO, PRT, TPO, CPVReq, CPVTrack, CPVLetter
from conf.user_utils import c_user_dgaf, c_user_div, c_user_dnof, c_user_min

# CPV
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opCPVProjList(request):
	group = get_roles(request)
	objects = Project.objects.filter().all().order_by('-year','id')
	context = {
		'group': group, 'objects': objects,
		'module_name': 'Modulu CPV', 'title': 'Lista Projetu', 'legend': 'Lista Projetu'
	}
	return render(request, 'finance_op/proj_list.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opCPVList(request, hashid):
	group = get_roles(request)
	proj = get_object_or_404(Project, hashed=hashid)
	objects = CPV.objects.filter(proj=proj).all().order_by('date')
	context = {
		'group': group, 'proj': proj, 'objects': objects,
		'module_name': 'Modulu CPV', 'title': 'Lista CPV', 'legend': 'Lista CPV',
	}
	return render(request, 'finance_op/cpv_list.html', context)
# PO
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opPOContList(request):
	group = get_roles(request)
	objects = Contract.objects.filter().all().order_by('-start_date','id')
	context = {
		'group': group, 'objects': objects, 'page': 'po',
		'module_name': 'Modulu PO', 'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
	}
	return render(request, 'finance_op/cont_list.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opPOList(request, hashid):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	objects = PO.objects.filter(cont=cont).all().order_by('date')
	tot = PO.objects.filter(cont=cont).aggregate(Sum('amount')).get('amount__sum', 0.00)
	context = {
		'group': group, 'cont': cont, 'objects': objects, 'tot': tot,
		'module_name': 'Modulu PO', 'title': 'Lista PO', 'legend': 'Lista PO',
	}
	return render(request, 'finance_op/po_list.html', context)
# PRT
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opPRTContList(request):
	group = get_roles(request)
	objects = Contract.objects.filter().all().order_by('-start_date','id')
	context = {
		'group': group, 'objects': objects, 'page': 'prt',
		'module_name': 'Modulu PRT', 'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
	}
	return render(request, 'finance_op/cont_list.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opPRTList(request, hashid):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	objects = PRT.objects.filter(cont=cont).all().order_by('date')
	tot = PRT.objects.filter(cont=cont).aggregate(Sum('total')).get('total__sum', 0.00)
	context = {
		'group': group, 'cont': cont, 'objects': objects, 'tot': tot,
		'module_name': 'Modulu PRT', 'title': 'Lista PRT', 'legend': 'Lista PRT',
	}
	return render(request, 'finance_op/prt_list.html', context)
# EV
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opEVContList(request):
	group = get_roles(request)
	objects = Contract.objects.filter().all().order_by('-start_date','id')
	context = {
		'group': group, 'objects': objects, 'page': 'ev',
		'module_name': 'Modulu EV', 'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
	}
	return render(request, 'finance_op/cont_list.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opEVList(request, hashid):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	objects = EV.objects.filter(cont=cont).all().order_by('date')
	context = {
		'group': group, 'cont': cont, 'objects': objects,
		'module_name': 'Modulu EV', 'title': 'Lista EV', 'legend': 'Lista EV',
	}
	return render(request, 'finance_op/ev_list.html', context)
# TPO
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opTPOContList(request):
	group = get_roles(request)
	objects = Contract.objects.filter().all().order_by('-start_date','id')
	context = {
		'group': group, 'objects': objects, 'page': 'tpo',
		'module_name': 'Modulu TPO', 'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
	}
	return render(request, 'finance_op/cont_list.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opTPOList(request, hashid):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	objects = TPO.objects.filter(cont=cont).all().order_by('date')
	context = {
		'group': group, 'cont': cont, 'objects': objects,
		'module_name': 'Modulu TPO', 'title': 'Lista TPO', 'legend': 'Lista TPO',
	}
	return render(request, 'finance_op/tpo_list.html', context)