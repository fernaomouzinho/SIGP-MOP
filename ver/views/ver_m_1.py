import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles
from django.contrib import messages
from django.db import IntegrityError
from custom.models import Section
from eval.models import Eval
from ver.models import Ver, VerSecEng, VerTracks, VerSecEngEmployee
from ver.forms import VerForm, VerForm2, VerForm3, VerSecForm, VerSecForm2, VerEngForm
from conf.user_utils import c_user_sec, c_user_eng
from conf.utils import getnewid, write_roman


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipVerAdd(request, hashid):
    group = get_roles(request)
    eval = get_object_or_404(Eval, hashed=hashid)
   
    if request.method == 'POST':
        newid, new_hashid = getnewid(Ver)
        form = VerForm(request.POST or None, request.FILES or None)
        mt = datetime.datetime.today().month
        yr = datetime.datetime.today().year
        rom_num = write_roman(mt)
        if form.is_valid():
            
            try:
                instance = form.save(commit=False)
                data = form.cleaned_data
                number = data['number']
                eval_number  = "%s/%s-MOP/%s/%s" % (number,group.upper(),rom_num,yr)
                
                if Ver.objects.filter(number=eval_number).exists():
                    form.add_error('number', f"'{eval_number}' eziste ona.")
               
                else:    
                    instance.id = newid
                    instance.number = eval_number
                    instance.eval = eval
                    instance.datetime = datetime.datetime.now()
                    instance.user = request.user
                    instance.hashed = new_hashid
                    instance.save()
                    track = VerTracks.objects.all().last()
                    track.is_start = True
                    track.date_start = datetime.datetime.now()
                    track.save()
                    messages.success(request, f'Aumenta ona.')
                    return redirect('uvip-eval-list2', hashid=hashid)
            
            except IntegrityError as e:
            # Friendly message for duplicate
                form.add_error('number', f"'{number}' eziste ona.")
    
    else: form = VerForm()
    context = {
        'group':group, 'eval':eval, 'form':form,
        'title':f'Kria Despaxu', 'legend':f'Kria Despaxu'
    }
    return render(request, 'ver/form.html', context)


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipVerEdit(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(Ver, hashed=hashid)
    eval = obj.eval
    if request.method == 'POST':
        form = VerForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera susesu.')
            return redirect('uvip-ver-det', hashid=hashid)
    else: form = VerForm(instance=obj)
    context = {
        'group':group, 'eval':eval, 'obj':obj, 'form':form,
        'title':f'Altera Despaxu', 'legend':f'Altera Despaxu'
    }
    return render(request, 'ver/form.html', context)


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipVerEdit2(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(Ver, hashed=hashid)
    cont = obj.cont
    if request.method == 'POST':
        form = VerForm2(cont, request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Adisiona susesu.')
            return redirect('div-ver-let-det', hashid=hashid)
    else: form = VerForm2(cont, instance=obj)
    context = {
        'group': group, 'cont': cont, 'obj': obj, 'form': form,
        'title': f'Adisiona Resibu', 'legend': f'Adisiona Resibu'
    }
    return render(request, 'verletter/form2.html', context)


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipVerRem(request, pk):
    obj = get_object_or_404(Ver, pk=pk)
    eval = obj.eval
    obj.delete()
    messages.success(request, f'Hamos ona.')
    return redirect('uvip-eval-list2', hashid=eval.hashed)


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipVerSend(request, hashid):
    ver = get_object_or_404(Ver, hashed=hashid)
    ver.is_send = True
    ver.is_back = False
    ver.back_comment = None
    ver.save()
    track = VerTracks.objects.filter(ver=ver).first()
    track.is_uvip_out = True
    track.date_uvip_out = datetime.datetime.now()
    track.percent = 11
    track.stages = f"UIVP ba {ver.sec.code}"
    track.save()
    messages.success(request, f'UIVP ba {ver.sec.code}.')
    return redirect('uvip-ver-det', hashid=hashid)
###

@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secVerBack1(request, hashid):
    group = get_roles(request)
    ver = get_object_or_404(Ver, hashed=hashid)
    track = VerTracks.objects.filter(ver=ver).first()	
    if request.method == 'POST':
        form = VerForm3(request.POST, instance=ver)
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
            track.stages = f"Husi {ver.sec.code} fila ba UIVP"
            track.save()
            messages.success(request, f'Husi {ver.sec.code} fila ba UIVP.')
            return redirect('sec-ver-det', hashid=hashid)
    else: form = VerForm3(instance=ver)
    context = {
        'group': group, 'ver': ver, 'form': form,
        'title': f'Komentariu Fila', 'legend': f'Komentariu Fila'
    }
    return render(request, 'verletter/form4.html', context)


@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secVerIn1(request, hashid):
    ver = get_object_or_404(Ver, hashed=hashid)
    ver.is_read = True
    ver.save()
    track = VerTracks.objects.filter(ver=ver).first()
    track.is_sec_in_1 = True
    track.date_sec_in_1 = datetime.datetime.now()
    track.percent = 22
    track.stages = f"Husi UIVP mai {ver.sec.code}"
    track.save()
    messages.success(request, f'Husi UIVP mai {ver.sec.code}.')
    return redirect('sec-ver-det', hashid=hashid)


@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secVerAdd(request, hashid):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    ver = get_object_or_404(Ver, hashed=hashid)
    if request.method == 'POST':
        newid, new_hashid = getnewid(VerSecEng)
        form = VerSecForm(sec, request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.ver = ver
            instance.epos = ver.epos
            instance.number = ver.number
            instance.sec = sec
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            instance.to.set(form.cleaned_data['to'])
            instance.save()
            messages.success(request, f'Kria succesu.')
            return redirect('sec-ver-det', hashid=hashid)
    else: form = VerSecForm(sec)
    context = {
        'group': group, 'ver': ver, 'form': form,
        'title': f'Kria Despaxu', 'legend': f'Kria Karta Despaxu'
    }
    return render(request, 'ver/form2.html', context)

@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secVerEdit(request, hashid):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    obj = get_object_or_404(VerSecEng, hashed=hashid)
    ver = obj.ver
    if request.method == 'POST':
        form = VerSecForm(sec, request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.ver = ver
            instance.number = ver.number
            instance.sec = sec
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            instance.to.set(form.cleaned_data['to'])
            instance.save()
            messages.success(request, f'Altera succesu.')
            return redirect('sec-ver-det', hashid=ver.hashed)
    else: form = VerSecForm(sec, instance=obj)
    context = {
        'group': group, 'ver': ver, 'form': form,
        'title': f'Altera Despaxu', 'legend': f'Altera Despaxu'
    }
    return render(request, 'ver/form2.html', context)


@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secVerRem(request, pk):
    obj = get_object_or_404(VerSecEng, pk=pk)
    ver = obj.ver
    obj.delete()
    messages.success(request, f'Hapaga ona.')
    return redirect('sec-ver-let-det', hashid=ver.hashed)


@allowed_users(allowed_roles=['sigp_sec','sigp_admin'])
def secVerSend(request, pk):
    sec = c_user_sec(request.user)
    obj = get_object_or_404(VerSecEng, pk=pk)
    emp=obj.to.all()
    ver = obj.ver
    obj.is_send = True
    obj.save()
    track = VerTracks.objects.filter(ver=ver).first()
    track.is_sec_out_1 = True
    track.date_sec_out_1 = datetime.datetime.now()
    track.is_sec_in_2 = False
    track.date_sec_in_2 = None
    track.is_eng_in = False
    track.date_eng_in = None
    track.is_eng_out = False
    track.date_eng_out = None
    track.percent = 33
    track.stages = f"{sec.code} ba Enjineiru {emp[0]}"
    track.save()
    messages.success(request, f'{sec.code} ba {emp[0]}.')
    return redirect('sec-ver-det', hashid=ver.hashed)

#

@allowed_users(allowed_roles=['sigp_eng','sigp_admin'])
def engVerIn(request, hashid):
    versec = get_object_or_404(VerSecEng, hashed=hashid)
    verseceng = VerSecEngEmployee.objects.filter(verseceng=versec).select_related('employee')
    # Get the names of the employees
    employee_names = [ve.employee.name for ve in verseceng]
    versec.is_send_read = True
    versec.save()
    ver = versec.ver
    track = VerTracks.objects.filter(ver=ver).first()
    track.is_eng_in = True
    track.date_eng_in = datetime.datetime.now()
    track.percent = 44
    track.stages = f"Husi {versec.sec.code} mai Enjineiru {employee_names[0]}."
    track.save()
    messages.success(request, f'Husi {versec.sec.code} mai Enjineiru {employee_names[0]}.')
    return redirect('eng-ver-det', hashid=hashid)


@allowed_users(allowed_roles=['sigp_eng','sigp_admin'])
def engVerEdit(request, hashid):
    group = get_roles(request)
    sec = c_user_sec(request.user)
    versec = get_object_or_404(VerSecEng, hashed=hashid)
    if request.method == 'POST':
        form = VerEngForm(request.POST, request.FILES, instance=versec)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera succesu.')
            return redirect('eng-ver-det', hashid=hashid)
    else: form = VerEngForm(instance=versec)
    context = {
        'group': group, 'versec': versec, 'form': form, 'page': 'sec',
        'title': f'Altera Komentariu', 'legend': f'Altera Komentariu'
    }
    return render(request, 'ver/form.html', context)


@allowed_users(allowed_roles=['sigp_eng','sigp_admin'])
def engVerSend(request, hashid):
    eng = c_user_eng(request.user)
    sec = eng.employeediv.sec
    versec = get_object_or_404(VerSecEng, hashed=hashid)
    verseceng = VerSecEngEmployee.objects.filter(verseceng=versec).select_related('employee')
    # Get the names of the employees
    employee_names = [ve.employee.name for ve in verseceng]
    versec.is_send_read = True
    versec.is_eng_back = True
    versec.is_eng_read = False
    versec.save()
    ver = versec.ver
    track = VerTracks.objects.filter(ver=ver).first()
    track.is_eng_out = True
    track.date_eng_out = datetime.datetime.now()
    track.percent = 56
    track.stages = f"Husi Enjineiru {employee_names[0]} ba {versec.sec.code}"
    track.save()
    messages.success(request, f'Husi Enjineiru {employee_names[0]} ba {versec.sec.code}.')
    return redirect('eng-ver-det', hashid=hashid)