from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from custom.models import Division
from project.models import Project, ProjectLoc
from contract.models import Contract, ContractYear, Amendment, ContractComp
from invoice.models import PayRecom
from payment.models import Payment
from contract.models import Amendment, ContractComp
from proc.models import Proc
from finance.models import CPV, PRT, TPO
from users.decorators import allowed_users
from sigp.utils import get_roles


def rdivRawData(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	conts = ContractYear.objects.filter(contract__project__owner=div).all().order_by('-contract__start_date__year')
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
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'objects': objects,
		'subtitle': subtitle, 'title': 'Raw Data', 'legend': 'Raw Data'
	}
	return render(request, 'reportdiv_raw_data/raw_data.html', context)


def rdivRawDataCPV(request, pk, hashid):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	proj = get_object_or_404(Project, hashed=hashid)
	objects = CPV.objects.filter(project=proj).all()
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'proj': proj, 'objects': objects,
		'subtitle': subtitle, 'title': 'Lista CPV', 'legend': 'Lista CPV'
	}
	return render(request, 'reportdiv_raw_data/cpv_list.html', context)


def rdivRawDataPRT(request, pk, hashid):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	cont = get_object_or_404(Contract, hashed=hashid)
	proj = cont.project
	amend = Amendment.objects.get(contract=cont)
	comps = ContractComp.objects.filter(contract=cont).all()
	objects = PRT.objects.filter(contract=cont).all()
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'proj': proj, 'cont': cont, 'amend': amend, 'comps': comps, 'objects': objects,
		'subtitle': subtitle, 'title': 'Lista PRT', 'legend': 'Lista PRT'
	}
	return render(request, 'reportdiv_raw_data/prt_list.html', context)


def rdivRawDataRecom(request, pk, hashid):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	cont = get_object_or_404(Contract, hashed=hashid)
	proj = cont.project
	amend = Amendment.objects.get(contract=cont)
	comps = ContractComp.objects.filter(contract=cont).all()
	objects = PayRecom.objects.filter(contract=cont).all()
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'proj': proj, 'cont': cont, 'amend': amend, 'comps': comps, 'objects': objects,
		'subtitle': subtitle, 'title': 'Lista Rekomendasaun Pagamentu', 'legend': 'Lista Rekomendasaun Pagamentu'
	}
	return render(request, 'reportdiv_raw_data/recom_list.html', context)


def rdivRawDataTPO(request, pk, hashid):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	cont = get_object_or_404(Contract, hashed=hashid)
	proj = cont.project
	amend = Amendment.objects.get(contract=cont)
	comps = ContractComp.objects.filter(contract=cont).all()
	objects = TPO.objects.filter(contract=cont).all()
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'proj': proj, 'cont': cont, 'amend': amend, 'comps': comps, 'objects': objects,
		'subtitle': subtitle, 'title': 'Lista TPO', 'legend': 'Lista TPO'
	}
	return render(request, 'reportdiv_raw_data/tpo_list.html', context)