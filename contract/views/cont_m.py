import datetime
from django.shortcuts import render, redirect, get_object_or_404
from contract.models import Contract, ContractComp, ContractFiles, Amendment, ContractYear
from contract.forms import ContForm, ContCompForm, ContFilesForm, ContStatusForm, ContStopForm, ContractYearForm
from project.models import Project
from conf.user_utils import c_user_dna
from django.contrib import messages
from conf.utils import getnewid
from datetime import datetime
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles


@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContAdd(request):
    group = get_roles(request)
    dna = c_user_dna(request.user)
    if request.method == 'POST':
        newid, new_hashid = getnewid(Contract)
        form = ContForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            proj = form.cleaned_data.get('project')
            instance.id = newid
            instance.is_cont = True
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            proj.is_cont = True
            proj.save()
            amend = Amendment.objects.filter(id=newid).first()
            amend.number = form.cleaned_data.get('number')
            amend.end_date = form.cleaned_data.get('end_date')
            amend.total = form.cleaned_data.get('total')
            amend.save()

            a = form.cleaned_data.get('start_date').year
            b = form.cleaned_data.get('end_date').year
            c = form.cleaned_data.get('total')
            if form.cleaned_data.get('is_fiscal') == True:
                for i in range(a,b+1):
                    newid2, _ = getnewid(ContractYear)
                    check = ContractYear.objects.filter(contract_id=newid, year=i).first()
                    if not check:
                        obj = ContractYear(id=newid2, contract_id=newid, total=c, year=i)
                        obj.save()
            else:
                newid2, _ = getnewid(ContractYear)
                check = ContractYear.objects.filter(contract_id=newid, year=a).first()
                if not check:
                    obj = ContractYear(id=newid2, contract_id=newid, total=c, year=a)
                    obj.save()
            messages.success(request, f'Aumenta ona.')
            return redirect('dna-cont-det', hashid=new_hashid)
    else: form = ContForm()
    context = {
        'group': group, 'form': form, 'page': 'plist',
        'title': 'Aumenta Kontratu', 'legend': 'Aumenta Kontratu'
    }
    return render(request, 'contract/form.html', context)


@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContEdit(request, hashid):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    amend = Amendment.objects.filter(contract=cont).first()
    proj = cont.project
    if request.method == 'POST':
        form = ContForm(request.POST, request.FILES, instance=cont)
        if form.is_valid():
            amend.number = form.cleaned_data.get('number')
            amend.end_date = form.cleaned_data.get('end_date')
            amend.total = form.cleaned_data.get('total')
            amend.save()
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            a = form.cleaned_data.get('start_date').year
            b = form.cleaned_data.get('end_date').year
            c = form.cleaned_data.get('total')
            if form.cleaned_data.get('is_fiscal') == True:
                for i in range(a,b+1):
                    newid2, _ = getnewid(ContractYear)
                    check = ContractYear.objects.filter(contract=cont, year=i).first()
                    if not check:
                        obj = ContractYear(id=newid2, contract=cont, total=c, year=i)
                        obj.save()
            else:
                newid2, _ = getnewid(ContractYear)
                check = ContractYear.objects.filter(contract=cont, year=a).first()
                if not check:
                    obj = ContractYear(id=newid2, contract=cont, total=c, year=a)
                    obj.save()
                else:
                    check.total = c
                    check.save()
            messages.success(request, f'Altera ona.')
            return redirect('dna-cont-det', hashid=hashid)
    else: form = ContForm(instance=cont)
    context = {
        'group': group, 'proj': proj, 'cont':cont, 'form': form, 'page': 'pdet',
        'title': 'Altera Kontratu', 'legend': 'Altera Kontratu'
    }
    return render(request, 'contract/form.html', context)


