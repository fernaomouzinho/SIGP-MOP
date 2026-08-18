import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conf.decorators import allowed_users
from contract.models import Amendment
from invoice.models import Invoice, InvTrack
from finance.models import FinFiles
from finance.forms import FinFilesForm
from conf.utils import getnewid

@login_required
@allowed_users(allowed_roles=['dnof','dna'])
def FinFileList(request, hashid):
	group = request.user.groups.all()[0].name
	inv = get_object_or_404(Invoice, hashed=hashid)
	track = InvTrack.objects.filter(inv=inv).first()
	if group == "dna":
		objects = FinFiles.objects.filter(inv=inv, is_dna=True).all()
	elif group == "dnof":
		objects = FinFiles.objects.filter(inv=inv, is_dnof=True).all()
	context = {
		'group': group, 'inv': inv, 'objects': objects, 'track': track,
		'title': 'Anexu Relevantes', 'legend': 'Anexu Relevantes'
	}
	return render(request, 'finance_files/list.html', context)

@login_required
@allowed_users(allowed_roles=['dnof','dna'])
def FinFilesAdd(request, hashid):
	group = request.user.groups.all()[0].name
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
			if group == "dna": instance.is_dna = True
			elif group == "dnof": instance.is_dnof = True
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

@login_required
@allowed_users(allowed_roles=['dnof','dna'])
def FinFilesEdit(request, hashid, pk):
	group = request.user.groups.all()[0].name
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

@login_required
@allowed_users(allowed_roles=['dnof','dna'])
def FinFilesRem(request, hashid, pk):
	obj = get_object_or_404(FinFiles, pk=pk)
	obj.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('fin-file-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['dnof','dna'])
def FinFilesLock(request, hashid, pk):
	obj = get_object_or_404(FinFiles, pk=pk)
	obj.is_lock = True
	obj.save()
	messages.success(request, f'Xavi ona.')
	return redirect('fin-file-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['dnof','dna'])
def FinFilesUnlock(request, hashid, pk):
	obj = get_object_or_404(FinFiles, pk=pk)
	obj.is_lock = False
	obj.save()
	messages.success(request, f'Loke fali ona.')
	return redirect('fin-file-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['dnof','dna'])
def FinFilesReady(request, hashid, pk):
	obj = get_object_or_404(FinFiles, pk=pk)
	obj.is_ready = True
	obj.save()
	messages.success(request, f'Anexu pronto ona.')
	return redirect('fin-file-list', hashid=hashid)
