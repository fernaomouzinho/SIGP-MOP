import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.contrib import messages
from django.db import IntegrityError
from invoice.models import Invoice
from insp.models import Insp, InspSecEng, InspTracks, InspSecEngEmployee
from insp.forms import InspForm, InspForm2, InspForm3, InspSecForm, InspSecForm2, InspEngForm
from conf.user_utils import c_user_sec, c_user_eng
from conf.utils import getnewid, write_roman
from users.decorators import allowed_users
from sigp.utils import get_roles

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipInspAdd(request, hashid):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    if request.method == 'POST':
        newid, new_hashid = getnewid(Insp)
        form = InspForm(request.POST, request.FILES)
        mt = datetime.datetime.today().month
        yr = datetime.datetime.today().year
        rom_num = write_roman(mt)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                data = form.cleaned_data
                number = data['number']
                insp_number = "%s/%s-MOP/%s/%s" % (number,group.upper(),rom_num,yr)
                
                if Insp.objects.filter(number=insp_number).exists():
                     form.add_error('number', f"'{insp_number}' eziste ona.")
                else:
                    instance.id = newid
                    instance.number = insp_number
                    instance.inv = inv
                    instance.cont = inv.cont
                    instance.datetime = datetime.datetime.now()
                    instance.user = request.user
                    instance.hashed = new_hashid
                    insp = Insp.objects.all()
                    instance.save()
                    messages.success(request, f'Aumenta ona.')
                    return redirect('uvip-insp-list', hashid=hashid)
            except IntegrityError as e:
                form.add_error('number', f"'{number}' eziste ona.")
                
    else: form = InspForm()
    context = {
        'group':group, 'inv':inv, 'form':form,
        'title':f'Kria Despaxu', 'legend':f'Kria Despaxu'
    }
    return render(request, 'insp/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipInspEdit(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(Insp, hashed=hashid)
    cont = obj.cont
    inv = obj.inv
    if request.method == 'POST':
        form = InspForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            try: 
                instance = form.save(commit=False)
                data = form.cleaned_data
                number = data['number']
                if Insp.objects.filter(number=number).exclude(pk=obj.pk).exists():
                    form.add_error('number', f"'{number}' eziste ona.")
                else:
                    instance.datetime = datetime.datetime.now()
                    instance.user = request.user
                    instance.save()
                    messages.success(request, f'Altera susesu.')
                return redirect('uvip-insp-det', hashid=hashid)
            except IntegrityError as e:
                form.add_error('number', f"'{number}' eziste ona.")
    else: form = InspForm(instance=obj)
    context = {
        'group':group, 'cont':cont, 'obj':obj, 'inv':inv, 'form':form,
        'title':f'Altera Despaxu', 'legend':f'Altera Despaxu'
    }
    return render(request, 'insp/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipInspEdit2(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(Insp, hashed=hashid)
    cont = obj.cont
    if request.method == 'POST':
        form = InspForm2(cont, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Adiciona susesu.')
            return redirect('div-insp-let-det', hashid=hashid)
    else: form = InspForm2(cont, instance=obj)
    context = {
        'group': group, 'cont': cont, 'obj': obj, 'form': form,
        'title': f'Adiciona Resibu', 'legend': f'Adiciona Resibu'
    }
    return render(request, 'insp/form2.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipInspRem(request, pk):
    obj = get_object_or_404(Insp, pk=pk)
    inv = obj.inv
    obj.delete()
    messages.success(request, f'Hamos ona.')
    return redirect('uvip-insp-list', hashid=inv.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipInspSend(request, hashid):
    insp = get_object_or_404(Insp, hashed=hashid)
    insp.is_send = True
    insp.is_back = False
    insp.back_comment = None
    insp.save()
    track = InspTracks.objects.filter(insp=insp).first()
    track.is_start = True
    track.date_start = datetime.datetime.now()
    track.is_uvip_out = True
    track.date_uvip_out = datetime.datetime.now()
    track.percent = 11
    track.stages = f"UIVP ba {insp.sec.code}"
    track.save()
    messages.success(request, f'UIVP ba {insp.sec.code}.')
    return redirect('uvip-insp-det', hashid=hashid)
###
@login_required
@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secInspBack1(request, hashid):
    group = get_roles(request)
    insp = get_object_or_404(Insp, hashed=hashid)
    track = InspTracks.objects.filter(insp=insp).first()	
    if request.method == 'POST':
        form = InspForm3(request.POST, instance=insp)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_send = False
            instance.is_read = False
            instance.is_back = True
            instance.save()
            
            track.is_sec_in_1 = False
            track.date_sec_in_1 = None
            track.is_uvip_out = False
            track.date_uvip_out = None
            track.percent = 0
            track.stages = f"Husi {insp.sec.code} fila ba UIVP"
            track.save()
            messages.success(request, f'Husi {insp.sec.code} fila ba UIVP.')
            return redirect('sec-indp-det', hashid=hashid)
    else: form = InspForm3(instance=insp)
    context = {
        'group': group, 'insp': insp, 'form': form,
        'title': f'Komentariu Fila', 'legend': f'Komentariu Fila'
    }
    return render(request, 'insp/form4.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secInspIn1(request, hashid):
    insp = get_object_or_404(Insp, hashed=hashid)
    insp.is_read = True
    insp.save()
    track = InspTracks.objects.filter(insp=insp).first()
    track.is_sec_in_1 = True
    track.date_sec_in_1 = datetime.datetime.now()
    track.percent = 22
    track.stages = f"Husi UIVP mai {insp.sec.code}"
    track.save()
    messages.success(request, f'Husi UIVP mai {insp.sec.code}.')
    return redirect('sec-insp-det', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secInspAdd(request, hashid):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    insp = get_object_or_404(Insp, hashed=hashid)
    if request.method == 'POST':
        newid, new_hashid = getnewid(InspSecEng)
        form = InspSecForm(sec, request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.insp = insp
            instance.number = insp.number
            instance.sec = sec
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            
            instance.to.set(form.cleaned_data['to'])
            instance.save()
            messages.success(request, f'Kria susesu.')
            return redirect('sec-insp-det', hashid=hashid)
    else: form = InspSecForm(sec)
    context = {
        'group': group, 'insp': insp, 'form': form,
        'title': f'Kria Despaxu', 'legend': f'Kria Karta Despaxu'
    }
    return render(request, 'insp/form2.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secInspEdit(request, hashid):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    obj = get_object_or_404(InspSecEng, hashed=hashid)
    insp = obj.insp
    if request.method == 'POST':
        form = InspSecForm(sec, request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.insp = insp
            instance.number = insp.number
            instance.sec = sec
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            instance.to.set(form.cleaned_data['to'])
            instance.save()
            messages.success(request, f'Altera susesu.')
            return redirect('sec-insp-det', hashid=insp.hashed)
    else: form = InspSecForm(sec, instance=obj)
    context = {
        'group': group, 'insp': insp, 'form': form,
        'title': f'Altera Despaxu', 'legend': f'Altera Despaxu'
    }
    return render(request, 'insp/form2.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secInspRem(request, pk):
    obj = get_object_or_404(InspSecEng, pk=pk)
    insp = obj.insp
    obj.delete()
    messages.success(request, f'Hamos ona.')
    return redirect('sec-insp-let-det', hashid=insp.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secInspSend(request, pk):
    sec = c_user_sec(request.user)
    obj = get_object_or_404(InspSecEng, pk=pk)
    inspseceng = InspSecEngEmployee.objects.filter(inspseceng=obj).select_related('employee')
    employee_names = [ve.employee.name for ve in inspseceng]
    insp = obj.insp
    obj.is_send = True
    obj.save()
    track = InspTracks.objects.filter(insp=insp).first()
    track.is_sec_out_1 = True
    track.date_sec_out_1 = datetime.datetime.now()
    track.is_sec_in_2 = False
    track.date_sec_in_2 = None
    track.is_eng_in = False
    track.date_eng_in = None
    track.is_eng_out = False
    track.date_eng_out = None
    track.percent = 33
    
    track.stages = f"Husi {sec.code} ba {employee_names}"
    
    track.save()
    messages.success(request, f'Husi {sec.code} ba {employee_names}.')
    return redirect('sec-insp-det', hashid=insp.hashed)
#
@login_required
@allowed_users(allowed_roles=['sigp_eng','sigp_admin'])
def engInspIn(request, hashid):
    inspsec = get_object_or_404(InspSecEng, hashed=hashid)
    inspseceng = InspSecEngEmployee.objects.filter(inspseceng=inspsec).select_related('employee')
    employee_names = [ve.employee.name for ve in inspseceng]
    inspsec.is_send_read = True
    inspsec.save()
    insp = inspsec.insp
    track = InspTracks.objects.filter(insp=insp).first()
    track.is_eng_in = True
    track.date_eng_in = datetime.datetime.now()
    track.percent = 44
    track.stages = f"Husi {inspsec.sec.code} mai {employee_names}."
    track.save()
    messages.success(request, f'Husi {inspsec.sec.code} mai {employee_names}.')
    return redirect('eng-insp-det', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['sigp_eng','sigp_admin'])
def engInspEdit(request, hashid):
    group = request.user.groups.all()[0].name
    sec = c_user_sec(request.user)
    inspsec = get_object_or_404(InspSecEng, hashed=hashid)
    if request.method == 'POST':
        form = InspEngForm(request.POST, request.FILES, instance=inspsec)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera susesu.')
            return redirect('eng-insp-det', hashid=hashid)
    else: form = InspEngForm(instance=inspsec)
    context = {
        'group': group, 'inspsec': inspsec, 'form': form, 'page': 'sec',
        'title': f'Altera Komentariu', 'legend': f'Altera Komentariu'
    }
    return render(request, 'insp/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_eng','sigp_admin'])
def engInspSend(request, hashid):
    eng = c_user_eng(request.user)
    sec = eng.employeediv.sec
    inspsec = get_object_or_404(InspSecEng, hashed=hashid)
    inspseceng = InspSecEngEmployee.objects.filter(inspseceng=inspsec).select_related('employee')
    # Get the names of the employees
    employee_names = [ve.employee.name for ve in inspseceng]
    inspsec.is_send_read = True
    inspsec.is_eng_back = True
    inspsec.is_eng_read = False
    inspsec.save()
    insp = inspsec.insp
    track = InspTracks.objects.filter(insp=insp).first()
    track.is_eng_out = True
    track.date_eng_out = datetime.datetime.now()
    track.percent = 56
    track.stages = f"Husi {employee_names} ba {inspsec.sec.code}"
    track.save()
    messages.success(request, f'Husi {employee_names} ba {inspsec.sec.code}.')
    return redirect('eng-insp-det', hashid=hashid)