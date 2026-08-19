import datetime
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from custom.models import DG,Division
from eval.models import Eval, EvalLet, EvalTrack, EvalFITrack, EvalLetAdnBack
from eval.forms import EvalLetForm, EvalLetForm3,EvalLetForm4
from conf.user_utils import c_user_uvip
from conf.utils import getnewid,write_roman
from users.decorators import allowed_users
from sigp.utils import get_roles


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalLetAdd(request, hashid):
    group = get_roles(request)
    if 'sigp_uivp' in group: div = c_user_uvip(request.user)
    eval = get_object_or_404(Eval, hashed=hashid)
    
    if request.method == 'POST':
        newid, new_hashid = getnewid(EvalLet)
        form = EvalLetForm(request.POST, request.FILES,eval=eval)
        mt = datetime.datetime.today().month
        yr = datetime.datetime.today().year
        rom_num = write_roman(mt)
        
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                data = form.cleaned_data
                number = data['number']
                eval_number = "%s/%s-MOP/%s/%s" % (number,group.upper(),rom_num,yr)
                
                if EvalLet.objects.filter(number=eval_number).exists():
                    form.add_error('number', f"'{eval_number}' eziste ona.")
                else:
                    instance.id = newid
                    instance.number = eval_number
                    instance.eval = eval
                    instance.datetime = datetime.datetime.now()
                    instance.user = request.user
                    instance.hashed = new_hashid
                    instance.save()
                    messages.success(request, f'Aumenta ona.')
                return redirect('uvip-eval-det', hashid=hashid)
        
            except IntegrityError as e:
                # Friendly message for duplicate
                form.add_error('number', f"'{number}' eziste ona.")
                
    else: form = EvalLetForm(eval=eval)
    context = {
        'group':group, 'eval':eval, 'form':form,
        'title': f'Aumenta Karta', 'legend': f'Aumenta Karta'
    }
    return render(request, 'eval_uvip/form.html', context)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalLetEdit(request, hashid):
    group = get_roles(request)
    if 'sigp_uivp' in group: div = c_user_uvip(request.user)
    obj = get_object_or_404(EvalLet, hashed=hashid)
    eval = obj.eval
    
    if request.method == 'POST':
        form = EvalLetForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            try:    
                instance = form.save(commit=False)
                data = form.cleaned_data
                number = data['number']
                if EvalLet.objects.filter(number=number).exists():
                    form.add_error('number', f"'{number}' eziste ona.")
                else:
                    instance.datetime = datetime.datetime.now()
                    instance.user = request.user
                    instance.save()
                    messages.success(request, f'Altera ona.')
                return redirect('uvip-eval-det', hashid=eval.hashed)
            except IntegrityError as e:
            # Friendly message for duplicate
                form.add_error('number', f"'{number}' eziste ona.")
    
    else: form = EvalLetForm(instance=obj)
    context = {
        'group':group, 'eval':eval, 'form':form,
        'title': f'Altera Karta', 'legend': f'Altera Karta'
    }
    return render(request, 'eval_uvip/form.html', context)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalLetADNBackDev(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(EvalLet, hashed=hashid)
   
    eval = obj.eval
    # fi = eval.proj.pcategory.id
    # if fi == 1: 
    #     track = EvalFITrack.objects.filter(eval=eval).first()
    # else: 
    #     track = EvalTrack.objects.filter(eval=eval).first()
    if request.method == 'POST':
        newid, new_hashid = getnewid(EvalLetAdnBack)
        form = EvalLetForm3(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.is_return = True
            instance.evallet_id = obj.pk
            instance.datetime = datetime.datetime.now().replace(second=0, microsecond=0)
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f' UIVP.')
        return redirect('uvip-eval-det', hashid=eval.hashed)
    else: form = EvalLetForm3()
    context = {
        'group': group, 'eval':eval, 'obj':obj, 'form':form,
        'title': 'Komentariu Devolve', 'legend': 'Komentariu Devolve'
    }
    return render(request, 'eval_uvip/form.html', context)


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalLetADNBackDevEdit(request, hashid):
    group = get_roles(request)
    if 'sigp_uivp' in group: div = c_user_uvip(request.user)
    obj = get_object_or_404(EvalLetAdnBack, hashed=hashid)
    eval = obj.evallet.eval
   
    if request.method == 'POST':
        form = EvalLetForm3(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now().replace(second=0, microsecond=0)
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
        return redirect('uvip-eval-det', hashid=eval.hashed)
    
    else: form = EvalLetForm3(instance=obj)
    context = {
        'group':group, 'eval':eval, 'form':form,
        'title': f'Altera Karta', 'legend': f'Altera Karta'
    }
    return render(request, 'eval_uvip/form.html', context)


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalLetADNBackRes(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(EvalLet, hashed=hashid)
    eval = obj.eval
      
    if request.method == 'POST':
        newid, new_hashid = getnewid(EvalLetAdnBack)
        form = EvalLetForm4(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.is_result = True
            instance.evallet_id = obj.pk
            instance.datetime = datetime.datetime.now().replace(second=0, microsecond=0)
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f' UIVP.')
        else:
            # Print errors for debugging
            print("Form errors:")
            for field, errors in form.errors.items():
                print(f"Field: {field}")
                for error in errors:
                    print(f"  Error: {error}")
            
            # Print non-field errors
            print("Non-field errors:")
            for error in form.non_field_errors():
                print(f"  Error: {error}")
        return redirect('uvip-eval-det', hashid=eval.hashed)
    else: form = EvalLetForm4()
    context = {
        'group': group, 'eval':eval, 'obj':obj, 'form':form,
        'title': 'Atualiza Rezultadu', 'legend': 'Atualiza Rezultadu'
    }
    return render(request, 'eval_uvip/form.html', context)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalLetADNBackResEdit(request, hashid):
    group = get_roles(request)
    if 'sigp_uivp' in group: div = c_user_uvip(request.user)
    
    obj = get_object_or_404(EvalLetAdnBack, hashed=hashid)
    eval = obj.evallet.eval
    
    # fi = eval.proj.pcategory.id
    # if fi == 1: 
    #      track = EvalFITrack.objects.filter(eval=eval).first()
    #      track.is_uvip_in_3 = True
    #      track.save()
   
    if request.method == 'POST':
        form = EvalLetForm4(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now().replace(second=0, microsecond=0)
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
        return redirect('uvip-eval-det', hashid=eval.hashed)
    
    else: form = EvalLetForm4(instance=obj)
    context = {
        'group':group, 'eval':eval, 'form':form,
        'title': f'Altera Karta', 'legend': f'Altera Karta'
    }
    return render(request, 'eval_uvip/form.html', context)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalLetRem(request, pk):
    obj = get_object_or_404(EvalLet, pk=pk)
    eval = obj.eval
    obj.delete()
    messages.success(request, f'Hamos ona.')
    return redirect('uvip-eval-det', hashid=eval.hashed)
###