import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from custom.models import DG,Division
from conf.decorators import allowed_users
from proc.models import Proc, ProcComp, ProcLet, ProcReqTrack, ProcResTrack, ProcTrack
from proc.forms import ProcCompForm, ProcForm, ProcTrackForm, ProcLetForm
from conf.user_utils import c_user_dna,c_user_dgaf
from conf.utils import getnewid,write_roman
from django.core.exceptions import ObjectDoesNotExist
from users.decorators import allowed_users
from sigp.utils import get_roles


@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcAdd(request):
    group = get_roles(request)
    if 'sigp_dna' in group: div = c_user_dna(request.user)
 
    if request.method == 'POST':
        newid, new_hashid = getnewid(Proc)
        form = ProcForm(request.POST)
        mt = datetime.datetime.today().month
        yr = datetime.datetime.today().year
        dv = div.code
        dg = div.dg.code
        rom_num = write_roman(mt)
  
  
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            data = form.cleaned_data
            number = data['number']
            instance.number = "%s/%s-%s-MOP/%s/%s" % (number,dv,dg,rom_num,yr)
            num= instance.number
            try:
                p = Proc.objects.get(number=num)
                messages.warning(request, f'Numeru referensia %s eziste ona. Favor prense ho numeru refencia seluk' % (number))
                return redirect('dna-proc-add')
            
            except ObjectDoesNotExist:
                instance.datetime = datetime.datetime.now()
                instance.user = request.user
                instance.hashed = new_hashid
                instance.save()
                messages.success(request, f'Aumenta ona.')
                return redirect('dna-proc-det', hashid=new_hashid)
    else: form = ProcForm()
    context = {
        'group':group, 'form':form, 'page':'input',
        'title':'Aumenta Tender', 'legend':'Aumenta Tender'
    }
    return render(request, 'proc_dna/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcEdit(request, hashid):
    group = get_roles(request)
    proc = get_object_or_404(Proc, hashed=hashid)
    if request.method == 'POST':
        form = ProcForm(request.POST, instance=proc)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('dna-proc-det', hashid=hashid)
    else: form = ProcForm(instance=proc)
    context = {
        'group':group, 'proc':proc, 'form':form, 'page':'det',
        'title': 'Altera Tender', 'legend': 'Altera Tender'
    }
    return render(request, 'proc_dna/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcRem(request, hashid):
    obj = get_object_or_404(Proc, hashed=hashid)
    obj.delete()
    messages.success(request, f'Hapaga ona.')
    return redirect('dna-proc-list')

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcLock(request, hashid):
    obj = get_object_or_404(Proc, hashed=hashid)
    obj.is_lock = True
    obj.save()
    messages.success(request, f'Xavi ona.')
    return redirect('dna-proc-det', hashid=hashid)
###
@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcCompAdd(request, hashid):
    group = request.user.groups.all()[0].name
    proc = get_object_or_404(Proc, hashed=hashid)
    proj = proc.proj
    if request.method == 'POST':
        newid, new_hashid = getnewid(ProcComp)
        form = ProcCompForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.proc = proc
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Aumenta succesu.')
            return redirect('dna-proc-det', hashid=hashid)
    else: form = ProcCompForm()
    context = {
        'group':group, 'proc': proc, 'proj': proj, 'form': form,
        'title': 'Aumenta Companha', 'legend': 'Aumenta Companha'
    }
    return render(request, 'proc_dna/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcCompEdit(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(ProcComp, hashed=hashid)
    proc = obj.proc
    proj = proc.proj
    if request.method == 'POST':
        form = ProcCompForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Altera succesu.')
            return redirect('dna-proc-det', hashid=proc.hashed)
    else: form = ProcCompForm(instance=obj)
    context = {
        'group':group, 'proc':proc, 'proj':proj, 'form':form,
        'title':'Altera Companha', 'legend':'Altera Companha'
    }
    return render(request, 'proc_dna/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcCompRem(request, hashid):
    obj = get_object_or_404(ProcComp, hashed=hashid)
    proc = obj.proc
    obj.delete()
    messages.success(request, f'Hapaga succesu.')
    return redirect('dna-proc-det', hashid=proc.hashed)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcCompWin(request, hashid):
    obj = get_object_or_404(ProcComp, hashed=hashid)
    proc = obj.proc
    obj.is_win = True
    obj.save()
    objects = ProcComp.objects.exclude(hashed=hashid).all()
    for i in objects:
        i.is_win = False
        i.save()
    messages.success(request, f'Altera succesu.')
    return redirect('dna-proc-det', hashid=proc.hashed)
###
@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcTrackEdit(request, hashid, pk):
    group = get_roles(request)
    proc = get_object_or_404(Proc, hashed=hashid)
    objects = get_object_or_404(ProcTrack, pk=pk)
    if request.method == 'POST':
        form = ProcTrackForm(request.POST, instance=objects)
        if form.is_valid():
            instance = form.save(commit=False)
            if form.cleaned_data.get('is_announce') == True and form.cleaned_data.get('is_open') == False:
                instance.stages = "Anuncia"
                instance.percent = 64
            elif form.cleaned_data.get('is_open') == True and form.cleaned_data.get('is_eval') == False:
                instance.stages = "Open Bid"
                instance.percent = 73
            elif form.cleaned_data.get('is_eval') == True and form.cleaned_data.get('is_result') == False:
                instance.stages = "Avaliasaun"
                instance.percent = 82
            elif form.cleaned_data.get('is_result') == True:
                instance.stages = "Anuncia Resultadu"
                instance.percent = 91
            instance.save()
            messages.success(request, f'Altera succesu.')
            return redirect('dna-proc-det', hashid=hashid)
    else: form = ProcTrackForm(instance=objects)
    context = {
        'group':group, 'proc':proc, 'proj':proc.proj, 'form': form, 'page':'proc',
        'title': 'Altera Etapa', 'legend': 'Altera Etapa'
    }
    return render(request, 'track/form.html', context)
###
@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcReqStart(request, pk):
    proc = get_object_or_404(Proc, pk=pk)
    proc.is_req_start = True
    proc.is_lock = True
    proc.save()
    track = ProcReqTrack.objects.filter(proc=proc).first()
    track.is_start = True
    track.date_start = datetime.datetime.now()
    track.stages = "Procesu Hahu"
    track.percent = 0
    track.save()
    messages.success(request, f'Pedidu Tender Hahu.')
    return redirect('dna-proc-req-det', hashid=proc.hashed)

@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabProcReqAppr(request, pk):
    proc = get_object_or_404(Proc, pk=pk)
    proc.is_req_appr = True
    proc.save()
    messages.success(request, f'Pedidu Tender Aprovadu.')
    return redirect('gab-proc-req-det', hashid=proc.hashed)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcReqEnd(request, pk):
    proc = get_object_or_404(Proc, pk=pk)
    proc.is_req_end = True
    proc.save()
    track = ProcReqTrack.objects.filter(proc=proc).first()
    track.is_end = True
    track.date_end = datetime.datetime.now()
    track.stages = "Pedidu Tender Termina"
    track.percent = 100
    track.save()
    messages.success(request, f'Pedidu Tender Termina.')
    return redirect('dna-proc-req-det', hashid=proc.hashed)
#
@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcResStart(request, pk):
    proc = get_object_or_404(Proc, pk=pk)
    proc.is_res_start = True
    proc.save()
    track = ProcResTrack.objects.filter(proc=proc).first()
    track.is_start = True
    track.date_start = datetime.datetime.now()
    track.stages = "Procesu Hahu"
    track.percent = 0
    track.save()
    messages.success(request, f'Procesu Tender Hahu.')
    return redirect('dna-proc-det', hashid=proc.hashed)

@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabProcResAppr(request, pk):
    proc = get_object_or_404(Proc, pk=pk)
    proc.is_res_appr = True
    proc.save()
    messages.success(request, f'Resultadu Tender Aprovadu.')
    return redirect('gab-proc-res-det', hashid=proc.hashed)

@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcResEnd(request, pk):
    proc = get_object_or_404(Proc, pk=pk)
    proc.is_res_end = True
    proc.save()
    track = ProcResTrack.objects.filter(proc=proc).first()
    track.is_end = True
    track.date_end = datetime.datetime.now()
    track.stages = "Procesu Tender Termina"
    track.percent = 100
    track.save()
    messages.success(request, f'Procesu Tender Termina.')
    return redirect('dna-proc-res-det', hashid=proc.hashed)
### Let
@allowed_users(allowed_roles=['sigp_dgaf','sigp_gabm','sigp_admin'])
def ProcLetAdd(request, hashid, page):
    group = get_roles(request)
    proc = get_object_or_404(Proc, hashed=hashid)
    proj = proc.proj
    if request.method == 'POST':
        newid, new_hashid = getnewid(ProcLet)
        form = ProcLetForm(request.POST, request.FILES)
        mt = datetime.datetime.today().month
        yr = datetime.datetime.today().year
        rom_num = write_roman(mt)
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            data = form.cleaned_data
            number = data['number']
            instance.number = "%s/%s-MOP/%s/%s" % (number,group.upper(),rom_num,yr)
            num = instance.number
            try:
                p = ProcLet.objects.get(number=num)
                messages.warning(request, f'Numeru referensia %s eziste ona. Favor prense ho numeru refencia seluk' % (number))
                return redirect('proc-let-add', proc.hashed, page)
            
            except ObjectDoesNotExist:
                instance.proc = proc
                if 'sigp_dgaf' in group:
                    instance.is_dgaf = True
                if page == "req": instance.is_req = True
                
                instance.datetime = datetime.datetime.now()
                instance.user = request.user
                instance.hashed = new_hashid
                instance.save()
                messages.success(request, f'Aumenta ona.')
                if page == "req": 
                    if 'sigp_dgaf' in group: return redirect('dgaf-proc-req-det', hashid=hashid)
                    elif 'sigp_gabm' in group: return redirect('gab-proc-req-det', hashid=hashid)
                elif page == "res": 
                    if 'sigp_dgaf' in group: return redirect('dgaf-proc-res-det', hashid=hashid)
                    elif 'sigp_gabm' in group: return redirect('gab-proc-res-det', hashid=hashid)
    else: form = ProcLetForm()
    context = {
        'group':group, 'proj':proj, 'proc':proc, 'form':form, 'page':page,
        'title':'Aumenta Karta', 'legend':'Aumenta Karta'
    }
    return render(request, 'proc/form.html', context)

@allowed_users(allowed_roles=['sigp_dgaf','sigp_gabm','sigp_admin'])
def ProcLetEdit(request, hashid, page):
    group = get_roles(request)
    obj = get_object_or_404(ProcLet, hashed=hashid)
    proc = obj.proc
    proj = proc.proj
    if request.method == 'POST':
        form = ProcLetForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Altera ona.')
            if page == "req": 
                if 'sigp_dgaf' in group: return redirect('dgaf-proc-req-det', hashid=proc.hashed)
                elif 'sigp_gabm' in group: return redirect('gab-proc-req-det', hashid=proc.hashed)
            elif page == "res": 
                if 'sigp_dgaf' in group: return redirect('dgaf-proc-res-det', hashid=proc.hashed)
                elif 'sigp_gabm' in group: return redirect('gab-proc-res-det', hashid=proc.hashed)
    else: form = ProcLetForm(instance=obj)
    context = {
        'group': group, 'proj': proj, 'proc': proc, 'form': form, 'page': 'letter',
        'title': 'Altera Karta', 'legend': 'Altera Karta'
    }
    return render(request, 'proc/form.html', context)

@allowed_users(allowed_roles=['sigp_dgaf','sigp_gabm','sigp_admin'])
def ProcLetRem(request, pk, page):
    group = get_roles(request)
    obj = get_object_or_404(ProcLet, pk=pk)
    proc = obj.proc
    obj.delete()
    messages.success(request, f'Hapaga ona.')
    if page == "req": 
        if 'sigp_dgaf' in group: return redirect('dgaf-proc-req-det', hashid=proc.hashed)
        elif 'sigp_gabm' in group: return redirect('gab-proc-req-det', hashid=proc.hashed)
    elif page == "res": 
        if 'sigp_dgaf' in group: return redirect('dgaf-proc-res-det', hashid=proc.hashed)
        elif 'sigp_gabm' in group: return redirect('gab-proc-res-det', hashid=proc.hashed)