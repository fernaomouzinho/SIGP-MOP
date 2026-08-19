import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.decorators import allowed_users
from sigp.utils import get_roles
from contract.models import Contract
from project.models import Project, ProjectEst
from finance.models import CPV, EV, PO, PRT, TPO
from finance.forms import CPVForm, EVForm, POForm, opPOForm, PRTForm, TPOForm
from conf.utils import getnewid

# CPV
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opCPVAdd(request, hashid):
	group = get_roles(request)
	proj = get_object_or_404(Project, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(CPV)
		form = CPVForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.proj = proj
			instance.div = proj.owner
			instance.is_appr = True
			instance.is_end = True
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta susesu.')
			return redirect('op-cpv-list', hashid=hashid)
	else: form = CPVForm()
	context = {
		'group': group, 'proj': proj, 'form': form, 'page': 'cpv',
		'title': 'Kria CPV', 'legend': 'Kria CPV'
	}
	return render(request, 'finance_op/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opCPVEdit(request, hashid, hashid2):
	group = get_roles(request)
	proj = get_object_or_404(Project, hashed=hashid)
	cpv = get_object_or_404(CPV, hashed=hashid2)
	if request.method == 'POST':
		form = CPVForm(request.POST, request.FILES, instance=cpv)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera susesu.')
			return redirect('op-cpv-list', hashid=hashid)
	else: form = CPVForm(instance=cpv)
	context = {
		'group': group, 'proj': proj, 'form': form, 'page': 'cpv',
		'title': 'Altera CPV', 'legend': 'Altera CPV'
	}
	return render(request, 'finance_op/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opCPVRem(request, hashid, pk):
	obj = get_object_or_404(CPV, pk=pk)
	obj.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('op-cpv-list', hashid=hashid)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opCPVLock(request, hashid, pk):
	obj = get_object_or_404(CPV, pk=pk)
	obj.is_commit = True
	obj.save()
	messages.success(request, f'Xavi.')
	return redirect('op-cpv-list', hashid=hashid)
# PO
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opPOAdd(request, hashid):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	proj = cont.project
	if request.method == 'POST':
		newid, new_hashid = getnewid(PO)
		form = opPOForm(proj, request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.cont = cont
			instance.is_end = True
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta susesu.')
			return redirect('op-po-list', hashid=hashid)
	else: form = opPOForm(proj)
	context = {
		'group': group, 'cont': cont, 'form': form, 'page': 'po',
		'title': 'Kria PO', 'legend': 'Kria PO'
	}
	return render(request, 'finance_op/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opPOEdit(request, hashid, hashid2):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	proj = cont.project
	po = get_object_or_404(PO, hashed=hashid2)
	if request.method == 'POST':
		form = opPOForm(proj, request.POST, request.FILES, instance=po)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera susesu.')
			return redirect('op-po-list', hashid=hashid)
	else: form = opPOForm(proj, instance=po)
	context = {
		'group': group, 'cont': cont, 'form': form, 'page': 'po',
		'title': 'Altera PO', 'legend': 'Altera PO'
	}
	return render(request, 'finance_op/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opPORem(request, hashid, pk):
	obj = get_object_or_404(PO, pk=pk)
	obj.delete()
	messages.success(request, f'Apaga ona.')
	return redirect('op-po-list', hashid=hashid)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opPOLock(request, hashid, pk):
	obj = get_object_or_404(PO, pk=pk)
	obj.is_lock = True
	obj.save()
	messages.success(request, f'Xavi.')
	return redirect('op-po-list', hashid=hashid)
# PRT
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opPRTAdd(request, hashid):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(PRT)
		form = PRTForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.cont = cont
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta susesu.')
			return redirect('op-prt-list', hashid=hashid)
	else: form = PRTForm()
	context = {
		'group': group, 'cont': cont, 'form': form, 'page': 'prt', 
		'title': 'Kria PRT', 'legend': 'Kria PRT'
	}
	return render(request, 'finance_op/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opPRTEdit(request, hashid, hashid2):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	prt = get_object_or_404(PRT, hashed=hashid2)
	if request.method == 'POST':
		form = PRTForm(request.POST, request.FILES, instance=prt)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera susesu.')
			return redirect('op-prt-list', hashid=hashid)
	else: form = PRTForm(instance=prt)
	context = {
		'group': group, 'cont': cont, 'form': form, 'page': 'prt', 
		'title': 'Altera PRT', 'legend': 'Altera PRT'
	}
	return render(request, 'finance_op/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opPRTRem(request, hashid, pk):
	obj = get_object_or_404(PRT, pk=pk)
	obj.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('op-prt-list', hashid=hashid)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opPRTLock(request, hashid, pk):
	obj = get_object_or_404(PRT, pk=pk)
	obj.is_ready = True
	obj.save()
	messages.success(request, f'Xavi.')
	return redirect('op-prt-list', hashid=hashid)
# EV
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opEVEdit(request, hashid, hashid2):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	ev = get_object_or_404(EV, hashed=hashid2)
	if request.method == 'POST':
		form = EVForm(request.POST, request.FILES, instance=ev)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera susesu.')
			return redirect('op-ev-list', hashid=hashid)
	else: form = EVForm(instance=ev)
	context = {
		'group': group, 'cont': cont, 'form': form, 'page': 'ev', 
		'title': 'Altera EV', 'legend': 'Altera EV'
	}
	return render(request, 'finance_op/form.html', context)


@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opEVRem(request, hashid, pk):
	obj = get_object_or_404(EV, pk=pk)
	obj.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('op-ev-list', hashid=hashid)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opEVLock(request, hashid, pk):
	obj = get_object_or_404(EV, pk=pk)
	obj.is_ready = True
	obj.save()
	messages.success(request, f'Xavi.')
	return redirect('op-ev-list', hashid=hashid)
# TPO
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opTPOAdd(request, hashid):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(TPO)
		form = TPOForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.proj = cont.project
			instance.cont = cont
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta susesu.')
			return redirect('op-tpo-list', hashid=hashid)
	else: form = TPOForm()
	context = {
		'group': group, 'cont': cont, 'form': form, 'page': 'tpo',
		'title': 'Kria TPO', 'legend': 'Kria TPO'
	}
	return render(request, 'finance_op/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opTPOEdit(request, hashid, hashid2):
	group = get_roles(request)
	cont = get_object_or_404(Contract, hashed=hashid)
	tpo = get_object_or_404(TPO, hashed=hashid2)
	if request.method == 'POST':
		form = TPOForm(request.POST, request.FILES, instance=tpo)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera susesu.')
			return redirect('op-tpo-list', hashid=hashid)
	else: form = TPOForm(instance=tpo)
	context = {
		'group': group, 'cont': cont, 'form': form, 'page': 'tpo',
		'title': 'Altera TPO', 'legend': 'Altera TPO'
	}
	return render(request, 'finance_op/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opTPORem(request, hashid, pk):
	obj = get_object_or_404(TPO, pk=pk)
	obj.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('op-tpo-list', hashid=hashid)

@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_op','sigp_admin'])
def opTPOLock(request, hashid, pk):
	obj = get_object_or_404(TPO, pk=pk)
	obj.is_ready = True
	obj.save()
	messages.success(request, f'Xavi.')
	return redirect('op-tpo-list', hashid=hashid)