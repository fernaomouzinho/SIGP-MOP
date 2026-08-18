from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.db.models import Q
from project.models import Project, ProjectEst
from contract.models import Contract, ContractComp, Amendment
from invoice.models import Invoice, InvTrack, CertPay, PayRecom, InvLet, InvLetAdnBack
from finance.models import CPV, PO, PRT, EV
from insp.models import Insp
from conf.user_utils import c_user_sup, c_user_dg, c_user_dgaf, c_user_div, c_user_dna, c_user_dnof, c_user_min,\
    c_user_uvip
from users.decorators import allowed_users
from sigp.utils import get_roles

### SUP
@login_required
@allowed_users(allowed_roles=['sigp_sup','sigp_admin'])
def supInvContList(request):
    group = get_roles(request)
    mun = c_user_sup(request.user)
    if group == "sup":
        objects = Contract.objects.filter(project__projectloc__municipality=mun).all().order_by("-id")
        contcomp = ContractComp.objects.filter().all()
    else:
        objects = Contract.objects.all().order_by("-id")
        contcomp = ContractComp.objects.filter().all()
    context = {
        'group': group, 'mun': mun, 'objects': objects,'contcomp': contcomp,
        'title': 'Lista Kontratu', 'legend': 'Lista Kontratu'
    }
    return render(request, 'invoice/sup_cont_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_sup','sigp_admin'])
def supInvList(request, hashid):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    amend = Amendment.objects.filter(contract=cont).first()
    comps = ContractComp.objects.filter(contract=cont).all()
    invs = Invoice.objects.filter(cont=cont).all()
    context = {
        'group': group, 'cont': cont, 'amend': amend, 'comps': comps, 'invs': invs,
        'title': 'Lista Resibu', 'legend': 'Lista Resibu',
    }
    return render(request, 'invoice/sup_inv_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_sup','sigp_admin'])
def supInvDet(request, hashid):
    group = get_roles(request)
    mun = c_user_sup(request.user)
    inv = get_object_or_404(Invoice, hashed=hashid)
    track = InvTrack.objects.filter(inv=inv).first()
    invlets = InvLet.objects.filter(inv=inv, mun=mun).all()
    contcomp = ContractComp.objects.filter(contract=inv.cont).first()
    context = {
        'group': group, 'inv': inv, 'cont': inv.cont,
        'track': track, 'invlets': invlets,'contcomp':contcomp,
        'title': 'Detallu Resibu', 'legend': 'Detallu Resibu'
    }
    return render(request, 'invoice/sup_inv_det.html', context)
### UIVP
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_uivp'])
def uvipInvList(request):
    group = get_roles(request)
    objects = Invoice.objects.filter(is_end=False).all().order_by('-date')
    contcomp = ContractComp.objects.filter().all()
    context = {
        'group': group, 'objects': objects, 'contcomp': contcomp,
        'title': 'Lista Resibu', 'legend': 'Lista Resibu',
    }
    return render(request, 'invoice/uvip_inv_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_uivp'])
def uvipInvDet(request, hashid):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    proj = cont.project
    contcomp = ContractComp.objects.filter(contract=cont).first()
    projest = ProjectEst.objects.filter(project=proj).first()
    insp = Insp.objects.filter(inv=inv).all()
    track = InvTrack.objects.filter(inv=inv).first()
    certpays = CertPay.objects.filter(inv=inv).all()
    recoms = PayRecom.objects.filter(inv=inv).all()
    cpv = CPV.objects.filter(proj=proj, is_end=True).last()
    po = PO.objects.filter(inv=inv, is_end=True).first()
    prt = PRT.objects.filter(inv=inv).first()
    ev = EV.objects.filter(prt=prt).first()
    lets = InvLet.objects.filter((Q(is_uvip=True)|Q(is_sup=True)), inv=inv).all()
    letsadnback = InvLetAdnBack.objects.all()
    context = {
        'group':group, 'inv':inv, 'cont':inv.cont, 'certpays':certpays, 'recoms':recoms,
        'track':track, 'insp':insp, 'cpv':cpv, 'po':po, 'prt':prt, 'ev':ev, 'lets':lets, 'letsadnback':letsadnback,
        'p1':1, 'p2':2, 'p3':3, 'projest':projest,'contcomp':contcomp,
        'title': 'Detallu Resibu', 'legend': 'Detallu Resibu'
    }
    return render(request, 'invoice/uvip_inv_det.html', context)
### GAB
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_gabm'])
def gabInvList(request):
    group = get_roles(request)
    objects = Invoice.objects.filter(is_end=False).all().order_by('-date')
    contcomp = ContractComp.objects.filter().all()
    context = {
        'group': group, 'objects': objects,'contcomp': contcomp,
        'title': 'Lista Resibu Ativu', 'legend': 'Lista Resibu Ativu',
    }
    return render(request, 'invoice/gab_inv_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_gabm'])
