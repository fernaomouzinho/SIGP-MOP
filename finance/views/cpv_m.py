import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conf.decorators import allowed_users
from finance.models import CPV, CPVReq, CPVTrack, CPVLetter
from finance.forms import CPVForm, CPVForm2, CPVLetterForm
from conf.user_utils import c_user_div, c_user_dna, c_user_dnof,c_user_dgaf
from conf.utils import getnewid, write_roman

#dnof
@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVAdd(request, hashid):
    group = request.user.groups.all()[0].name
    if group == "dnof": div = c_user_dnof(request.user)
    
    cpvreq = get_object_or_404(CPVReq, hashed=hashid)
    proj = cpvreq.proj
    if request.method == 'POST':
        newid, new_hashid = getnewid(CPV)
        form = CPVForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.proj = proj
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Aumenta susesu.')
            return redirect('dnof-cpv-det', hashid=proj.hashed)
    else: form = CPVForm()
    context = {
        'group': group, 'form': form, 'cpvreq':cpvreq, 'proj':proj, 'page':'add',
        'title': 'Aumenta CPV', 'legend': 'Aumenta CPV'
    }
    return render(request, 'finance_cpv/form.html', context)

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVEdit(request, hashid):
    group = request.user.groups.all()[0].name
    obj = get_object_or_404(CPV, hashed=hashid)
    proj = obj.proj
    if request.method == 'POST':
        form = CPVForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera susesu.')
            return redirect('dnof-cpv-det', hashid=proj.hashed)
    else: form = CPVForm(instance=obj)
    context = {
        'group': group, 'obj':obj, 'proj':proj, 'form': form,
        'title': 'Altera CPV', 'legend': 'Altera CPV'
    }
    return render(request, 'finance_cpv/form.html', context)

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVRem(request, pk):
    obj = get_object_or_404(CPV, pk=pk)
    proj = obj.proj
    obj.delete()
    messages.success(request, f'Hamos susesu.')
    return redirect('dnof-cpv-det', hashid=proj.hashed)

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVSend(request, pk, pk2):
    obj = get_object_or_404(CPV, pk=pk)
    if pk2 == "1": 
        obj.is_dgaf = True
        obj.group = "dgaf"
        obj.status = "DNOF Manda ba DGAF"
    else: 
        obj.is_dgaf = False
        obj.group = "gab"
        obj.status = "DNOF Manda ba Gabinete Ministru"
    obj.is_send = True
    obj.is_back = False
    obj.comment = None
    obj.save()
    proj = obj.proj
    track = CPVTrack.objects.filter(cpv=obj).first()
    track.is_dnof_out = True
    track.date_dnof_out = datetime.datetime.now()
    if pk2 == "1":
        track.stages = "DNOF ba DGAF"
    else:
        track.stages = "DNOF ba Gabinete Ministru"
    track.percent = 20
    track.save()
    messages.success(request, f'DNOF ba DGAF.')
    return redirect('dnof-cpv-det', hashid=proj.hashed)
# dgaf
@login_required
@allowed_users(allowed_roles=['dgaf','gab'])
def dgafCPVBack(request, hashid):
    group = request.user.groups.all()[0].name
    cpv = get_object_or_404(CPV, hashed=hashid)
    track = CPVTrack.objects.filter(cpv=cpv).first()
    if request.method == 'POST':
        form = CPVForm2(request.POST, instance=cpv)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_back = True
            instance.is_send = False
            instance.is_read = False
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            cpv.status = "DGAF Manda Fila"
            cpv.save()
            track.is_dnof_out = False
            track.date_dnof_out = None
            track.stages = "DGAF fila ba DNOF"
            track.percent = 0
            track.save()
            messages.success(request, f'DGAF fila ba DNOF.')
            return redirect('dgaf-cpv-det', hashid=hashid)
    else: form = CPVForm2(instance=cpv)
    context = {
        'group': group, 'cpv': cpv, 'proj':cpv.proj, 'form': form, 'page':'det',
        'title': 'Komentariu Manda Fila', 'legend': 'Komentariu Manda Fila'
    }
    return render(request, 'finance_cpv/form.html', context)

