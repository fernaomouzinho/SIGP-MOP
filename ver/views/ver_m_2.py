import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles
from django.contrib import messages
from ver.models import Ver, VerSecEng, VerTracks, VerSecEngEmployee
from ver.forms import VerForm2, VerSecForm2
from conf.user_utils import c_user_sec, c_user_eng
from conf.utils import getnewid

### SEC
@login_required
@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secVerIn2(request, hashid):
    versec = get_object_or_404(VerSecEng, hashed=hashid)
    verseceng = VerSecEngEmployee.objects.filter(verseceng=versec).select_related('employee')
    # Get the names of the employees
    employee_names = [ve.employee.name for ve in verseceng]
    versec.is_eng_read = True
    versec.save()
    ver = versec.ver
    track = VerTracks.objects.filter(ver=ver).first()
    track.is_sec_in_2 = True
    track.date_sec_in_2 = datetime.datetime.now()
    track.percent = 67
    track.stages = f"Husi {employee_names[0]} mai {versec.sec.code}"
    track.save()
    messages.success(request, f'Husi {versec.to} mai {versec.sec.code}.')
    return redirect('sec-ver-det', hashid=ver.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secVerCommEdit(request, hashid):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    versec = get_object_or_404(VerSecEng, hashed=hashid)
    ver = versec.ver
    if request.method == 'POST':
        form = VerSecForm2(request.POST, request.FILES, instance=versec)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'succesu.')
            return redirect('sec-ver-det', hashid=ver.hashed)
    else: form = VerSecForm2(instance=versec)
    context = {
        'group': group, 'ver': ver, 'form': form,
        'title': f'Aneksu Komentariu', 'legend': f'Aneksu Komentariu'
    }
    return render(request, 'ver/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secVerEnd(request, pk):
    obj = get_object_or_404(VerSecEng, pk=pk)
    obj.is_end = True
    obj.save()
    messages.success(request, f'Despaxu Seksaun Termina.')
    return redirect('sec-ver-det', hashid=obj.ver.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secVerBack(request, pk):
    obj = get_object_or_404(VerSecEng, pk=pk)
    obj.is_back = True
    obj.save()
    ver = obj.ver
    track = VerTracks.objects.filter(ver=ver).first()
    track.is_sec_out_2 = True
    track.date_sec_out_2 = datetime.datetime.now()
    track.percent = 78
    track.stages = f"Husi {obj.sec.code} ba UIVP"
    track.save()
    messages.success(request, f'Husi {obj.sec.code} ba UIVP.')
    return redirect('sec-ver-det', hashid=ver.hashed)
### UIVP
@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipVerIn(request, hashid):
    versec = get_object_or_404(VerSecEng, hashed=hashid)
    versec.is_back_read = True
    versec.is_end = True
    versec.save()
    ver = versec.ver
    track = VerTracks.objects.filter(ver=ver).first()
    track.is_uvip_in = True
    track.date_uvip_in = datetime.datetime.now()
    track.percent = 89
    track.stages = f"Husi {versec.sec.code} mai UIVP"
    track.save()
    v = Ver.objects.get(hashed=versec.ver.hashed)
    v.is_back = True
    v.save()
    
    messages.success(request, f'Husi {versec.sec.code} mai UIVP.')
    return redirect('uvip-ver-det', hashid=ver.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipVerCommEdit(request, hashid):
    group = get_roles(request)
    ver = get_object_or_404(Ver, hashed=hashid)
    if request.method == 'POST':
        form = VerForm2(request.POST, request.FILES, instance=ver)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'susesu.')
            return redirect('uvip-ver-det', hashid=hashid)
    else: form = VerForm2(instance=ver)
    context = {
        'group': group, 'ver':ver, 'form':form, 'page':'back',
        'title': f'Aneksu Komentariu', 'legend': f'Aneksu Komentariu'
    }
    return render(request, 'ver/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipVerEnd(request, hashid):
    ver = get_object_or_404(Ver, hashed=hashid)
    ver.is_end = True
    ver.save()
    track = VerTracks.objects.filter(ver=ver).first()
    track.is_end = True
    track.date_end = datetime.datetime.now()
    track.percent = 100
    track.stages = f"Verifikasaun Termina"
    track.save()   
    messages.success(request, f'Verifikasaun Termina.')
 
    return redirect('uvip-eval-det', hashid=ver.eval.hashed)
