import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from contract.models import Contract
from invoice.models import Invoice, InvLet, InvTrack
from users.decorators import allowed_users
from sigp.utils import get_roles


@allowed_users(allowed_roles=['sigp_admin','sigp_dna'])
def letContList(request):
	group = get_roles(request)
	objects = Contract.objects.filter().all().order_by('-start_date','id')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
	}
	return render(request, 'inv_let/cont_list.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna'])
def letInvList(request, hashid):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	objects = Invoice.objects.filter(cont=cont).all().order_by('-date','-id')
	context = {
		'group': group, 'objects': objects, 'cont': cont, 'proj': cont.project,
		'title': 'Lista Resibu', 'legend': 'Lista Resibu'
	}
	return render(request, 'inv_let/inv_list.html', context)

@allowed_users(allowed_roles=['sigp_admin','sigp_dna'])
def letInvLetList(request, hashid):
	group = get_roles(request)
	inv = get_object_or_404(Invoice, hashed=hashid)
	objects = InvLet.objects.filter(inv=inv).all().order_by('-date')
	context = {
		'group': group, 'inv': inv, 'cont':inv.cont, 'objects': objects,
		'title': 'Karta Relevantes', 'legend': 'Karta Relevantes'
	}
	return render(request, 'inv_let/let_list.html', context)
