import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from company.models import Company, CompUser
from company.forms import CompanyForm
from conf.utils import getnewid, split_string


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def CompanyAdd(request):
    if request.method == 'POST':
        newid, new_hashid = getnewid(Company)
        form = CompanyForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.datetime = datetime.datetime.now()
            instance.hashed = new_hashid
            instance.save()
            messages.success(request, f'Aumenta ona.')
            return redirect('comp-list')
    else: form = CompanyForm()
    context = {
        'form': form, 'user': request.user,
        'title': 'Aumenta Companha', 'legend': 'Aumenta Companha'
    }
    return render(request, 'company/form.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def CompanyEdit(request, hashid):
    objects = get_object_or_404(Company, hashed=hashid)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=objects)
        if form.is_valid():
            form.save()
            messages.success(request, f'Altera ona.')
            return redirect('comp-det', hashid=hashid)
    else: form = CompanyForm(instance=objects)
    context = {
        'form': form,
        'title': 'Altera Companha', 'legend': 'Altera Companha'
    }
    return render(request, 'company/form.html', context)
#

@allowed_users(allowed_roles=['sigp_admin'])
def CompUserCreate(request, pk):
    group = Group.objects.get(name='comp')
    comp = get_object_or_404(Company, pk=pk)
    newid, _ = getnewid(User)
    username = 'c_'+split_string(comp.name).lower()+str(comp.id)
    password = make_password('mop#@2024')
    obj = User(id=newid, username=username, password=password)
    obj.save()
    obj2 = CompUser(id=newid, user_id=newid, comp=comp)
    obj2.save()
    user = User.objects.get(pk=newid)
    user.groups.add(group)
    messages.success(request, f'Kria ona.')
    return redirect('comp-list')


@allowed_users(allowed_roles=['sigp_admin'])
def CompPassReset(request, pk):
    obj = get_object_or_404(CompUser, comp_id=pk)
    user = User.objects.filter(id=obj.user.id).first()
    passwd = make_password('mop#@2024')
    user.password = passwd
    user.save()
    messages.success(request, f'Konta reset ona.')
    return redirect('comp-list')


@allowed_users(allowed_roles=['sigp_admin'])
def CompPassEna(request, pk):
    obj = get_object_or_404(CompUser, comp_id=pk)
    user = User.objects.filter(id=obj.user.id).first()
    user.is_active = True
    user.save()
    messages.success(request, f'Ativa ona.')
    return redirect('comp-list')


@allowed_users(allowed_roles=['sigp_admin'])
def CompPassDis(request, pk):
    obj = get_object_or_404(CompUser, comp_id=pk)
    
    user = User.objects.filter(id=obj.user.id).first()
    user.is_active = False
    user.save()
    messages.success(request, f'Desativa ona.')
    return redirect('comp-list')