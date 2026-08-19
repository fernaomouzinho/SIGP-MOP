import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.decorators import allowed_users
from sigp.utils import get_roles
from contract.models import Amendment
from invoice.models import Invoice, InvTrack
from finance.models import FinFiles
from finance.forms import FinFilesForm
from conf.utils import getnewid

@allowed_users(allowed_roles=['sigp_dna','sigp_dnof','sigp_admin'])
def FinFileList(request, hashid):
	group = get_roles(request)
	track = InvTrack.objects.filter(inv=inv).first()
	if 'sig_dana' in group:
		objects = FinFiles.objects.filter(inv=inv, is_dna=True).all()
	elif 'sigp_dnof' in group:
		objects = FinFiles.objects.filter(inv=inv, is_dnof=True).all()
	context = {
		'group': group, 'inv': inv, 'objects': objects, 'track': track,
		'title': 'Anexu Relevantes', 'legend': 'Anexu Relevantes'
	}
	return render(request, 'finance_files/list.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dnof','sigp_admin'])
def FinFilesAdd(request, hashid):
	group = get_roles(request)
	inv = get_object_or_404(Invoice, hashed=hashid)
	cont = inv.cont
	proj = cont.project
	amend = Amendment.objects.filter(contract=cont).first()
	if request.method == 'POST':
		newid, _ = getnewid(FinFiles)
		form = FinFilesForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.proj = proj
			instance.cont = cont
			instance.inv = inv
			if 'sigp_dna' in group: instance.is_dna = True
			elif 'sigp_dnof' in group: instance.is_dnof = True
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta ona.')
			return redirect('fin-file-list', hashid=hashid)
	else: form = FinFilesForm()
	context = {
		'group': group, 'inv': inv, 'amend':amend, 'form': form,
		'title': 'Aumenta Anexu', 'legend': 'Aumenta Anexu'
	}
	return render(request, 'finance_files/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dnof','sigp_admin'])
def FinFilesEdit(request, hashid, pk):
	group = get_roles(request)
	inv = get_object_or_404(Invoice, hashed=hashid)
	obj = get_object_or_404(FinFiles, pk=pk)
	amend = Amendment.objects.filter(contract=inv.cont).first()
	if request.method == 'POST':
		form = FinFilesForm(request.POST, request.FILES, instance=obj)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera ona.')
			return redirect('fin-file-list', hashid=hashid)
	else: form = FinFilesForm(instance=obj)
	context = {
		'group': group, 'inv': inv, 'amend':amend, 'form': form,
		'title': 'Altera Anexu', 'legend': 'Altera Anexu'
	}
	return render(request, 'finance_files/form.html', context)

@allowed_users(allowed_roles=['sigp_dna','sigp_dnof','sigp_admin'])
def FinFilesRem(request, hashid, pk):
	obj = get_object_or_404(FinFiles, pk=pk)
	obj.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('fin-file-list', hashid=hashid)

@allowed_users(allowed_roles=['sigp_dna','sigp_dnof','sigp_admin'])
def FinFilesLock(request, hashid, pk):
	obj = get_object_or_404(FinFiles, pk=pk)
	obj.is_lock = True
	obj.save()
	messages.success(request, f'Xavi ona.')
	return redirect('fin-file-list', hashid=hashid)

@allowed_users(allowed_roles=['sigp_dna','sigp_dnof','sigp_admin'])
def FinFilesUnlock(request, hashid, pk):
	obj = get_object_or_404(FinFiles, pk=pk)
	obj.is_lock = False
	obj.save()
	messages.success(request, f'Loke fali ona.')
	return redirect('fin-file-list', hashid=hashid)

@allowed_users(allowed_roles=['sigp_dna','sigp_dnof','sigp_admin'])
def FinFilesReady(request, hashid, pk):
	obj = get_object_or_404(FinFiles, pk=pk)
	obj.is_ready = True
	obj.save()
	messages.success(request, f'Anexu pronto ona.')
	return redirect('fin-file-list', hashid=hashid)
