import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conf.decorators import allowed_users
from contract.models import Contract, Amendment, ContractComp
from invoice.models import Invoice, InvTrack
from invoice.forms import InvForm
from conf.user_utils import c_user_sup
from conf.utils import getnewid, split_string
from users.decorators import allowed_users
from sigp.utils import get_roles

@allowed_users(allowed_roles=['sigp_sup','sigp_bd'])
def supInvAdd(request, hashid):
    mun = c_user_sup(request.user)
    cont = get_object_or_404(Contract, hashed=hashid)
    contcomp = ContractComp.objects.filter(contract=cont).first()
    amend = Amendment.objects.filter(contract=cont).first()
    if request.method == 'POST':
        newid, new_hashid = getnewid(Invoice)
        form = InvForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.cont = cont
            instance.proj = cont.project
            instance.mun = mun
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Aumenta succesu.')
            return redirect('sup-inv-list', hashid=hashid)
    else: form = InvForm()
    context = {
        'cont': cont, 'amend': amend, 'contcomp':contcomp,'form': form, 'page': 'inv',
        'title': 'Kria Resibu', 'legend': 'Kria Resibu'
    }
    return render(request, 'invoice/form.html', context)

@allowed_users(allowed_roles=['sigp_sup','sigp_bd'])
def supInvEdit(request, hashid, hashid2):
    cont = get_object_or_404(Contract, hashed=hashid)
    amend = Amendment.objects.filter(contract=cont).first()
    obj = get_object_or_404(Invoice, hashed=hashid2)
    if request.method == 'POST':
        form = InvForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera succesu.')
            return redirect('sup-inv-list', hashid=hashid)
    else: form = InvForm(instance=obj)
    context = {
        'cont': cont, 'amend':amend, 'form': form,
        'title': 'Altera Resibu', 'legend': 'Altera Resibu'
    }
    return render(request, 'invoice/form.html', context)

@allowed_users(allowed_roles=['sigp_sup','sigp_bd'])
def supInvRem(request, hashid, pk):
    cont = get_object_or_404(Contract, hashed=hashid)
    objects = get_object_or_404(Invoice, pk=pk)
    objects.delete()
    messages.success(request, f'Hamos susesu.')
    return redirect('sup-inv-list', hashid=hashid)

@allowed_users(allowed_roles=['sigp_sup','sigp_bd'])
def supInvLock(request, hashid, pk):
    obj = get_object_or_404(Invoice, pk=pk)
    obj.is_lock = True
    obj.save()
    messages.success(request, f'Xavi.')
    return redirect('sup-inv-list', hashid=hashid)


@allowed_users(allowed_roles=['sigp_sup','sigp_bd'])
def supInvUnLock(request, hashid, pk):
    obj = get_object_or_404(Invoice, pk=pk)
    obj.is_lock = False
    obj.save()
    messages.success(request, f'Loke.')
    return redirect('sup-inv-list', hashid=hashid)

@allowed_users(allowed_roles=['sigp_sup','sigp_bd'])
def supInvReady(request, hashid, pk):
    obj = get_object_or_404(Invoice, pk=pk)
    obj.is_ready = True
    obj.save()
    messages.success(request, f'Resibu prontu.')
    return redirect('sup-inv-list', hashid=hashid)
###
@allowed_users(allowed_roles=['sigp_uivp','sigp_bd'])
def uvipInvIsADNY(request, hashid):
    obj = get_object_or_404(Invoice, hashed=hashid)
    obj.is_adn = True
    obj.save()
    messages.success(request, f'Altera susesu.')
    return redirect('uvip-inv-det', hashid=hashid)

@allowed_users(allowed_roles=['sigp_uivp'])
def uvipInvIsADNN(request, hashid):
    obj = get_object_or_404(Invoice, hashed=hashid)
    obj.is_adn = False
    obj.save()
    messages.success(request, f'Altera susesu.')
    return redirect('uvip-inv-det', hashid=hashid)

@allowed_users(allowed_roles=['sigp_uivp'])
def uvipInvADN(request, pk, page):
    obj = get_object_or_404(Invoice, pk=pk)
    if page == "1": 
        obj.is_adn = True
        obj.is_cna = False
    elif page == "2":
        obj.is_adn = True
        obj.is_cna = True
    else:
        obj.is_adn = False
        obj.is_cna = False
    obj.save()
    messages.success(request, f'Altera ona.')
    return redirect('uvip-inv-det', hashid=obj.hashed)
###
@allowed_users(allowed_roles=['sigp_gab'])
def gabInvAppr(request, pk):
    obj = get_object_or_404(Invoice, pk=pk)
    obj.is_appr = True
    obj.save()
    trackappr = InvTrack.objects.filter(inv=obj).first()
    trackappr.is_gap_app = True
    trackappr.date_gab_app = datetime.datetime.now()
    trackappr.save()
    messages.success(request, f'Resibu aprovadu.')
    return redirect('gab-inv-det', hashid=obj.hashed)