@login_required
@allowed_users(allowed_roles=['dgaf','gab'])
def dgafCPVIn(request, pk):
    obj = get_object_or_404(CPV, pk=pk)
    obj.is_read = True
    obj.status = "DGAF Simu"
    obj.save()
    track = CPVTrack.objects.filter(cpv=obj).first()
    track.is_dgaf_in = True
    track.date_dgaf_in = datetime.datetime.now()
    track.stages = "DGAF Simu"
    track.percent = 40
    track.save()
    messages.success(request, f'DGAF Simu.')
    return redirect('dgaf-cpv-det', hashid=obj.hashed)

@login_required
@allowed_users(allowed_roles=['dgaf','gab'])
def dgafCPVAppr(request, pk):
    obj = get_object_or_404(CPV, pk=pk)
    obj.is_appr = True
    obj.status = "DGAF Aprova"
    obj.save()
    track = CPVTrack.objects.filter(cpv=obj).first()
    track.is_appr = True
    track.date_appr = datetime.datetime.now()
    track.stages = "CPV Aprovadu"
    track.percent = 60
    track.save()
    messages.success(request, f'CPV Aprovadu.')
    return redirect('dgaf-cpv-det', hashid=track.cpv.hashed)
#
@login_required
@allowed_users(allowed_roles=['dgaf','gab'])
def dgafCPVLetEdit(request, hashid, pk):
    group = request.user.groups.all()[0].name
   
    cpv = get_object_or_404(CPV, hashed=hashid)
    obj = get_object_or_404(CPVLetter, pk=pk)
    if request.method == 'POST':
        form = CPVLetterForm(request.POST, request.FILES, instance=obj)
        mt = datetime.datetime.today().month
        yr = datetime.datetime.today().year
        rom_num = write_roman(mt)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('dgaf-cpv-det', hashid=hashid)
    else: form = CPVLetterForm(instance=obj)
    context = {
        'group': group, 'cpv': cpv, 'proj':cpv.proj, 'form': form,
        'title': 'Altera Despaxu', 'legend': 'Altera Despaxu'
    }
    return render(request, 'finance_cpv/form.html', context)

@login_required
@allowed_users(allowed_roles=['dgaf','gab'])
def dgafCPVLetRem(request, pk):
    obj = get_object_or_404(CPVLetter, pk=pk)
    obj.number = None
    obj.subject = None
    obj.date = None
    obj.file = None
    obj.save()
    messages.success(request, f'Hamos ona.')
    return redirect('dgaf-cpv-det', hashid=obj.cpv.hashed)

@login_required
@allowed_users(allowed_roles=['dgaf','gab'])
def dgafCPVSend(request, pk):
    obj = get_object_or_404(CPVLetter, pk=pk)
    obj.is_send = True
    obj.save()
    cpv = obj.cpv
    cpv.status = "DGAF Manda ba DNOF"
    cpv.save()
    track = CPVTrack.objects.filter(cpv=obj.cpv).first()
    track.is_dgaf_out = True
    track.date_dgaf_out = datetime.datetime.now()
    track.stages = "Manda ba DNOF"
    track.percent = 80
    track.save()
    messages.success(request, f'Manda ba DNOF.')
    return redirect('dgaf-cpv-det', hashid=obj.cpv.hashed)
# dnof
@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVIn(request, pk):
    obj = get_object_or_404(CPVLetter, pk=pk)
    obj.is_read = True
    obj.save()
    cpv = obj.cpv
    cpv.status = "DNOF Simu"
    cpv.save()
    track = CPVTrack.objects.filter(cpv=obj.cpv).first()
    track.is_dnof_in = True
    track.date_dnof_in = datetime.datetime.now()
    track.stages = "DNOF Simu"
    track.percent = 83
    track.save()
    messages.success(request, f'DNOF Simu.')
    return redirect('dnof-cpv-let-det', hashid=obj.hashed)

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVEnd(request, pk):
    obj = get_object_or_404(CPVLetter, pk=pk)
    cpv = obj.cpv
    cpv.status = "Aprovadu & Termina"
    cpv.save()
    cpv.is_end = True
    cpv.save()
    track = CPVTrack.objects.filter(cpv=cpv).first()
    track.is_end = True
    track.date_end = datetime.datetime.now()
    track.stages = "CPV Termina"
    track.percent = 100
    track.save()
    messages.success(request, f'CPV Termina.')
    return redirect('dnof-cpv-let-det', hashid=obj.hashed)
