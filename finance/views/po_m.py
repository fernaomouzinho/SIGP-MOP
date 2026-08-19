import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.decorators import allowed_users
from sigp.utils import get_roles
from contract.models import Contract
from invoice.models import Invoice
from finance.models import PO, POTrack, POLetter, CPV
from finance.forms import POForm, POForm2, POForm3, POLetterForm
from conf.utils import getnewid,write_roman


@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaPOAdd(request, hashid):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    proj = cont.project
    cpv = CPV.objects.filter(proj=proj).last()
    if request.method == 'POST':
        newid, new_hashid = getnewid(PO)
        form = POForm(proj, request.POST, request.FILES)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.cont = cont
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            
            cpv.is_get_dna = True
            cpv.save()
            messages.success(request, f'Aumenta ona.')
            return redirect('dna-po-list', hashid=hashid)
    else: form = POForm(proj)
    context = {
        'group':group, 'proj':proj, 'cont':cont, 'form':form,
        'title': 'Aumenta PO', 'legend': 'Aumenta PO'
    }
    return render(request, 'finance_po/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaPOEdit(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(PO, hashed=hashid)
    cont = obj.cont
    proj = cont.project
    if request.method == 'POST':
        form = POForm(proj, request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('dna-po-list', hashid=cont.hashed)
    else: form = POForm(proj, instance=obj)
    context = {
        'group': group, 'proj':proj, 'cont': cont, 'form': form,
        'title': 'Altera PO', 'legend': 'Altera PO'
    }
    return render(request, 'finance_po/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaPOEdit2(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(PO, hashed=hashid)
    cont = obj.cont
    proj = cont.project
    if request.method == 'POST':
        form = POForm2(cont, request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('dna-po-list', hashid=cont.hashed)
    else: form = POForm2(cont, instance=obj)
    context = {
        'group': group, 'proj':proj, 'cont': cont, 'form': form,
        'title': 'Altera PO', 'legend': 'Altera PO'
    }
    return render(request, 'finance_po/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaPORef(request, pk, pk2):
    obj = get_object_or_404(PO, hashed=pk)
    inv = get_object_or_404(Invoice, hashed=pk2)
    obj.inv = inv
    obj.save()
    messages.success(request, f'Altera ona.')
    return redirect('dna-inv-det', hashid=inv.hashed)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaPORem(request, pk):
    po = get_object_or_404(PO, pk=pk)
    cont = po.cont
    po.delete()
    messages.success(request, f'Hapaga ona.')
    return redirect('dna-po-list', hashid=cont.hashed)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaPOSend(request, pk):
    obj = get_object_or_404(PO, pk=pk)
    obj.is_send = True
    obj.is_back = False
    obj.comment = None
    obj.status = "DNA Manda ba DGAF"
    obj.save()
    cont = obj.cont
    track = POTrack.objects.filter(po=obj).first()
    track.is_dna_out = True
    track.date_dna_out = datetime.datetime.now()
    track.stages = "DNA ba DGAF"
    track.percent = 20
    track.save()
    messages.success(request, f'DNA ba DGAF.')
    return redirect('dna-po-list', hashid=cont.hashed)
# dgaf
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafPOBack(request, hashid):
    group = get_roles(request)
    po = get_object_or_404(PO, hashed=hashid)
    track = POTrack.objects.filter(po=po).first()
    if request.method == 'POST':
        form = POForm3(request.POST, instance=po)
       
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_back = True
            instance.is_send = False
            instance.is_read = False
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            po.status = "DGAF Manda Fila"
            po.save()
            track.is_dna_out = False
            track.date_dna_out = None
            track.stages = "DGAF fila ba DNA"
            track.percent = 0
            track.save()
            messages.success(request, f'DGAF fila ba DNA.')
            return redirect('notif-dgaf-po-det', hashid=hashid)
    else: form = POForm3(instance=po)
    context = {
        'group': group, 'po':po, 'cont':po.cont, 'proj':po.cont.project, 'form':form,
        'title': 'Komentariu Manda Fila', 'legend': 'Komentariu Manda Fila'
    }
    return render(request, 'finance_po/form.html', context)

@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafPOIn(request, pk):
    obj = get_object_or_404(PO, pk=pk)
    obj.is_read = True
    obj.status = "DGAF Simu"
    obj.save()
    track = POTrack.objects.filter(po=obj).first()
    track.is_dgaf_in = True
    track.date_dgaf_in = datetime.datetime.now()
    track.stages = "DGAF Simu"
    track.percent = 40
    track.save()
    messages.success(request, f'DGAF Simu.')
    return redirect('dgaf-po-det', hashid=obj.hashed)

@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafPOAppr(request, pk):
    obj = get_object_or_404(PO, pk=pk)
    obj.is_appr = True
    obj.status = "DGAF Aprova"
    obj.save()
    track = POTrack.objects.filter(po=obj).first()
    track.is_appr = True
    track.date_appr = datetime.datetime.now()
    track.stages = "PO Aprovadu"
    track.percent = 60
    track.save()
    messages.success(request, f'DGAF Aprova.')
    return redirect('dgaf-po-det', hashid=obj.hashed)
#
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafPOLetEdit(request, hashid, pk):
    group = get_roles(request)
    po = get_object_or_404(PO, hashed=hashid)
    obj = get_object_or_404(POLetter, pk=pk)
    if request.method == 'POST':
        form = POLetterForm(request.POST, request.FILES, instance=obj)
        mt = datetime.datetime.today().month
        yr = datetime.datetime.today().year
        rom_num = write_roman(mt)
        if form.is_valid():
            instance = form.save(commit=False)
            data = form.cleaned_data
            number = data['number']
            instance.number = "%s/%s-MOP/%s/%s" % (number,group.upper(),rom_num,yr)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('dgaf-po-det', hashid=hashid)
    else: form = POLetterForm(instance=obj)
    context = {
        'group': group, 'po': po, 'cont':po.cont, 'proj':po.cont.project, 'form': form,
        'title': 'Altera Despaxu', 'legend': 'Altera Despaxu'
    }
    return render(request, 'finance_po/form.html', context)

@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafPOLetRem(request, pk):
    obj = get_object_or_404(POLetter, pk=pk)
    obj.number = None
    obj.subject = None
    obj.date = None
    obj.file = None
    obj.save()
    messages.success(request, f'Hapaga ona.')
    return redirect('notif-dgaf-po-det', hashid=obj.po.hashed)

@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafPOSend(request, pk):
    obj = get_object_or_404(POLetter, pk=pk)
    obj.is_send = True
    obj.save()
    po = obj.po
    po.status = "DGAF Manda ba DNA"
    po.save()
    track = POTrack.objects.filter(po=obj.po).first()
    track.is_dgaf_out = True
    track.date_dgaf_out = datetime.datetime.now()
    track.stages = "Manda ba DNA"
    track.percent = 80
    track.save()
    messages.success(request, f'Manda ba DNA.')
    return redirect('dgaf-po-det', hashid=obj.po.hashed)
# dna
@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaPOIn(request, pk):
    obj = get_object_or_404(POLetter, pk=pk)
    obj.is_read = True
    obj.save()
    po = obj.po
    po.status = "DNA Simu"
    po.save()
    track = POTrack.objects.filter(po=obj.po).first()
    track.is_dna_in = True
    track.date_dna_in = datetime.datetime.now()
    track.stages = "DNA Simu"
    track.percent = 83
    track.save()
    messages.success(request, f'DNA Simu.')
    return redirect('dna-po-det', hashid=obj.po.hashed)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaPOEnd(request, pk):
    obj = get_object_or_404(POLetter, pk=pk)
    po = obj.po
    po.is_end = True
    po.status = "Aprovadu & Termina"
    po.save()
    track = POTrack.objects.filter(po=po).first()
    track.is_end = True
    track.date_end = datetime.datetime.now()
    track.stages = "PO Termina"
    track.percent = 100
    track.save()
    messages.success(request, f'PO Termina.')
    return redirect('dna-po-det', hashid=po.hashed)

