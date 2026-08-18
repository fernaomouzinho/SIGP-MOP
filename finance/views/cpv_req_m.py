import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conf.decorators import allowed_users
from finance.models import CPVReq, CPVReqTrack
from finance.forms import CPVReqForm, CPVReqForm2
from conf.user_utils import c_user_div, c_user_dna, c_user_dnof
from conf.utils import getnewid, write_roman
from django.core.exceptions import ObjectDoesNotExist

#dnof
@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVReqAdd(request):
    group = request.user.groups.all()[0].name
    if group == "dnof": div = c_user_dnof(request.user)
    
    if request.method == 'POST':
        newid, new_hashid = getnewid(CPVReq)
        form = CPVReqForm(request.POST, request.FILES)
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
            #instance.number = "%s/%s-%s-MOP/%s/%s" % (number,dv,dg,rom_num,yr)
            instance.number = number
            num= instance.number
            try:
                p = CPVReq.objects.get(number=num)
                messages.warning(request, f'Numeru referensia %s eziste ona. Favor prense ho numeru refencia seluk' % (number))
                return redirect('dnof-cpvreq-add')
            
            except ObjectDoesNotExist:
                instance.datetime = datetime.datetime.now()
                instance.user = request.user
                instance.hashed = new_hashid
                instance.save()
                messages.success(request, f'Aumenta susesu.')
                return redirect('dnof-cpvreq-det', hashid=new_hashid)
    else: form = CPVReqForm()
    context = {
        'group': group, 'form': form,
        'title': 'Aumenta Rekizasaun CPV', 'legend': 'Aumenta Rekizasaun CPV'
    }
    return render(request, 'finance_cpv/form_req.html', context)

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVReqEdit(request, hashid):
    group = request.user.groups.all()[0].name
    obj = get_object_or_404(CPVReq, hashed=hashid)
    if request.method == 'POST':
        form = CPVReqForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera susesu.')
            return redirect('dnof-cpvreq-det', hashid=hashid)
    else: form = CPVReqForm(instance=obj)
    context = {
        'group': group, 'obj':obj, 'form': form, 'page':'det',
        'title': 'Altera Rekizasaun CPV', 'legend': 'Altera Rekizasaun CPV'
    }
    return render(request, 'finance_cpv/form_req.html', context)

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVReqRem(request, pk):
    obj = get_object_or_404(CPVReq, pk=pk)
    obj.delete()
    messages.success(request, f'Hapaga susesu.')
    return redirect('dnof-cpvreq-list')

@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVReqSend(request, pk):
    obj = get_object_or_404(CPVReq, pk=pk)
    obj.is_send = True
    obj.is_back = False
    obj.comment = None
    obj.status = "Manda ba DGAF"
    obj.save()
    track = CPVReqTrack.objects.filter(cpvreq=obj).first()
    track.is_dnof_out = True
    track.date_dnof_out = datetime.datetime.now()
    track.stages = "DNOF ba DGAF"
    track.percent = 25
    track.save()
    messages.success(request, f'DNOF ba DGAF.')
    return redirect('dnof-cpvreq-det', hashid=obj.hashed)
# dgaf
@login_required
@allowed_users(allowed_roles=['dgaf'])
def dgafCPVReqBack(request, hashid):
    group = request.user.groups.all()[0].name
    obj = get_object_or_404(CPVReq, hashed=hashid)
    track = CPVReqTrack.objects.filter(cpvreq=obj).first()
    if request.method == 'POST':
        form = CPVReqForm2(request.POST, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_back = True
            instance.is_send = False
            instance.is_read = False
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            obj.status = "DGAF Manda Fila"
            obj.save()
            track.is_dnof_out = False
            track.date_dnof_out = None
            track.stages = "DGAF fila ba DNOF"
            track.percent = 0
            track.save()
            messages.success(request, f'DGAF fila ba DNOF.')
            return redirect('dgaf-cpvreq-det', hashid=hashid)
    else: form = CPVReqForm2(instance=obj)
    context = {
        'group': group, 'obj': obj, 'form': form, 'page':'det',
        'title': 'Komentariu Manda Fila', 'legend': 'Komentariu Manda Fila'
    }
    return render(request, 'finance_cpv/form_req.html', context)

@login_required
@allowed_users(allowed_roles=['dgaf'])
def dgafCPVReqIn(request, pk):
    obj = get_object_or_404(CPVReq, pk=pk)
    obj.is_read = True
    obj.status = "DGAF Simu"
    obj.save()
    track = CPVReqTrack.objects.filter(cpvreq=obj).first()
    track.is_dgaf_in = True
    track.date_dgaf_in = datetime.datetime.now()
    track.stages = "DGAF Simu"
    track.percent = 50
    track.save()
    messages.success(request, f'DGAF Simu.')
    return redirect('dgaf-cpvreq-det', hashid=obj.hashed)

@login_required
@allowed_users(allowed_roles=['dgaf'])
def dgafCPVReqAppr(request, pk):
    obj = get_object_or_404(CPVReq, pk=pk)
    obj.is_appr = True
    obj.status = "DGAF Aprova"
    obj.save()
    track = CPVReqTrack.objects.filter(cpvreq=obj).first()
    track.is_appr = True
    track.date_appr = datetime.datetime.now()
    track.stages = "DGAF Aprova"
    track.percent = 75
    track.save()
    messages.success(request, f'DGAF Aprova.')
    return redirect('dgaf-cpvreq-det', hashid=track.cpvreq.hashed)
# dnof
@login_required
@allowed_users(allowed_roles=['dnof'])
def dnofCPVReqEnd(request, pk):
    obj = get_object_or_404(CPVReq, pk=pk)
    obj.is_end = True
    obj.status = "Aprovadu & Termina"
    obj.save()
    track = CPVReqTrack.objects.filter(cpvreq=obj).first()
    track.is_end = True
    track.date_end = datetime.datetime.now()
    track.stages = "Rekizasaun Termina"
    track.percent = 100
    track.save()
    messages.success(request, f'Rekizasaun Termina.')
    return redirect('dnof-cpvreq-det', hashid=obj.hashed)
