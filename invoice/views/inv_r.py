from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from contract.models import ContractComp
from invoice.models import Invoice, InvTrack, CertPay, PayRecom, InvLet
from finance.models import CPV, PO, PRT, EV
from ver.models import Ver
from users.decorators import allowed_users
from sigp.utils import get_roles

# all
@login_required
def allInvList(request):
	group = get_roles(request)
	objects = Invoice.objects.filter(is_end=False).all().order_by('-date')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Resibu', 'legend': 'Historia Resibu',
	}
	return render(request, 'invoice_r/all_list.html', context)

@login_required
def allInvDet(request, hashid):
	group = get_roles(request)
	inv = get_object_or_404(Invoice, hashed=hashid)
	cont = inv.cont
	proj = cont.project
	vers = Ver.objects.filter(inv=inv).all()
	track = InvTrack.objects.filter(inv=inv).first()
	certpays = CertPay.objects.filter(inv=inv).all()
	recoms = PayRecom.objects.filter(inv=inv).all()
	cpv = CPV.objects.filter(proj=proj, is_end=True).last()
	po = PO.objects.filter(inv=inv, is_end=True).first()
	prt = PRT.objects.filter(inv=inv).first()
	ev = EV.objects.filter(prt=prt).first()
	lets = InvLet.objects.filter(inv=inv).all()
	contcomp = ContractComp.objects.filter(contract=cont).first()
	context = {
		'group':group, 'inv':inv, 'cont':inv.cont, 'certpays':certpays, 'recoms':recoms,'contcomp':contcomp,
		'track':track, 'cpv':cpv, 'po':po, 'prt':prt, 'ev':ev, 'lets':lets,
		'title': 'Detallu Resibu', 'legend': 'Detallu Resibu'
	}
	return render(request, 'invoice_r/all_det.html', context)
# hist
@login_required
def histInvList(request):
	group = get_roles(request)
	objects = Invoice.objects.filter(is_end=True).all()
	years = Invoice.objects.filter(is_end=True).distinct().values('date__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': 'Lista Resibu', 'legend': 'Lista Resibu',
	}
	return render(request, 'invoice_r/hist_list.html', context)

@login_required
def histInvYear(request, year):
	group = get_roles(request)
	objects = Invoice.objects.filter(is_end=True, date__year=year).all()
	years = Invoice.objects.filter(is_end=True).distinct().values('date__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Lista Resibu Tinan {year}', 'legend': f'Lista Resibu Tinan {year}',
	}
	return render(request, 'invoice_r/inv_hist_list.html', context)

@login_required
def histInvDet(request, hashid):
	group = get_roles(request)
	inv = get_object_or_404(Invoice, hashed=hashid)
	proj = inv.proj
	track = InvTrack.objects.filter(inv=inv).first()
	certpays = CertPay.objects.filter(inv=inv).all()
	recoms = PayRecom.objects.filter(inv=inv).all()
	cpv = CPV.objects.filter(project=proj).last()
	po = PO.objects.filter(project=proj, invoice=inv).first()
	prt = PRT.objects.filter(invoice=inv).first()
	ev = EV.objects.filter(invoice=inv).first()
	objects = InvLet.objects.filter(inv=inv).all()
	context = {
		'group':group, 'inv':inv, 'cont':inv.cont, 'certpays':certpays, 'recoms':recoms,
		'track':track, 'cpv':cpv, 'po':po, 'prt':prt, 'ev':ev, 'objects':objects,
		'title': 'Detallu Resibu', 'legend': 'Detallu Resibu'
	}
	return render(request, 'invoice_r/hist_det.html', context)
