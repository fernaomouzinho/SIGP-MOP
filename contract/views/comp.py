from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from contract.models import Contract, ContractComp, ContractFiles, Amendment, ContractYear
from conf.user_utils import c_user_comp
from users.decorators import allowed_users
from sigp.utils import get_roles


@allowed_users(allowed_roles=['sigp_comp','sigp_admin'])
def compContList(request):
	group = get_roles(request.user)
	comp = c_user_comp(request.user)
	conts = Contract.objects.filter(contractcomp__company=comp).prefetch_related('contractcomp').all().order_by('-start_date','id')
	objects = []
	for i in conts:
		a = Amendment.objects.filter(contract=i).first()
		objects.append([i,a])
	context = {
		'group': group, 'comp':comp, 'objects': objects,
		'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
	}
	return render(request, 'contract_c/list.html', context)


@allowed_users(allowed_roles=['sigp_comp','sigp_admin'])
def compContDet(request, hashid):
	group = get_roles(request.user)
	cont = get_object_or_404(Contract, hashed=hashid)
	proj = cont.project
	powner = proj.owner
	amend = Amendment.objects.filter(contract=cont).first()
	comps = ContractComp.objects.filter(contract=cont).all()
	files = ContractFiles.objects.filter(contract=cont).all()
	contyears = ContractYear.objects.filter(contract=cont).all()
	context = {
		'group': group, 'proj': proj, 'powner': powner, 'cont': cont, 'amend': amend, 'comps': comps,
		'files': files, 'contyears':contyears,
		'title': 'Detalha Kontratu', 'legend': 'Detalha Kontratu'
	}
	return render(request, 'contract_c/det.html', context)