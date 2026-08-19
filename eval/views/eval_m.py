import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from custom.models import DG,Division
from project.models import Project
from eval.models import Eval, EvalFile, EvalTrack, EvalFITrack, EvalLetCNABack, EvalLet
from eval.forms import EvalFileForm, EvalForm, EvalForm3,EvalLetForm5
from conf.user_utils import c_user_div, c_user_dna, c_user_dnof
from conf.utils import getnewid, split_string, write_roman
from users.decorators import allowed_users
from sigp.utils import get_roles

@allowed_users(allowed_roles=['sigp_div','sigp_dna','sigp_dnof'])
def divEvalAdd(request):
    group = get_roles(request)
    if 'sigp_div' in group: div = c_user_div(request.user)
    elif 'sigp_dna' in group: div = c_user_dna(request.user)
    elif 'sigp_dnof' in group: div = c_user_dnof(request.user)
    
    if request.method == 'POST':
        newid, new_hashid = getnewid(Eval)
        form = EvalForm(div, request.POST)
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
                proj = data['proj']
                
                eval_number  = "%s/%s-%s-MOP/%s/%s" % (number,dv,dg,rom_num,yr)
                
                if Eval.objects.filter(number=eval_number).exists():
                    form.add_error('number', f"'{eval_number}' eziste ona.")
                elif Eval.objects.filter(proj=proj).exists():
                    form.add_error('proj', f"'{proj}' eziste ona.")
                else:
                    instance.id = newid
                    instance.number = eval_number
                    instance.div = div
                    instance.datetime = datetime.datetime.now()
                    instance.user = request.user
                    instance.hashed = new_hashid
                    instance.save()
                    messages.success(request, f'Aumenta ona.')
                    return redirect('div-eval-det', hashid=new_hashid)
                
            except IntegrityError as e:
            # Friendly message for duplicate
                form.add_error('number', f"'{number}' eziste ona.")
                form.add_error('proj', f"'{proj}' eziste ona.")  
    else: form = EvalForm(div)
    context = {
        'group':group, 'form': form, 'page': 'plist',
        'title': 'Kria Avaliasaun ToR', 'legend': 'Kria Avaliasaun ToR'
    }
    return render(request, 'eval_div/form.html', context)

@allowed_users(allowed_roles=['sigp_div','sigp_dna','sigp_dnof'])
def divEvalEdit(request, hashid):
    group = get_roles(request)
    if 'sigp_div' in group: div = c_user_div(request.user)
    elif 'sigp_dna' in group: div = c_user_dna(request.user)
    elif 'sigp_dnof' in group: div = c_user_dnof(request.user)
    
    eval = get_object_or_404(Eval, hashed=hashid)
    if request.method == 'POST':
        
        form = EvalForm(div, request.POST, instance=eval)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                data = form.cleaned_data
                number = data['number']
                proj = data['proj']
                if Eval.objects.filter(number=number).exists():
                    form.add_error('number', f"'{number}' eziste ona.")
                elif Eval.objects.filter(proj=proj).exists():
                    form.add_error('proj', f"'{proj}' eziste ona.")
                else:
                    instance.number = number
                    instance.save()
                    messages.success(request, f'Altera ona.')
                    return redirect('div-eval-det', hashid=hashid)
            
            except IntegrityError as e:
            # Friendly message for duplicate
                form.add_error('number', f"'{number}' eziste ona.")
                form.add_error('proj', f"'{proj}' eziste ona.")  
        
    else: form = EvalForm(div, instance=eval)
    context = {
        'group':group, 'eval': eval, 'form': form, 'page': 'pdet',
        'title': 'Altera Avaliasaun', 'legend': 'Altera Avaliasaun'
    }
    return render(request, 'eval_div/form.html', context)

@allowed_users(allowed_roles=['sigp_div','sigp_dna','sigp_dnof'])
def divEvalRem(request, hashid):
    objects = get_object_or_404(Eval, hashed=hashid)
    objects.delete()
    messages.success(request, f'Hapaga ona.')
    return redirect('div-eval-list')
###
@allowed_users(allowed_roles=['sigp_div','sigp_dna','sigp_dnof'])
def divEvalFileAdd(request, hashid):
    group = get_roles(request)
    eval = get_object_or_404(Eval, hashed=hashid)
    if request.method == 'POST':
        newid, _ = getnewid(EvalFile)
        form = EvalFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.eval = eval
            instance.save()
            messages.success(request, f'Aumenta ona.')
            return redirect('div-eval-det', hashid=hashid)
    else: form = EvalFileForm()
    context = {
        'group':group, 'eval': eval, 'form': form, 'page': 'pdet',
        'title': 'Aneksu ToR', 'legend': 'Aneksu ToR'
    }
    return render(request, 'eval_div/form.html', context)

@allowed_users(allowed_roles=['sigp_div','sigp_dna','sigp_dnof'])
def divEvalFileEdit(request, hashid, pk):
    group = get_roles(request)
    eval = get_object_or_404(Eval, hashed=hashid)
    objects = get_object_or_404(EvalFile, pk=pk)
    if request.method == 'POST':
        form = EvalFileForm(request.POST, request.FILES, instance=objects)
        if form.is_valid():
            form.save()
            messages.success(request, f'Altera ona.')
            return redirect('div-eval-det', hashid=hashid)
    else: form = EvalFileForm(instance=objects)
    context = {
        'group':group, 'eval': eval, 'form': form, 'page': 'pdet',
        'title': 'Altera ToR', 'legend': 'Altera ToR'
    }
    return render(request, 'eval_div/form.html', context)

