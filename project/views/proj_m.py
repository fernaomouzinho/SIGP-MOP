import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.contrib import messages
from project.models import Project, ProjectEst, ProjectLoc
from project.forms import ProjectEstForm1, ProjectEstForm3, ProjectLocForm
from users.decorators import allowed_users
from sigp.utils import get_roles

# div

@allowed_users(allowed_roles=['sigp_div','sigp_dna','sigp_dnof','sigp_op','sigp_bd'])
def divProjEstEdit(request, hashid, pk):
    objects = get_object_or_404(ProjectEst, pk=pk)
    if request.method == 'POST':
        form = ProjectEstForm1(request.POST, instance=objects)
        if form.is_valid():
            form.save()
            messages.success(request, f'Altera ona.')
            return redirect('div-proj-det', hashid=hashid)
    else: form = ProjectEstForm1(instance=objects)
    context = {
        'proj': objects.project, 'form': form, 'page': 'pdet',
        'title': 'Altera Estimasaun', 'legend': 'Altera Estimasaun'
    }
    return render(request, 'project/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_op','sig_uivp','sigp_bd'])
def opProjEstEdit(request, hashid, pk):
    objects = get_object_or_404(ProjectEst, pk=pk)
    if request.method == 'POST':
        form = ProjectEstForm3(request.POST, instance=objects)
        if form.is_valid():
            adn_est = form.cleaned_data.get('adn')
            a = Project.objects.get(pk=objects.project.pk)
            est = form.cleaned_data.get('owner')
            adn = 0
            if adn_est: adn = adn_est
            bal = float(objects.owner)-float(adn)
            instance = form.save(commit=False)
            instance.balance = bal
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('uvip-proj-det', hashid=hashid)
    else: form = ProjectEstForm3(instance=objects)
    context = {
        'proj': objects.project, 'form': form, 'page': 'pdet',
        'title': 'Altera Estimasaun', 'legend': 'Altera Estimasaun'
    }
    return render(request, 'project/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_div','sigp_dna','sigp_dnof','sigp_op'])
def divProjEstRem(request, hashid, pk):
    objects = get_object_or_404(ProjectEst, pk=pk)
    objects.owner = None
    objects.save()
    messages.success(request, f'Hamos ona.')
    return redirect('div-proj-det', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sig_uivp','sigp_div','sigp_dna','sigp_dnof','sigp_op','sigp_bd'])
def divProjLocEdit(request, hashid, pk):
    group = get_roles(request)
    proj = get_object_or_404(Project, hashed=hashid)
    objects = get_object_or_404(ProjectLoc, pk=pk)
    if request.method == 'POST':
        form = ProjectLocForm(request.POST, instance=objects)
        if form.is_valid():
            proj.is_read = True
            proj.save()
            form.save()
            messages.success(request, f'Altera ona.')
            if group == "div": return redirect('div-proj-det', hashid=hashid)
            else: return redirect('uvip-proj-det', hashid=hashid)
    else: form = ProjectLocForm(instance=objects)
    context = {
        'group':group, 'proj': proj, 'form': form, 'page': 'pdet',
        'title': 'Altera Lokalizasaun', 'legend': 'Altera Lokalizasaun'
    }
    return render(request, 'project/form_loc.html', context)
###