@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContStatusEdit(request, hashid):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    proj = cont.project
    if request.method == 'POST':
        form = ContStatusForm(request.POST, instance=cont)
        if form.is_valid():
            status = form.cleaned_data.get('status')
            instance = form.save(commit=False)
            instance.save()
            
            if status.name == "Abandona" or status.name == "Tarde":
                proj.status_id = 3 ## pending for project status
                proj.save()
            elif status.name == "FHO":
                proj.status_id = 4 ## completed for project status
                proj.save()
            else:
                proj.status_id = 2 ## ongoing for project status
                proj.save()
            
            messages.success(request, f'Altera ona.')
            return redirect('dna-cont-det', hashid=hashid)
    else: form = ContStatusForm(instance=cont)
    context = {
        'group': group, 'proj': proj, 'cont':cont, 'form': form, 'page': 'pdet',
        'title': 'Altera Status', 'legend': 'Altera Status'
    }
    return render(request, 'contract/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContRem(request, pk):
    objects = get_object_or_404(Contract, pk=pk)
    objects.delete()
    messages.success(request, f'Hapaga ona.')
    return redirect('dna-cont-list')


@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_admin'])
def dnaContLock(request, hashid):
    objects = get_object_or_404(Contract, hashed=hashid)
    objects.is_lock = True
    objects.save()
    proj = objects.project
    messages.success(request, f'Xavi ona.')
    return redirect('dna-cont-det', hashid=hashid)


@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContUnLock(request, hashid):
    objects = get_object_or_404(Contract, hashed=hashid)
    objects.is_lock = False
    objects.save()
    proj = objects.project
    messages.success(request, f'Loke fali ona.')
    return redirect('dna-cont-det', hashid=hashid)


@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContReady(request, hashid):
    obj = get_object_or_404(Contract, hashed=hashid)
    obj.is_ready = True
    obj.save()
    proj = obj.project
    proj.is_cont = True
    proj.save()
    messages.success(request, f'Kontratu pronto ona.')
    return redirect('dna-cont-det', hashid=hashid)


@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContComplete(request, hashid):
    obj = get_object_or_404(Contract, hashed=hashid)
    obj.is_complete = True
    obj.save()
    proj = obj.project
    proj.is_end = True
    proj.save()
    messages.success(request, f'Altera ona.')
    return redirect('dna-cont-det', hashid=hashid)


@allowed_users(allowed_roles=['admin','sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContYearEdit(request, pk):
    group = get_roles(request.user)
    obj = get_object_or_404(ContractYear, pk=pk)
    cont = obj.contract
    if request.method == 'POST':
        form = ContractYearForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Altera ona.')
            return redirect('dna-cont-det', hashid=cont.hashed)
    else: form = ContractYearForm(instance=obj)
    context = {
        'group': group, 'form': form, 'cont':cont, 'page': 'pdet',
        'title': 'Altera Montante', 'legend': 'Altera Montante'
    }
    return render(request, 'contract/form.html', context)
###

@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContCompAdd(request, hashid):
    group = get_roles(request.user)
    cont = get_object_or_404(Contract, hashed=hashid)
    proj = cont.project
    if request.method == 'POST':
        newid, new_hashid = getnewid(ContractComp)
        form = ContCompForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.contract = cont
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Aumenta ona.')
            return redirect('dna-cont-det', hashid=hashid)
    else: form = ContCompForm()
    context = {
        'group': group, 'proj': proj, 'cont':cont, 'form': form, 'page': 'pdet',
        'title': 'Aumenta Kompanha', 'legend': 'Aumenta Kompanha'
    }
    return render(request, 'contract/form.html', context)


@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContCompEdit(request, hashid, pk):
    group = get_roles(request.user)
    cont = get_object_or_404(Contract, hashed=hashid)
    proj = cont.project
    objects = get_object_or_404(ContractComp, pk=pk)
    if request.method == 'POST':
        form = ContCompForm(request.POST, instance=objects)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('dna-cont-det', hashid=hashid)
    else: form = ContCompForm(instance=objects)
    context = {
        'group': group, 'proj': proj, 'cont':cont, 'form': form, 'page': 'pdet',
        'title': 'Altera Kompanha', 'legend': 'Altera Kompanha'
    }
    return render(request, 'contract/form.html', context)


@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContCompRem(request, hashid, pk):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    proj = cont.project
    objects = get_object_or_404(ContractComp, pk=pk)
    objects.delete()
    messages.success(request, f'Hapaga ona.')
    return redirect('dna-cont-det', hashid=hashid)
###

@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContFileAdd(request, hashid):
    group = get_roles(request)
    dna = c_user_dna(request.user)
    cont = get_object_or_404(Contract, hashed=hashid)
    proj = cont.project
    if request.method == 'POST':
        newid, new_hashid = getnewid(ContractFiles)
        form = ContFilesForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.contract = cont
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Aumenta ona.')
            return redirect('dna-cont-det', hashid=hashid)
    else: form = ContFilesForm()
    context = {
        'group': group, 'proj': proj, 'cont':cont, 'form': form, 'page': 'pdet',
        'title': 'Aumenta Anexu', 'legend': 'Aumenta Anexu'
    }
    return render(request, 'contract/form.html', context)


@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContFileEdit(request, hashid, pk):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    proj = cont.project
    objects = get_object_or_404(ContractFiles, pk=pk)
    if request.method == 'POST':
        form = ContFilesForm(request.POST, request.FILES, instance=objects)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('dna-cont-det', hashid=hashid)
    else: form = ContFilesForm(instance=objects)
    context = {
        'group': group, 'proj': proj, 'cont':cont, 'form': form, 'page': 'pdet',
        'title': 'Altera Anexu', 'legend': 'Altera Anexu'
    }
    return render(request, 'contract/form.html', context)


@allowed_users(allowed_roles=['sigp_dna','sigp_op','sigp_uivp','sigp_admin'])
def dnaContFileRem(request, hashid, pk):
    cont = get_object_or_404(Contract, hashed=hashid)
    proj = cont.project
    objects = get_object_or_404(ContractFiles, pk=pk)
    objects.delete()
    messages.success(request, f'Hapaga ona.')
    return redirect('dna-cont-det', hashid=hashid)
###

@allowed_users(allowed_roles=['sigp_dna','sigp_uivp','sigp_admin'])
def dnaContStopEdit(request, hashid):
    group = get_roles(request)
    cont = get_object_or_404(Contract, hashed=hashid)
    proj = cont.project
    if request.method == 'POST':
        form = ContStopForm(request.POST, instance=cont)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, f'Hapara ona.')
            return redirect('dna-cont-det', hashid=hashid)
    else: form = ContStopForm(instance=cont)
    context = {
        'group': group, 'proj': proj, 'cont':cont, 'form': form, 'page': 'pdet',
        'title': 'Hapara Kontratu', 'legend': 'Hapara Kontratu'
    }
    return render(request, 'contract/form.html', context)



@allowed_users(allowed_roles=['sigp_dna','sigp_uivp','sigp_admin'])
def dnaContUpdataEstatus(request):
    group = get_roles(request)

    current_year = datetime.now().year
    # GET ALL PROJECTS THAT HAVE CONTRACTS
    projects = Project.objects.filter(contract__isnull=False).distinct()
    # LOOP AND UPDATE STATUS
    for proj in projects:
        allocate_year = proj.year.year # integer year

        if allocate_year == current_year:
            proj.statusproj_id = 1    # FOUN
        elif allocate_year < current_year:
            proj.statusproj_id = 2    # REAPROPRIASAUN

        proj.save()

    messages.success(request, "Atualiza Estatus Orsamentu ba Projetu Hotu!")
    return redirect('dna-cont-list')
