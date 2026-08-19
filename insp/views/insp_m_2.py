import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.contrib import messages
from insp.models import Insp, InspSecEng, InspTracks, InspSecEngEmployee
from insp.forms import InspForm2, InspSecForm2
from conf.user_utils import c_user_sec, c_user_eng
from conf.utils import getnewid
from invoice.models import InvTrack
from users.decorators import allowed_users
from sigp.utils import get_roles

### SEC
@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secInspIn2(request, hashid):
    inspsec = get_object_or_404(InspSecEng, hashed=hashid)
    inspseceng = InspSecEngEmployee.objects.filter(inspseceng=inspsec).select_related('employee')
    employee_names = [ve.employee.name for ve in inspseceng]
    inspsec.is_eng_read = True
    inspsec.save()
    insp = inspsec.insp
    track = InspTracks.objects.filter(insp=insp).first()
    track.is_sec_in_2 = True
    track.date_sec_in_2 = datetime.datetime.now()
    track.percent = 67
    track.stages = f"Husi {employee_names} mai {inspsec.sec.code}"
    track.save()
    messages.success(request, f'Husi {employee_names} mai {inspsec.sec.code}.')
    return redirect('sec-insp-det', hashid=insp.hashed)

@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secInspCommEdit(request, hashid):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    inspsec = get_object_or_404(InspSecEng, hashed=hashid)
    insp = inspsec.insp
    if request.method == 'POST':
        form = InspSecForm2(request.POST, request.FILES, instance=inspsec)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'succesu.')
            return redirect('sec-insp-det', hashid=insp.hashed)
    else: form = InspSecForm2(instance=inspsec)
    context = {
        'group': group, 'insp': insp, 'form': form,
        'title': f'Aneksu Komentariu', 'legend': f'Aneksu Komentariu'
    }
    return render(request, 'insp/form.html', context)

@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secInspEnd(request, pk):
    obj = get_object_or_404(InspSecEng, pk=pk)
    obj.is_end = True
    obj.save()
    messages.success(request, f'Despaxu Seksaun Termina.')
    return redirect('sec-insp-det', hashid=obj.insp.hashed)

@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secInspBack(request, pk):
    obj = get_object_or_404(InspSecEng, pk=pk)
    obj.is_back = True
    obj.save()
    insp = obj.insp
    track = InspTracks.objects.filter(insp=insp).first()
    track.is_sec_out_2 = True
    track.date_sec_out_2 = datetime.datetime.now()
    track.percent = 78
    track.stages = f"Husi {obj.sec.code} ba UIVP"
    track.save()
    messages.success(request, f'Husi {obj.sec.code} ba UIVP.')
    return redirect('sec-insp-det', hashid=insp.hashed)

### UIVP
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipInspIn(request, hashid):
    inspsec = get_object_or_404(InspSecEng, hashed=hashid)
    inspsec.is_back_read = True
    inspsec.save()
    insp = inspsec.insp
    track = InspTracks.objects.filter(insp=insp).first()
    track.is_uvip_in = True
    track.date_uvip_in = datetime.datetime.now()
    track.percent = 89
    track.stages = f"Husi {inspsec.sec.code} mai UIVP"
    track.save()
    messages.success(request, f'Husi {inspsec.sec.code} mai UIVP.')
    return redirect('uvip-insp-det', hashid=insp.hashed)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipInspCommEdit(request, hashid):
    group = request.user.groups.all()[0].name
    insp = get_object_or_404(Insp, hashed=hashid)
    if request.method == 'POST':
        form = InspForm2(request.POST, request.FILES, instance=insp)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'susesu.')
            return redirect('uvip-insp-det', hashid=hashid)
    else: form = InspForm2(instance=insp)
    context = {
        'group': group, 'insp':insp, 'inv':insp.inv, 'form':form, 'page':'back',
        'title': f'Aneksu Komentariu', 'legend': f'Aneksu Komentariu'
    }
    return render(request, 'insp/form.html', context)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipInspEnd(request, hashid):
    insp = get_object_or_404(Insp, hashed=hashid)
    insp.is_end = True
    insp.save()
    inv  = insp.inv
    invtrack = InvTrack.objects.filter(inv=inv).first()
    invtrack.is_insp_end = True
    invtrack.date_insp_end = datetime.datetime.now()
    invtrack.save()
    track = InspTracks.objects.filter(insp=insp).first()
    track.is_end = True
    track.date_end = datetime.datetime.now()
    track.percent = 100
    track.stages = f"Inspesaun Termina"
    track.save()
    messages.success(request, f'Inspesaun Termina.')
 
    return redirect('uvip-insp-det', hashid=hashid)