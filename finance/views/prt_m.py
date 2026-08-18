import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conf.decorators import allowed_users
from invoice.models import Invoice, InvTrack
from finance.models import PRT, EV
from finance.forms import PRTForm, PRTForm2, EVForm
from conf.user_utils import c_user_dna
from conf.utils import getnewid

@login_required
@allowed_users(allowed_roles=['dna'])
def dnaPRTAdd(request, hashid):
    group = request.user.groups.all()[0].name
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    proj = cont.project
    if request.method == 'POST':
        newid, new_hashid = getnewid(PRT)
        form = PRTForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.cont = cont
            instance.inv = inv
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Aumenta ona.')
            return redirect('dna-inv-det', hashid=hashid)
    else: form = PRTForm()
    context = {
        'group': group, 'proj': proj, 'inv': inv, 'form': form,
        'title': 'Aumenta PRT', 'legend': 'Aumenta PRT'
    }
    return render(request, 'finance_prt/form.html', context)

@login_required
@allowed_users(allowed_roles=['dna'])
def dnaPRTEdit(request, hashid):
    group = request.user.groups.all()[0].name
    obj = get_object_or_404(PRT, hashed=hashid)
    inv = obj.inv
    cont = inv.cont
    proj = cont.project
    if request.method == 'POST':
        form = PRTForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('dna-inv-det', hashid=hashid)
    else: form = PRTForm(instance=obj)
    context = {
        'group': group, 'proj': proj, 'inv': inv, 'form': form,
        'title': 'Altera PRT', 'legend': 'Altera PRT'
    }
    return render(request, 'finance_prt/form.html', context)

@login_required
@allowed_users(allowed_roles=['dna'])
def dnaPRTRem(request, hashid, pk):
    prt = get_object_or_404(PRT, pk=pk)
    prt.delete()
    messages.success(request, f'Apaga ona.')
    return redirect('dna-prt-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['dna'])
def dnaPRTReady(request, hashid, pk):
    prt = get_object_or_404(PRT, pk=pk)
    prt.is_ready = True
    prt.save()
    messages.success(request, f'PRT pronto ona.')
    return redirect('prt-list', hashid=hashid)
###
@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofEVEdit(request, hashid, pk):
    group = request.user.groups.all()[0].name
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    proj = cont.project
    obj = get_object_or_404(EV, pk=pk)
    if request.method == 'POST':
        form = EVForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('dnof-inv-det', hashid=hashid)
    else: form = EVForm(instance=obj)
    context = {
        'group': group, 'proj': proj, 'cont': inv.cont, 'inv': inv, 'form': form,
        'title': 'Altera EV', 'legend': 'Altera EV'
    }
    return render(request, 'finance_prt/form.html', context)

@login_required
@allowed_users(allowed_roles=['dnof','dnof-bo'])
def dnofEVReady(request, hashid, pk):
    ev = get_object_or_404(EV, pk=pk)
    ev.is_ready = True
    ev.save()
    messages.success(request, f'EV pronto ona.')
    return redirect('prt-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['dnof','dnof-bo'])
def dnofEVSend(request, hashid, pk):
    ev = get_object_or_404(EV, pk=pk)
    ev.is_send= True
    #ev.is_dnof_back_in = True
    #ev.date_dnof_back_in = datetime.datetime.now()
    #ev.is_dnof_back_ver_start = True
    #ev.date_dnof_back_ver_start = datetime.datetime.now()
    invtrack = InvTrack.objects.get(inv=ev.inv)
    invtrack.is_dnof_middle_out = True
    invtrack.date_dnof_middle_out = datetime.datetime.now()
    invtrack.stages = f"Husi DNOF Middle Office ba Back Office"
    invtrack.save()
    ev.save()
    messages.success(request, f'EV manda ona.')
    return redirect('prt-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['dnof','dnof-bo'])
def dnofboEVReceive(request, hashid, pk):
    ev = get_object_or_404(EV, pk=pk)
    ev.is_receive = True
    ev.save()
    invtrack = InvTrack.objects.get(inv=ev.inv)
    invtrack.is_dnof_back_in = True
    invtrack.date_dnof_back_in = datetime.datetime.now()
    invtrack.is_dnof_back_insp_start = True
    invtrack.date_dnof_back_insp_start = datetime.datetime.now()
    invtrack.percent = 94
    invtrack.save()
    messages.success(request, f'EV Simu ona.')
    return redirect('prt-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['dnof','dnof-bo'])
def dnofboEVVerify(request, hashid, pk):
    ev = get_object_or_404(EV, pk=pk)
    invtrack = InvTrack.objects.get(inv=ev.inv)
    invtrack.is_dnof_back_insp_end = True
    invtrack.date_dnof_back_insp_end = datetime.datetime.now()
    invtrack.is_dnof_back_cre_start = True
    invtrack.date_dnof_back_cre_start = datetime.datetime.now()
    invtrack.percent = 95
    invtrack.save()
    messages.success(request, f'PEP Verifika ona.')
    return redirect('prt-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['dnof','dnof-bo'])
def dnofboEVCreate(request, hashid, pk):
    ev = get_object_or_404(EV, pk=pk)
    invtrack = InvTrack.objects.get(inv=ev.inv)
    invtrack.is_dnof_back_cre_end = True
    invtrack.date_dnof_back_cre_end = datetime.datetime.now()
    invtrack.is_dnof_back_apr_start = True
    invtrack.date_dnof_back_apr_start = datetime.datetime.now()
    invtrack.percent = 96
    invtrack.save()
    messages.success(request, f'PEP Kria ona.')
    return redirect('prt-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['dnof','dnof-bo'])
def dnofboEVAprove(request, hashid, pk):
    ev = get_object_or_404(EV, pk=pk)
    invtrack = InvTrack.objects.get(inv=ev.inv)
    invtrack.is_dnof_back_apr_end = True
    invtrack.date_dnof_back_apr_end = datetime.datetime.now()
    invtrack.percent = 98
    invtrack.save()
    messages.success(request, f'PEP Kria ona.')
    return redirect('prt-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['dnof','dnof-bo'])
def dnofboEVTerminate(request, hashid, pk):
    ev = get_object_or_404(EV, pk=pk)
    ev.is_read= True
    ev.save()
    
    invtrack = InvTrack.objects.get(inv=ev.inv)
    invtrack.is_dnof_out = True
    invtrack.date_dnof_out = datetime.datetime.now()
    invtrack.is_dnof_back_out = True
    invtrack.date_dnof_back_out = datetime.datetime.now()
    invtrack.percent = 100
    invtrack.save()
    inv = Invoice.objects.get(pk=ev.inv.pk)
    inv.is_end = True
    inv.save()
    messages.success(request, f'PEP Termina ona.')
    return redirect('prt-list', hashid=hashid)