def gabInvDet(request, hashid):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    proj = cont.project
    insp = Insp.objects.filter(inv=inv).all()
    track = InvTrack.objects.filter(inv=inv).first()
    certpays = CertPay.objects.filter(inv=inv).all()
    recoms = PayRecom.objects.filter(inv=inv).all()
    cpv = CPV.objects.filter(proj=proj, is_end=True).last()
    po = PO.objects.filter(inv=inv, is_end=True).first()
    prt = PRT.objects.filter(inv=inv).first()
    ev = EV.objects.filter(prt=prt).first()
    lets = InvLet.objects.filter((Q(is_gab=True)|Q(is_uvip=True)),inv=inv).all()
    context = {
        'group':group, 'inv':inv, 'cont':inv.cont, 'certpays':certpays, 'recoms':recoms,
        'track':track, 'insp':insp, 'cpv':cpv, 'po':po, 'prt':prt, 'ev':ev, 'lets':lets,
        'title': 'Detallu Resibu', 'legend': 'Detallu Resibu'
    }
    return render(request, 'invoice/gab_inv_det.html', context)
### DGAF
@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafInvList(request):
    group = get_roles(request)
    objects = Invoice.objects.filter(is_end=False).all().order_by('-date')
    contcomp = ContractComp.objects.filter().all()
    context = {
        'group': group, 'objects': objects,'contcomp': contcomp,
        'title': 'Lista Resibu Ativu', 'legend': 'Lista Resibu Ativu',
    }
    return render(request, 'invoice/dgaf_inv_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafInvDet(request, hashid):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    proj = cont.project
    insp = Insp.objects.filter(inv=inv).all()
    track = InvTrack.objects.filter(inv=inv).first()
    certpays = CertPay.objects.filter(inv=inv).all()
    recoms = PayRecom.objects.filter(inv=inv).all()
    cpv = CPV.objects.filter(proj=proj, is_end=True).last()
    po = PO.objects.filter(inv=inv, is_end=True).first()
    prt = PRT.objects.filter(inv=inv).first()
    ev = EV.objects.filter(prt=prt).first()
    lets = InvLet.objects.filter((Q(is_dgaf=True)|Q(is_gab=True)), inv=inv).all()
    context = {
        'group':group, 'inv':inv, 'cont':inv.cont, 'certpays':certpays, 'recoms':recoms,
        'track':track, 'insp':insp, 'cpv':cpv, 'po':po, 'prt':prt, 'ev':ev, 'lets':lets,
        'title':'Detallu Resibu', 'legend':'Detallu Resibu'
    }
    return render(request, 'invoice/dgaf_inv_det.html', context)
### DNA
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_admin'])
def dnaInvList(request):
    group = get_roles(request)
    objects = Invoice.objects.filter(is_end=False).all().order_by('-date')
    contcomp = ContractComp.objects.filter().all()
    context = {
        'group': group, 'objects': objects,'contcomp': contcomp,
        'title': 'Lista Resibu', 'legend': 'Lista Resibu',
    }
    return render(request, 'invoice/dna_inv_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_admin'])
def dnaInvDet(request, hashid):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    proj = cont.project
    insp = Insp.objects.filter(inv=inv).all()
    track = InvTrack.objects.filter(inv=inv).first()
    certpays = CertPay.objects.filter(inv=inv).all()
    recoms = PayRecom.objects.filter(inv=inv).all()
    cpv = CPV.objects.filter(proj=proj, is_end=True).last()
    po = PO.objects.filter(inv=inv, is_end=True).first()
    prt = PRT.objects.filter(inv=inv).first()
    ev = EV.objects.filter(prt=prt).first()
    lets = InvLet.objects.filter((Q(to_id=1))|Q(is_dna=True), inv=inv).all()
    context = {
        'group':group, 'inv':inv, 'cont':inv.cont, 'insp':insp, 'certpays':certpays, 'recoms':recoms,
        'track':track, 'cpv':cpv, 'po':po, 'prt':prt, 'ev':ev, 'lets':lets,
        'title': 'Detallu Resibu', 'legend': 'Detallu Resibu'
    }
    return render(request, 'invoice/dna_inv_det.html', context)
### DNOF
@login_required
@allowed_users(allowed_roles=['sigp_dnof','sigp_dnof_bo','sigp_admin'])
def dnofInvList(request):
    group = get_roles(request)
    objects = Invoice.objects.filter(is_end=False).all().order_by('-date')
    contcomp = ContractComp.objects.filter().all()
    context = {
        'group': group, 'objects': objects,'contcomp': contcomp,
        'title': 'Lista Resibu', 'legend': 'Lista Resibu',
    }
    return render(request, 'invoice/dnof_inv_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dnof','sigp_admin'])
def dnofInvDet(request, hashid):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    proj = cont.project
    insp = Insp.objects.filter(inv=inv).all()
    track = InvTrack.objects.filter(inv=inv).first()
    certpays = CertPay.objects.filter(inv=inv).all()
    recoms = PayRecom.objects.filter(inv=inv).all()
    cpv = CPV.objects.filter(proj=proj, is_end=True).last()
    po = PO.objects.filter(inv=inv, is_end=True).first()
    prt = PRT.objects.filter(inv=inv).first()
    ev = EV.objects.filter(prt=prt).first()
    lets = InvLet.objects.filter((Q(is_dnof=True)|Q(is_dna=True)), inv=inv).all()
    context = {
        'group':group, 'inv':inv, 'cont':inv.cont, 'certpays':certpays, 'recoms':recoms,
        'track':track, 'cpv':cpv, 'po':po, 'prt':prt, 'ev':ev, 'lets':lets, 'insp':insp,
        'title':'Detallu Resibu', 'legend':'Detallu Resibu'
    }
    return render(request, 'invoice/dnof_inv_det.html', context)