import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.contrib import messages
from django.db import IntegrityError
from contract.models import Contract, Amendment
from invoice.models import Invoice, InvLet, InvLetAdnBack, CertPay
from invoice.forms import InvLetForm, InvLetForm3
from conf.user_utils import c_user_sup, c_user_div, c_user_dnof, c_user_dna, c_user_dgaf, c_user_min, c_user_sup
from conf.utils import getnewid, write_roman
from users.decorators import allowed_users
from sigp.utils import get_roles

### SUP
@login_required
@allowed_users(allowed_roles=['sigp_sup'])
def supInvLetAdd(request, hashid):
    group = get_roles(request)
    if 'sigp_div' in group: div = c_user_div(request.user)
    elif 'sigp_dna' in group: div = c_user_dna(request.user)
    elif 'sigp_dnof' in group: div = c_user_dnof(request.user)
    elif 'sigp_sup' in group: div = c_user_dnof(request.user)

    mun = c_user_sup(request.user)
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    amend = Amendment.objects.filter(contract=cont).first()
    if request.method == 'POST':
        newid, new_hashid = getnewid(InvLet)
        form = InvLetForm(group, request.POST, request.FILES)
        mt = datetime.datetime.today().month
        yr = datetime.datetime.today().year
        dv = div.code
        dg = div.dg.code
        rom_num = write_roman(mt)
       
  
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                data = form.cleaned_data
                number = data['number']
                #inv_number = "%s/%s_%s-%s-%s-MOP/%s/%s" % (number,group.upper(),mun, dv,dg,rom_num,yr)
                
                if InvLet.objects.filter(number=number).exists():
                    form.add_error('number', f"'{number}' eziste ona.")
                else:
                    instance.id = newid
                    instance.inv = inv
                    instance.cont = inv.cont
                    instance.mun = mun
                    instance.is_sup = True
                    data = form.cleaned_data
                    instance.number = number
                    instance.datetime = datetime.datetime.now()
                    instance.user = request.user
                    instance.hashed = new_hashid
                    instance.save()
                    messages.success(request, f'Aumenta susesu.')
                    return redirect('sup-inv-det', hashid=hashid)
                
            except IntegrityError as e:
                form.add_error('number', f"'{number}' eziste ona.")
                
    else: form = InvLetForm(group)
    context = {
        'group': group, 'inv': inv, 'amend':amend, 'form': form, 'page': 'pdet',
        'title': 'Aumenta Karta', 'legend': 'Aumenta Karta'
    }
    return render(request, 'inv_let/form_let.html', context)





@login_required
@allowed_users(allowed_roles=['sigp_sup'])
def supInvLetEdit(request, hashid, pk):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    obj = get_object_or_404(InvLet, pk=pk)
    cont = inv.cont
    amend = Amendment.objects.filter(contract=cont).first()
    if request.method == 'POST':
        form = InvLetForm(group, request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera susesu.')
            return redirect('sup-inv-det', hashid=hashid)
    else: form = InvLetForm(group, instance=obj)
    context = {
        'group': group, 'inv': inv, 'amend':amend, 'form': form, 'page': 'pdet',
        'title': 'Altera Karta', 'legend': 'Altera Karta'
    }
    return render(request, 'inv_let/form_let.html', context)





@login_required
@allowed_users(allowed_roles=['sigp_sup'])
def supInvLetRem(request, hashid, pk):
    obj = get_object_or_404(InvLet, pk=pk)
    obj.delete()
    messages.success(request, f'Hamos ona.')
    return redirect('sup-inv-det', hashid=hashid)
### LET
@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_gab','sigp_dgaf','sigp_dna','sigp_dnof'])
def InvLetAdd(request, hashid):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    cont = inv.cont
    amend = Amendment.objects.filter(contract=cont).first()
    txt_cov = "Karta"
    if group == 'min': txt_cov = "Despaxu"
    if request.method == 'POST':
        newid, new_hashid = getnewid(InvLet)
        form = InvLetForm(group, request.POST, request.FILES)
        mt = datetime.datetime.today().month
        yr = datetime.datetime.today().year
        rom_num = write_roman(mt)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.inv = inv
            instance.cont = inv.cont
            if group == 'uivp': 
                instance.is_uvip = True
            elif group == 'gab': 
                instance.is_gab = True
            elif group == 'dgaf': 
                instance.is_dgaf = True
            elif group == 'dna': 
                instance.is_dna = True
            elif group == 'dnof': 
                instance.is_dnof = True
            data = form.cleaned_data
            number = data['number']
            instance.number = "%s/%s-MOP/%s/%s" % (number,group.upper(),rom_num,yr)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Aumenta ona.')
            if 'sigp_uivp' in group:  return redirect('uvip-inv-det', hashid=hashid)
            elif 'sigp_gabm' in group:  return redirect('gab-inv-det', hashid=hashid)
            elif 'sigp_dgaf' in group:  return redirect('dgaf-inv-det', hashid=hashid)
            elif 'sigp_dna' in group:  return redirect('dna-inv-det', hashid=hashid)
            elif 'sigp_dnof' in group:  return redirect('dnof-inv-det', hashid=hashid)
            
    else: form = InvLetForm(group)
    context = {
        'group': group, 'inv': inv, 'amend':amend, 'form': form,
        'title': f'Aumenta {txt_cov}', 'legend': f'Aumenta {txt_cov}'
    }
    return render(request, 'inv_let/form_let.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_gab','sigp_dgaf','sigp_dna','sigp_dnof'])
