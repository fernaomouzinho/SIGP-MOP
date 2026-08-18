import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.contrib import messages
from contract.models import Amendment
from invoice.models import Invoice, InvTrack, InvLet
from invoice.forms import InvLetForm2
from users.decorators import allowed_users
from sigp.utils import get_roles

### SUP
@login_required
@allowed_users(allowed_roles=['sigp_sup'])
def supInvLetNext(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_send = True
    obj.is_back = False
    obj.comment = None
    obj.status = f"Supervizaun Munisipiu manda ona ba {obj.to.code}"
    obj.save()
    inv = obj.inv
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_sup_out = True
    track.date_sup_out = datetime.datetime.now()
    track.stages = f"Supervizaun Munisipiu manda ona ba UIVP"
    track.percent = 6
    track.save()
    messages.success(request, f'Supervizaun Munisipiu manda ona ba UIVP.')
    return redirect('sup-inv-det', hashid=inv.hashed)

### UIVP
@login_required
@allowed_users(allowed_roles=['sigp_uivp'])
def uvipInvBack(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(InvLet, hashed=hashid)
    inv = obj.inv
    if request.method == 'POST':
        form = InvLetForm2(request.POST, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_read = False
            instance.is_send = False
            instance.is_back = True
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            obj.status = "UIVP manda fila ba Supervizaun Munisipiu"
            obj.save()
            track = InvTrack.objects.filter(inv=inv).first()
            track.is_uvip_in = False
            track.date_uvip_in = None
            track.is_sup_out = False
            track.date_sup_out = None
            track.stages = "UIVP manda fila ba Supervizaun Munisipiu"
            track.percent = 0
            track.save()
            messages.success(request, f'Altera susesu.')
            return redirect('notif-uvip-inv-list')
    else: form = InvLetForm2(instance=obj)
    context = {
        'group':group, 'inv':inv, 'form':form,
        'title': 'Aumenta Komentariu', 'legend': 'Aumenta Komentariu'
    }
    return render(request, 'notif_uvip/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp'])
def uvipInvIn(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_read = True
    obj.status = "UIVP simu ona"
    obj.save()
    inv = obj.inv
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_uvip_in = True
    track.date_uvip_in = datetime.datetime.now()
    track.stages = "UIVP simu husi Supervizaun Munisipiu"
    track.percent = 13
    track.save()
    messages.success(request, f'UIVP simu husi Supervizaun Munisipiu.')
    return redirect('uvip-inv-det', hashid=inv.hashed)
#
@login_required
@allowed_users(allowed_roles=['sigp_uivp'])
def uvipInvInspStart(request, hashid):
    inv = get_object_or_404(Invoice, hashed=hashid)
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_insp_start = True
    track.date_insp_start = datetime.datetime.now()
    track.stages = "Inspeksaun hahu"
    track.percent = 19
    track.save()
    messages.success(request, f'Inspeksaun hahu.')
    return redirect('uvip-insp-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['sigp_uivp'])
def uvipInvInspEnd(request, hashid):
    inv = get_object_or_404(Invoice, hashed=hashid)
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_insp_end = True
    track.date_insp_end = datetime.datetime.now()
    track.stages = "Inspeksaun remata"
    track.percent = 25
    track.save()
    messages.success(request, f'Inspeksaun remata.')
    return redirect('uvip-inv-det', hashid=hashid)
#
@login_required
@allowed_users(allowed_roles=['sigp_uivp'])
def uvipInvNext1(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_send = True
    obj.is_back = False
    obj.status = "UIVP manda ona ba ADN"
    obj.save()
    inv = obj.inv
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_uvip_out_1 = True
    track.date_uvip_out_1 = datetime.datetime.now()
    track.is_adn_in = False
    track.date_adn_in = None
    track.stages = "UIVP manda ona ba ADN"
    track.percent = 31
    track.save()
    messages.success(request, f'UIVP manda ona ba ADN.')
    return redirect('uvip-inv-det', hashid=inv.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_uivp'])
def uvipInvADNIn(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_read = True
    obj.is_adn_back= True
    obj.status = "ADN manda mai UIVP"
    obj.save()
    inv = obj.inv
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_adn_in = True
    track.date_adn_in = datetime.datetime.now()
    track.stages = "ADN manda mai UIVP"
    track.percent = 38
    track.save()
    messages.success(request, f'ADN manda mai UIVP.')
    return redirect('uvip-inv-det', hashid=inv.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_uivp'])
def uvipInvNext2(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_send = True
    obj.is_back = False
    obj.comment = None
    obj.status = "UIVP manda ba Gabinete Ministru"
    obj.save()
    inv = obj.inv
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_uvip_out_2 = True
    track.date_uvip_out_2 = datetime.datetime.now()
    track.stages = "UIVP manda ba Gabinete Ministru"
    track.percent = 44
    track.save()
    messages.success(request, f'UIVP manda ba Gabinete Ministru.')
    return redirect('uvip-inv-det', hashid=inv.hashed)
### GAB
@login_required
@allowed_users(allowed_roles=['gab'])
def gabInvBack(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(InvLet, hashed=hashid)
    inv = obj.inv
    cont = inv.cont
    amend = Amendment.objects.filter(contract=cont).first()
    if request.method == 'POST':
        form = InvLetForm2(request.POST, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_read = False
            instance.is_send = False
            instance.is_back = True
            instance.save()
            track = InvTrack.objects.filter(inv=inv).first()
            track.is_uvip_out_2 = False
            track.date_uvip_out_2 = None
            track.is_gab_in = False
            track.date_gab_in = None
            track.stages = "Gabinete Ministru manda fila ba UIVP"
            track.percent = 40
            track.save()
            messages.success(request, f'Gabinete Ministru manda fila ba UIVP.')
            return redirect('notif-gab-inv-det', hashid=hashid)
    else: form = InvLetForm2(instance=obj)
    context = {
        'group':group, 'obj':obj, 'inv':inv, 'amend':amend, 'form':form,
        'title': 'Aumenta Komentariu', 'legend': 'Aumenta Komentariu'
    }
    return render(request, 'notif_gab/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigpp_gabm'])
def gabInvIn(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_read = True
    obj.status = "Gabinete Ministru Simu"
    obj.save()
    inv = obj.inv
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_gab_in = True
    track.date_gab_in = datetime.datetime.now()
    track.stages = "Husi UIVP manda mai Gabinete Ministru"
    track.percent = 53
    track.save()
    messages.success(request, f'Husi UIVP manda mai Gabinete Ministru.')
    return redirect('gab-inv-det', hashid=inv.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_gabm'])
def gabInvNext1(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_send = True
    obj.is_back = False
    obj.status = "Gabinete Ministru manda ba DGAF"
    obj.save()
    inv = obj.inv
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_gab_out = True
    track.date_gab_out = datetime.datetime.now()
    track.stages = "Gabinete Ministru manda ba DGAF"
    track.percent = 60
    track.save()
    messages.success(request, f'Gabinete Ministru manda ba DGAF.')
    return redirect('gab-inv-det', hashid=inv.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_gabm'])
def gabInvNext2(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_send = True
    obj.is_back = False
    obj.status = "Gabinete Ministru manda ba MPS"
    obj.save()
    inv = obj.inv
    inv.is_end = True
    inv.save()
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_gab_out = True
    track.date_gab_out = datetime.datetime.now()
    track.stages = "GAB ba MPS"
    track.percent = 100
    track.save()
    messages.success(request, f'UIVP ba MPS.')
    return redirect('gab-inv-det', hashid=inv.hashed)

### DGAF
@login_required
@allowed_users(allowed_roles=['sigp_dgaf'])
def dgafInvBack(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(InvLet, hashed=hashid)
    inv = obj.inv
    cont = inv.cont
    amend = Amendment.objects.filter(contract=cont).first()
    if request.method == 'POST':
        form = InvLetForm2(request.POST, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_read = False
            instance.is_send = False
            instance.is_back = True
            instance.save()
            track = InvTrack.objects.filter(inv=inv).first()
            track.is_gab_out = False
            track.date_gab_out = None
            track.stages = "DGAF manda fila ba Gabinete Ministru"
            track.percent = 53
            track.save()
            obj.status = "DGAF manda fila ba UIVP"
            obj.save()
            messages.success(request, f'Manda manda fila ona.')
            return redirect('notif-dgaf-inv-det', hashid=hashid)
    else: form = InvLetForm2(instance=obj)
    context = {
        'group': group, 'inv': inv, 'amend':amend, 'form': form, 'page': 'back',
        'title': 'Aumenta Komentariu', 'legend': 'Aumenta Komentariu'
    }
    return render(request, 'inv_let/form_let.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf'])
def dgafInvIn(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_read = True
    obj.status = "DGAF Simu"
    obj.save()
    inv = obj.inv
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_dgaf_in = True
    track.date_dgaf_in = datetime.datetime.now()
    track.stages = "Husi Gabinete Ministru manda mai DGAF"
    track.percent = 67
    track.save()
    messages.success(request, f'Husi Gabinete Ministru manda mai DGAF.')
    return redirect('dgaf-inv-det', hashid=inv.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf'])
def dgafInvNext(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_send = True
    obj.is_back = False
    obj.comment = None
    obj.status = "Manda ona ba DNA"
    obj.save()
    inv = obj.inv
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_dgaf_out = True
    track.date_dgaf_out = datetime.datetime.now()
    track.stages = "Husi DGAF manda ba DNA"
    track.percent = 73
    track.save()
    messages.success(request, f'Husi DGAF manda ba DNA.')
    return redirect('dgaf-inv-det', hashid=inv.hashed)
### DGAF
@login_required
@allowed_users(allowed_roles=['sigp_dna'])
def dnaInvBack(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(InvLet, hashed=hashid)
    inv = obj.inv
    cont = inv.cont
    amend = Amendment.objects.filter(contract=cont).first()
    if request.method == 'POST':
        form = InvLetForm2(request.POST, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_read = False
            instance.is_send = False
            instance.is_back = True
            instance.save()
            track = InvTrack.objects.filter(inv=inv).first()
            track.is_dgaf_out = False
            track.date_dgaf_out = None
            track.stages = "DNA manda fila ba DGAF"
            track.percent = 67
            track.save()
            messages.success(request, f'Manda fila ona.')
            return redirect('notif-dna-inv-det', hashid=hashid)
    else: form = InvLetForm2(instance=obj)
    context = {
        'group': group, 'inv': inv, 'amend':amend, 'form': form, 'page': 'back',
        'title': 'Aumenta Komentariu', 'legend': 'Aumenta Komentariu'
    }
    return render(request, 'inv_let/form_let.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna'])
def dnaInvIn(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_read = True
    obj.status = "DNA Simu"
    obj.save()
    inv = obj.inv
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_dna_in = True
    track.date_dna_in = datetime.datetime.now()
    track.stages = "Husi DGAF manda mai DNA"
    track.percent = 80
    track.save()
    messages.success(request, f'Husi DGAF manda mai DNA.')
    return redirect('dna-inv-det', hashid=inv.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_dna'])
def dnaInvNext(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_send = True
    obj.is_back = False
    obj.comment = None
    obj.status = "Manda ona ba DNOF"
    obj.save()
    inv = obj.inv
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_dna_out = True
    track.date_dna_out = datetime.datetime.now()
    track.stages = "Husi DNA manda ba DNOF"
    track.percent = 87
    track.save()
    messages.success(request, f'Husi DNA manda ba DNOF.')
    return redirect('dna-inv-det', hashid=inv.hashed)
# DNOF
@login_required
@allowed_users(allowed_roles=['sigp_dnof'])
def dnofInvBack(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(InvLet, hashed=hashid)
    inv = obj.inv
    cont = inv.cont
    amend = Amendment.objects.filter(contract=cont).first()
    if request.method == 'POST':
        form = InvLetForm2(request.POST, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_read = False
            instance.is_send = False
            instance.is_back = True
            instance.save()
            track = InvTrack.objects.filter(inv=inv).first()
            track.is_dna_out = False
            track.date_dna_out = None
            track.stages = "DNOF manda fila ba DNA"
            track.percent = 80
            track.save()
            obj.status = "DNOF manda fila ba DNA"
            obj.save()
            messages.success(request, f'Manda manda fila ona.')
            return redirect('notif-dnof-inv-det', hashid=hashid)
    else: form = InvLetForm2(instance=obj)
    context = {
        'group':group, 'obj':obj, 'inv':inv, 'amend':amend, 'form':form, 'page':'inv',
        'title':'Aumenta Komentariu', 'legend':'Aumenta Komentariu'
    }
    return render(request, 'notif_dnof/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dnof'])
def dnofInvIn(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_read = True
    obj.status = "DNOF Simu"
    obj.save()
    inv = obj.inv
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_dnof_in = True
    track.date_dnof_in = datetime.datetime.now()
    track.stages = "Husi DNA manda mai DNOF"
    track.percent = 93
    track.save()
    messages.success(request, f'Husi DNA manda mai DNOF.')
    return redirect('dnof-inv-det', hashid=inv.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_dnof'])
def dnofInvNext(request, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.is_send = True
    obj.status = "DNOF manda ba MF"
    obj.save()
    inv = obj.inv
    track = InvTrack.objects.filter(inv=inv).first()
    track.is_dnof_out = True
    track.date_dnof_out = datetime.datetime.now()
    track.stages = "DNOF manda ba MF"
    track.percent = 100
    track.save()
    messages.success(request, f'DNOF ba MF.')
    return redirect('dnof-inv-det', hashid=inv.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_dnof'])
def dnofInvEnd(request, pk):
    obj = get_object_or_404(Invoice, pk=pk)
    obj.is_paid = True
    obj.is_end = True
    obj.save()
    messages.success(request, f'DNOF TERMINA.')
    return redirect('dnof-inv-det', hashid=obj.hashed)
