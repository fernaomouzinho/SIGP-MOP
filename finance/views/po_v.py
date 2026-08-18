from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from conf.decorators import allowed_users
from project.models import Project, ProjectEst
from contract.models import Contract, ContractComp
from finance.models import CPV, PO, POTrack, POLetter
from conf.user_utils import c_user_dna, c_user_dgaf

@login_required
@allowed_users(allowed_roles=['dna'])
def dnaPOProjList(request):
	group = request.user.groups.all()[0].name
	objects = Project.objects.filter().all().order_by("-year","id")
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Projetu', 'legend': 'Lista Projetu'
	}
	return render(request, 'finance_po/dna_proj_list.html', context)

@login_required
@allowed_users(allowed_roles=['dna'])
def dnaPOContList(request, hashid):
	group = request.user.groups.all()[0].name
	proj = get_object_or_404(Project, hashed=hashid)
	conts = Contract.objects.filter(project=proj).all().order_by("-id")
	objects = []
	for i in conts:
		a = ContractComp.objects.filter(contract=i).all()
		objects.append([i,a])
	context = {
		'group': group, 'proj': proj, 'objects': objects, 
		'title': 'Kontratu', 'legend': 'Kontratu'
	}
	return render(request, 'finance_po/dna_cont_list.html', context)

@login_required
@allowed_users(allowed_roles=['dna'])
def dnaPOList(request, hashid):
	group = request.user.groups.all()[0].name
	cont = get_object_or_404(Contract, hashed=hashid)
	proj = cont.project
	comps = ContractComp.objects.filter(contract=cont).all()
	cpvs = CPV.objects.filter(proj=proj, is_end=True).all()
	objects = PO.objects.filter(cont=cont).all().order_by('-date')
	context = {
		'group':group, 'proj':proj, 'cont':cont, 'comps':comps, 'cpvs':cpvs, 'objects':objects,
		'title': 'Lista PO', 'legend': 'Lista PO',
	}
	return render(request, 'finance_po/dna_po_list.html', context)

@login_required
@allowed_users(allowed_roles=['dna'])
def dnaPODet(request, hashid):
	group = request.user.groups.all()[0].name
	po = get_object_or_404(PO, hashed=hashid)
	cont = po.cont
	proj = cont.project
	projest = ProjectEst.objects.filter(project=proj).first()
	polet = POLetter.objects.filter(po=po).first()
	track = POTrack.objects.filter(po=po).first()
	context = {
		'group': group, 'po':po, 'cont':cont, 'proj':proj, 'projest':projest, 'polet':polet, 'track':track,
		'title': 'Detallu PO', 'legend': 'Detallu PO',
	}
	return render(request, 'finance_po/dna_po_det.html', context)
# dgaf
@login_required
@allowed_users(allowed_roles=['dgaf'])
def dgafPOProjList(request):
	group = request.user.groups.all()[0].name
	objects = Project.objects.filter().all().order_by("-year","id")
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Projetu', 'legend': 'Lista Projetu'
	}
	return render(request, 'finance_po/dgaf_proj_list.html', context)

@login_required
@allowed_users(allowed_roles=['dgaf'])
def dgafPOContList(request, hashid):
	group = request.user.groups.all()[0].name
	proj = get_object_or_404(Project, hashed=hashid)
	conts = Contract.objects.filter(project=proj).all().order_by("-id")
	objects = []
	for i in conts:
		a = ContractComp.objects.filter(contract=i).all()
		objects.append([i,a])
	context = {
		'group': group, 'proj': proj, 'objects': objects, 
		'title': 'Kontratu', 'legend': 'Kontratu'
	}
	return render(request, 'finance_po/dgaf_cont_list.html', context)

@login_required
@allowed_users(allowed_roles=['dgaf'])
def dgafPOList(request, hashid):
	group = request.user.groups.all()[0].name
	cont = get_object_or_404(Contract, hashed=hashid)
	proj = cont.project
	comps = ContractComp.objects.filter(contract=cont).all()
	cpvs = CPV.objects.filter(proj=proj, is_end=True).all()
	objects = PO.objects.filter(cont=cont).all().order_by('-date')
	context = {
		'group':group, 'proj':proj, 'cont':cont, 'comps':comps, 'cpvs':cpvs, 'objects':objects,
		'title': 'Lista PO', 'legend': 'Lista PO',
	}
	return render(request, 'finance_po/dgaf_po_list.html', context)

@login_required
@allowed_users(allowed_roles=['dgaf'])
def dgafPODet(request, hashid):
	group = request.user.groups.all()[0].name
	po = get_object_or_404(PO, hashed=hashid)
	cont = po.cont
	proj = cont.project
	projest = ProjectEst.objects.filter(project=proj).first()
	track = POTrack.objects.filter(po=po).first()
	lett = POLetter.objects.filter(po=po).first()
	context = {
		'group': group, 'po':po, 'cont':cont, 'proj':proj, 'projest':projest, 'track':track, 'lett':lett,
		'title': 'Detallu PO', 'legend': 'Detallu PO',
	}
	return render(request, 'finance_po/dgaf_po_det.html', context)
# gab
@login_required
@allowed_users(allowed_roles=['gab','upiv','dnof'])
def gabPOProjList(request):
	group = request.user.groups.all()[0].name
	objects = Project.objects.filter().all().order_by("-year","id")
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Projetu', 'legend': 'Lista Projetu'
	}
	return render(request, 'finance_po/gab_proj_list.html', context)

@login_required
@allowed_users(allowed_roles=['gab','upiv','dnof'])
def gabPOContList(request, hashid):
	group = request.user.groups.all()[0].name
	proj = get_object_or_404(Project, hashed=hashid)
	conts = Contract.objects.filter(project=proj).all().order_by("-id")
	objects = []
	for i in conts:
		a = ContractComp.objects.filter(contract=i).all()
		objects.append([i,a])
	context = {
		'group': group, 'proj': proj, 'objects': objects, 
		'title': 'Kontratu', 'legend': 'Kontratu'
	}
	return render(request, 'finance_po/gab_cont_list.html', context)

@login_required
@allowed_users(allowed_roles=['gab','upiv','dnof'])
def gabPOList(request, hashid):
	group = request.user.groups.all()[0].name
	cont = get_object_or_404(Contract, hashed=hashid)
	proj = cont.project
	comps = ContractComp.objects.filter(contract=cont).all()
	cpvs = CPV.objects.filter(proj=proj, is_end=True).all()
	objects = PO.objects.filter(cont=cont).all().order_by('-date')
	context = {
		'group':group, 'proj':proj, 'cont':cont, 'comps':comps, 'cpvs':cpvs, 'objects':objects,
		'title': 'Lista PO', 'legend': 'Lista PO',
	}
	return render(request, 'finance_po/gab_po_list.html', context)

@login_required
@allowed_users(allowed_roles=['gab','upiv','dnof'])
def gabPODet(request, hashid):
	group = request.user.groups.all()[0].name
	po = get_object_or_404(PO, hashed=hashid)
	cont = po.cont
	proj = cont.project
	projest = ProjectEst.objects.filter(project=proj).first()
	track = POTrack.objects.filter(po=po).first()
	lett = POLetter.objects.filter(po=po).first()
	context = {
		'group': group, 'po':po, 'cont':cont, 'proj':proj, 'projest':projest, 'track':track, 'lett':lett,
		'title': 'Detallu PO', 'legend': 'Detallu PO',
	}
	return render(request, 'finance_po/gab_po_det.html', context)
#