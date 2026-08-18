from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from company.models import Company
from company.forms import uCompanyForm
from users.decorators import allowed_users
from sigp.utils import get_roles
from conf.user_utils import c_user_comp



@login_required
def CompanyList(request):
	group = get_roles(request)
	objects = Company.objects.all().prefetch_related('compuser').order_by("name")
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Companha', 'legend': 'Lista Companha'
	}
	return render(request, 'company/list.html', context)

@login_required
def CompanyDetail(request, hashid):
	group = get_roles(request)
	comp = get_object_or_404(Company, hashed=hashid)
	context = {
		'group': group, 'comp': comp,
		'title': 'Detalha Companha', 'legend': 'Detalha Companha',
	}
	return render(request, 'company/detail.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin'])
def CompUserList(request):
	group = get_roles(request)
	objects = Company.objects.filter().prefetch_related('compuser').all().order_by('name')
	context = {
		'group': group, 'objects': objects,
		'title': 'Lista Usarios ba Empreza', 'legend': 'Lista Usarios ba Empreza'
	}
	return render(request, 'lec/user_list.html', context)
#
@login_required
def uCompDet(request):
	group = get_roles(request)
	comp = c_user_comp(request.user)
	if request.method == 'POST':
		form = uCompanyForm(request.POST, request.FILES, instance=comp)
		if form.is_valid():
			form.save()
			messages.success(request, f'Atualiza ona!')
			return redirect('comp-u-det')
	else: form = uCompanyForm(instance=comp)
	context = {
		'group': group, 'comp': comp, 'form':form,
		'title': f'Perfil', 'legend': f'Perfil',
	}
	return render(request, 'company/u_det.html', context)
