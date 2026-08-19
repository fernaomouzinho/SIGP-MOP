import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.contrib import messages
from django.db import IntegrityError
from project.models import Project, ProjectEst
from eval.models import Eval, EvalLet, EvalTrack, EvalFITrack
from project.forms import ProjectForm, ProjectEstForm2, ProjectStatusForm, ProjADNForm
from conf.utils import getnewid
from django.core.exceptions import ObjectDoesNotExist
from users.decorators import allowed_users
from sigp.utils import get_roles


@allowed_users(allowed_roles=['sig_uivp','sigp_admin','sigp_op','sigp_bd'])
def uvipProjAdd(request):
    group = get_roles(request)
    if request.method == 'POST':
        newid, new_hashid = getnewid(Project)
        form = ProjectForm(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                year = str(form.cleaned_data.get('year'))
                yr   = str(year)[2:]
                yrnow = str(datetime.datetime.now().year)
                pcod = form.cleaned_data.get('code')
                pcat = form.cleaned_data.get('pcategory')
                ka= form.cleaned_data.get('code_act')
                pcat  = str(pcat)[0:2]
                
        
                if pcat == 'FI':
                    pcode = "PMOPFI%s%s" % (yr,pcod)
                   
                else:
                    pcode = "PMOP%s%s" % (yr,pcod)
                    
                if Project.objects.filter(code=pcod).exists():
                    form.add_error('code', f"'{pcode}' eziste ona.")
                elif Project.objects.filter(code_act=ka).exists():
                     form.add_error('code_act', f"'{ka}' eziste ona.")
                else:
                    instance.id = newid
                    instance.code = pcode
                    instance.code_act= ka
                    instance.datetime = datetime.datetime.now()
                    instance.user = request.user
                    instance.hashed = new_hashid
                    instance.save()
                    
                    messages.success(request, f'Aumenta ona.')
                    return redirect('uvip-proj-year', year=year)
            except IntegrityError as e:
                # Friendly message for duplicate
                form.add_error('code', f"'{pcode}' eziste ona.")
                form.add_error('code_act', f"'{ka}' eziste ona.")
            
    else: form = ProjectForm()
    context = {
        'group': group, 'form': form, 'page': 'plist',
        'title': 'Aumenta Projetu', 'legend': 'Aumenta Projetu'
    }
    return render(request, 'project_uvip/form.html', context)


@allowed_users(allowed_roles=['sig_uivp','sigp_admin','sigp_op','sigp_bd'])
def uvipProjEdit(request, hashid):
    group = get_roles(request)
    objects = get_object_or_404(Project, hashed=hashid)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=objects)
        if form.is_valid():
            instance = form.save(commit=False)
            pcod = form.cleaned_data.get('code')
            ka= form.cleaned_data.get('code_act')    
            instance.code = pcod
            instance.code_act= ka
            instance.save()    
            messages.success(request, f'Altera ona.')
            return redirect('uvip-proj-det', hashid=hashid)
            
    else: form = ProjectForm(instance=objects)
    context = {
        'group': group, 'proj': objects, 'form': form, 'page': 'pdet',
        'title': 'Altera Projetu', 'legend': 'Altera Projetu'
    }
    return render(request, 'project_uvip/form.html', context)


@allowed_users(allowed_roles=['sig_uivp','sigp_admin','sigp_op'])
def uvipProjStatusEdit(request, hashid):
    group = get_roles(request)
    objects = get_object_or_404(Project, hashed=hashid)
    if request.method == 'POST':
        form = ProjectStatusForm(request.POST, instance=objects)
        if form.is_valid():
            form.save()
            messages.success(request, f'Altera ona.')
            return redirect('uvip-proj-det', hashid=hashid)
    else: form = ProjectStatusForm(instance=objects)
    context = {
        'group': group, 'proj': objects, 'form': form, 'page': 'pdet',
        'title': 'Altera Status Projetu', 'legend': 'Altera Status Projetu'
    }
    return render(request, 'project_uvip/form.html', context)


@allowed_users(allowed_roles=['sig_uivp','sigp_admin','sigp_op'])
def uvipProjRem(request, hashid):
    objects = get_object_or_404(Project, hashed=hashid)
    objects.delete()
    messages.success(request, f'Hapaga ona.')
    return redirect('uvip-proj-list')

@allowed_users(allowed_roles=['sig_uivp','sigp_admin','sigp_op'])
def uvipProjLock(request, hashid):
    objects = get_object_or_404(Project, hashed=hashid)
    objects.is_lock = True
    objects.save()
    messages.success(request, f'Xavi ona.')
    return redirect('uvip-proj-det', hashid=hashid)


@allowed_users(allowed_roles=['sig_uivp','sigp_admin','sigp_op'])
def uvipProjUnlock(request, hashid):
    objects = get_object_or_404(Project, hashed=hashid)
    objects.is_lock = False
    objects.save()
    messages.success(request, f'Loke ona.')
    return redirect('uvip-proj-det', hashid=hashid)


@allowed_users(allowed_roles=['sig_uivp','sigp_admin','sigp_op'])
def uvipProjReady(request, hashid):
    objects = get_object_or_404(Project, hashed=hashid)
    objects.is_ready = True
    objects.save()
    messages.success(request, f'Pronto ona.')
    return redirect('uvip-proj-det', hashid=hashid)
###
@allowed_users(allowed_roles=['sig_uivp','sigp_admin','sigp_op'])
def uvipProjEstEdit(request, hashid, pk):
    group = get_roles(request)
    objects = get_object_or_404(ProjectEst, pk=pk)
    proj = objects.project
    fi = proj.pcategory.id
    eval = Eval.objects.filter(proj=proj).first()
    if request.method == 'POST':
        form = ProjectEstForm2(request.POST, instance=objects)
        if form.is_valid():
            adn_est = form.cleaned_data.get('adn')
            bal = float(objects.owner)-float(adn_est)
            instance = form.save(commit=False)
            instance.balance = bal
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('uvip-eval-det', hashid=eval.hashed)
    else: form = ProjectEstForm2(instance=objects)
    context = {
        'group': group, 'proj': objects.project, 'form': form, 'page': 'pdet',
        'title': 'Altera Estimasaun', 'legend': 'Altera Estimasaun'
    }
    return render(request, 'project_uvip/form.html', context)


@allowed_users(allowed_roles=['sig_uivp','sigp_admin','sigp_op'])
def uvipProjEstRem(request, hashid, pk):
    objects = get_object_or_404(ProjectEst, pk=pk)
    objects.adn = None
    objects.balance = None
    objects.save()
    messages.success(request, f'Hamos ona.')
    return redirect('uvip-proj-det', hashid=hashid)
###

@allowed_users(allowed_roles=['sig_uivp','sigp_admin','sigp_op'])
def uvipProjEstRem(request):
    objects = Project.objects.filter().all()
    messages.success(request, f'Hamos ona.')
    return redirect('uvip-proj-det')
#
@allowed_users(allowed_roles=['sig_uivp','sigp_admin','sigp_op'])
def uvipProjADNEdit(request, hashid):
    proj = get_object_or_404(Project, hashed=hashid)
    if request.method == 'POST':
        form = ProjADNForm(request.POST, instance=proj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Altera ona.')
            return redirect('uvip-proj-det', hashid=hashid)
    else: form = ProjADNForm(instance=proj)
    context = {
        'proj': proj, 'form': form, 'page': 'pdet',
        'title': 'Verifikasaun ADN', 'legend': 'Verifikasaun ADN'
    }
    return render(request, 'project_uvip/form.html', context)