@allowed_users(allowed_roles=['sigp_div','sigp_dna','sigp_dnof'])
def divEvalFileRem(request, hashid, pk):
    obj = get_object_or_404(EvalFile, pk=pk)
    obj.delete()
    messages.success(request, f'Hapaga ona.')
    return redirect('div-eval-det', hashid=hashid)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalADN(request, pk, page):
    obj = get_object_or_404(Eval, pk=pk)
    if page == "1": 
        obj.is_adn = True
        obj.is_cna = False
    elif page == "2":
        obj.is_adn = True
        obj.is_cna = True
    else:
        obj.is_adn = False
        obj.is_cna = False
    obj.save()
    messages.success(request, f'Altera ona.')
    return redirect('uvip-eval-det', hashid=obj.hashed)

###
@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalAppr(request, pk):
    eval = get_object_or_404(Eval, pk=pk)
    eval.is_appr = True
    eval.save()
    if eval.is_cna == True:
        track = EvalFITrack.objects.filter(eval=eval).first()
        track.is_appr = True
        track.date_appr = datetime.datetime.now()
        track.stages = "ToR Aprovadu"
        track.percent = 37
        track.save()
    else:
        track = EvalTrack.objects.filter(eval=eval).first()
        track.is_appr = True
        track.date_appr = datetime.datetime.now()
        track.stages = "ToR Aprovadu"
        track.percent = 88
        track.save()
    messages.success(request, f'ToR Aprovadu')
    return redirect('gab-eval-det', hashid=eval.hashed)


@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalLetAppr(request, pk):
    eval = get_object_or_404(Eval, pk=pk)
    eval.is_let_appr = True
    eval.save()
    track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_let_appr = True
    track.date_let_appr = datetime.datetime.now()
    track.stages = "Karta Aprovadu"
    track.percent = 86
    track.save()
    messages.success(request, f'Karta Aprovadu')
    return redirect('gab-eval-det', hashid=eval.hashed)
#
@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalEnd(request, pk):
    group = get_roles(request)
    eval = get_object_or_404(Eval, pk=pk)
    eval.is_end = True
    eval.save()
    proj = eval.proj
    proj.is_eval = True
    proj.save()
    if eval.is_cna == False: track = EvalTrack.objects.filter(eval=eval).first()
    else: track = EvalFITrack.objects.filter(eval=eval).first()
    track.is_end = True
    track.date_end = datetime.datetime.now()
    track.stages = "ToR Termina"
    track.percent = 100
    track.save()
    messages.success(request, f'ToR Termina')
    if group == 'gab': return redirect('gab-eval-det', hashid=eval.hashed)
    else: return redirect('uvip-eval-det', hashid=eval.hashed)
    
    
@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalReturnAdd(request, hashid):
    group = get_roles(request)
    eval = get_object_or_404(Eval, hashed=hashid)
    
    
    if request.method == 'POST':
        form = EvalForm3(request.POST, request.FILES, instance=eval)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_appr = False
            instance.is_let_appr = False
            instance.is_return = True
            instance.return_date = datetime.datetime.now()
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('gab-eval-det', hashid=hashid)
    else: form = EvalForm3(instance=eval)
    context = {
        'group': group, 'eval': eval, 'form': form, 'page': 'pdet',
        'title': 'Devolve Dokumentu ToR', 'legend': 'Devolve Dokumentu ToR'
    }
    return render(request, 'eval_div/form.html', context)

@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFIReturnAdd(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(EvalLet, hashed=hashid)
    eval = obj.eval
 
    if request.method == 'POST':
        newid, new_hashid = getnewid(EvalLetCNABack)
        form = EvalLetForm5(request.POST, request.FILES)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.id = newid
                instance.evallet_id = obj.pk
                instance.is_return = True
                instance.is_result = False
                instance.datetime = datetime.datetime.now().replace(second=0, microsecond=0)
                instance.user = request.user
                instance.hashed = new_hashid
                messages.success(request, f'Altera ona.')
                return redirect('gab-eval-det', hashid=eval.hashed)
            except IntegrityError as e:
                print('Error')
                pass
    else: form = EvalLetForm5()
    context = {
        'group': group, 'eval': eval, 'form': form, 'page': 'pdet',
        'title': 'Devolve Dokumentu CNA', 'legend': 'Devolve Dokumentu CNA'
    }
    return render(request, 'eval_div/form.html', context)

@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalFIResultAdd(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(EvalLet, hashed=hashid)
    eval = obj.eval
 
    if request.method == 'POST':
        newid, new_hashid = getnewid(EvalLetCNABack)
        form = EvalLetForm5(request.POST, request.FILES)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.id = newid
                instance.evallet_id = obj.pk
                instance.is_return = False
                instance.is_result = True
                instance.datetime = datetime.datetime.now().replace(second=0, microsecond=0)
                instance.user = request.user
                instance.hashed = new_hashid
                instance.save()
                messages.success(request, f'Altera ona.')
                return redirect('gab-eval-det', hashid=eval.hashed)
            except IntegrityError as e:
                print('Error')
                pass
    else: form = EvalLetForm5()
    context = {
        'group': group, 'eval': eval, 'form': form, 'page': 'pdet',
        'title': 'Rezultadu Dokumentu CNA', 'legend': 'Rezultadu Dokumentu CNA'
    }
    return render(request, 'eval_div/form.html', context)