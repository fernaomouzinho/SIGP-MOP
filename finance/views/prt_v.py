from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles
from contract.models import Contract, ContractComp
from payment.models import Invoice
from finance.models import PO, PRT, EV
from invoice.models import InvTrack
from conf.user_utils import c_user_dna

@allowed_users(allowed_roles=['sig_admin','sig_dna','sig_dnof','sig_dgaf','sig_gab','sig_uivp','sig_min','sig_dnof_bo'])
def PRTContList(request):
	group = get_roles(request)
	dna = c_user_dna(request.user)
	objects = Contract.objects.filter().all().order_by("-start_date","id")
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
	}
	return render(request, 'finance_prt/prt_cont_list.html', context)

@allowed_users(allowed_roles=['sig_admin','sig_dna','sig_dnof','sig_dgaf','sig_gab','sig_uivp','sig_min','sig_dnof_bo'])
def PRTInvList(request, hashid):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	proj = cont.project
	comps = ContractComp.objects.filter(contract=cont).all()
	objects = Invoice.objects.filter(cont=cont).all().order_by('-date')
	context = {
		'group': group, 'proj': proj, 'cont': cont, 'comps': comps, 'objects': objects,
		'title': 'Lista Invoice', 'legend': 'Lista Invoice',
	}
	return render(request, 'finance_prt/prt_inv_list.html', context)

@allowed_users(allowed_roles=['sig_admin','sig_dna','sig_dnof','sig_dgaf','sig_gab','sig_uivp','sig_min','sig_dnof_bo'])
def PRTList(request, hashid):
	group = get_roles(request)
	inv = get_object_or_404(Invoice, hashed=hashid)
	invtrack = InvTrack.objects.get(inv=inv)
	cont = inv.cont
	proj = cont.project
	po = PO.objects.filter(inv=inv).first()
	prt = PRT.objects.get(inv=inv)
	ev = EV.objects.get(prt=prt)
	context = {
		'group': group, 'proj': proj, 'cont': cont, 'inv': inv, 'invtrack':invtrack,'po': po, 'prt': prt, 'ev': ev,
		'title': 'Lista PRT', 'legend': 'Lista PRT',
	}
	return render(request, 'finance_prt/prt_list.html', context)
###