def InvLetEdit(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(InvLet, hashed=hashid)
    inv = obj.inv
    amend = Amendment.objects.filter(contract=inv.cont).first()
    if request.method == 'POST':
        form = InvLetForm(group, request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Alterasaun susesu.')
            if 'sigp_uivp' in group:  return redirect('uvip-inv-det', hashid=hashid)
            elif 'sigp_gabm' in group:  return redirect('gab-inv-det', hashid=hashid)
            elif 'sigp_dgaf' in group:  return redirect('dgaf-inv-det', hashid=hashid)
            elif 'sigp_dna' in group:  return redirect('dna-inv-det', hashid=hashid)
            elif 'sigp_dnof' in group:  return redirect('dnof-inv-det', hashid=hashid)
    else: form = InvLetForm(group, instance=obj)
    context = {
        'group': group, 'inv': inv, 'amend':amend, 'form': form,
        'title': 'Altera Karta', 'legend': 'Altera Karta'
    }
    return render(request, 'inv_let/form_let.html', context)

@login_required
@allowed_users(allowed_roles=['sup','sigp_uivp','sigp_gab','sigp_dgaf','sigp_dna','sigp_dnof'])
def InvLetRem(request, pk):
    group = get_roles(request)
    obj = get_object_or_404(InvLet, pk=pk)
    inv = obj.inv
    obj.delete()
    messages.success(request, f'Hamos ona.')
    if 'sigp_uivp' in group:  return redirect('uvip-inv-det', hashid=inv.hashed)
    elif 'sigp_gabm' in group:  return redirect('gab-inv-det', hashid=inv.hashed)
    elif 'sigp_dgaf' in group:  return redirect('dgaf-inv-det', hashid=inv.hashed)
    elif 'sigp_dna' in group:  return redirect('dna-inv-det', hashid=inv.hashed)
    elif 'sigp_dnof' in group:  return redirect('dnof-inv-det', hashid=inv.hashed)
    
@login_required
@allowed_users(allowed_roles=['sigp_uivp'])
def uvipInvLetADNBackDev(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(InvLet, hashed=hashid)
    inv = obj.inv
    invs = obj.pk
    cont = obj.inv.cont
    certpay = CertPay.objects.filter(inv=obj.inv).values('number', 'number_req','total','date')
    invlet = InvLet.objects.filter().last()

    # fi = eval.proj.pcategory.id
    # if fi == 1: 
    #     track = EvalFITrack.objects.filter(eval=eval).first()
    # else: 
    #     track = EvalTrack.objects.filter(eval=eval).first()
    if request.method == 'POST':
        newid, new_hashid = getnewid(InvLetAdnBack)
        form = InvLetForm3(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.invlet = invlet
            instance.is_return = True
            instance.datetime = datetime.datetime.now().replace(second=0, microsecond=0)
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            obj.is_back = True
            obj.save()
            messages.success(request, f' UIVP.')
        return redirect('uvip-inv-det', hashid=inv.hashed)
    else: 
        form = InvLetForm3()
    context = {
        'group': group, 'inv':inv, 'cont':cont,'obj':obj, 'form':form,'certpay':certpay,
        'title': 'Komentariu Devolve', 'legend': 'Komentariu Devolve'
    }
    return render(request, 'inv_let/form_let_adn.html', context)

@login_required
@allowed_users(allowed_roles=['admin','sigp_uivp'])
def uvipInvLetADNReturnDev(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(InvLet, hashed=hashid)
    inv = obj.inv
    invs = obj.pk
    cont = obj.inv.cont
    certpay = CertPay.objects.filter(inv=obj.inv).values('number', 'number_req','total','date')
    invlet = InvLet.objects.filter().last()
    adnreturn = InvLetAdnBack.objects.filter(invlet=obj, is_return=True).first()

    context = {
        'group': group, 'inv':inv, 'cont':cont,'obj':obj, 'certpay':certpay,'adnreturn':adnreturn,
        'title': 'Komentariu Devolve', 'legend': 'Komentariu Devolve'
    }
    return render(request, 'report_recap/let_return_adn.html', context)