from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles
from project.models import Project, ProjectLoc
from contract.models import Contract, ContractYear, Amendment, ContractComp
from invoice.models import PayRecom
from payment.models import Payment
from contract.models import Amendment, ContractComp
from proc.models import Proc
from finance.models import CPV, PRT, TPO

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rRawData(request):
	group = get_roles(request)
	conts = ContractYear.objects.filter().all().order_by('-contract__start_date__year')
	objects = []
	for i in conts:
		cont = i.contract
		proj = cont.project
		projloc = ProjectLoc.objects.filter(project=proj).first()
		amend = Amendment.objects.get(contract=cont)
		comps = ContractComp.objects.filter(contract=cont).all()
		proc = Proc.objects.filter(project=proj).last()
		cpv = CPV.objects.filter(project=proj).last()
		recom = PayRecom.objects.filter(contract=cont).last()
		prt = PRT.objects.filter(contract=cont).last()
		tpo = TPO.objects.filter(contract=cont).last()
		pay = Payment.objects.filter(contyear=i).last()
		objects.append([proj,projloc,cont,comps,amend,proc,cpv,recom,prt,tpo,pay,i])
	context = {
		'group': group, 'objects': objects,
		'title': 'Raw Data', 'legend': 'Raw Data'
	}
	return render(request, 'report_raw_data/raw_data.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rRawDataCPV(request, hashid):
	group = get_roles(request)
	proj = get_object_or_404(Project, hashed=hashid)
	objects = CPV.objects.filter(project=proj).all()
	context = {
		'group': group, 'proj': proj, 'objects': objects,
		'title': 'Lista CPV', 'legend': 'Lista CPV'
	}
	return render(request, 'report_raw_data/cpv_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rRawDataPRT(request, hashid):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	proj = cont.project
	amend = Amendment.objects.get(contract=cont)
	comps = ContractComp.objects.filter(contract=cont).all()
	objects = PRT.objects.filter(contract=cont).all()
	context = {
		'group': group, 'proj': proj, 'cont': cont, 'amend': amend, 'comps': comps, 'objects': objects,
		'title': 'Lista PRT', 'legend': 'Lista PRT'
	}
	return render(request, 'report_raw_data/prt_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rRawDataRecom(request, hashid):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	proj = cont.project
	amend = Amendment.objects.get(contract=cont)
	comps = ContractComp.objects.filter(contract=cont).all()
	objects = PayRecom.objects.filter(contract=cont).all()
	context = {
		'group': group, 'proj': proj, 'cont': cont, 'amend': amend, 'comps': comps, 'objects': objects,
		'title': 'Lista Rekomendasaun Pagamentu', 'legend': 'Lista Rekomendasaun Pagamentu'
	}
	return render(request, 'report_raw_data/recom_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rRawDataTPO(request, hashid):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	proj = cont.project
	amend = Amendment.objects.get(contract=cont)
	comps = ContractComp.objects.filter(contract=cont).all()
	objects = TPO.objects.filter(contract=cont).all()
	context = {
		'group': group, 'proj': proj, 'cont': cont, 'amend': amend, 'comps': comps, 'objects': objects,
		'title': 'Lista TPO', 'legend': 'Lista TPO'
	}
	return render(request, 'report_raw_data/tpo_list.html', context)