import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conf.decorators import allowed_users
from proc.models import Proc, ProcFiles
from proc.forms import ProcFilesForm
from conf.user_utils import c_user_dna
from conf.utils import getnewid
from users.decorators import allowed_users
from sigp.utils import get_roles


@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_admin'])
def dnaProcFileList(request, hashid):
	group = get_roles(request)
	dna = c_user_dna(request.user)
	proc = get_object_or_404(Proc, hashed=hashid)
	proj = proc.project
	objects = ProcFiles.objects.filter(proc=proc).all()
	context = {
		'group': group, 'proc': proc, 'proj': proj, 'objects': objects,
		'title': 'Lista Documentu', 'legend': 'Lista Documentu',
	}
	return render(request, 'proc/file_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_admin'])
def dnaProcFileAdd(request, hashid):
	group = get_roles(request)
	dna = c_user_dna(request.user)
	proc = get_object_or_404(Proc, hashed=hashid)
	proj = proc.project
	if request.method == 'POST':
		newid, new_hashid = getnewid(ProcFiles)
		form = ProcFilesForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.proc = proc
			instance.project = proc.project
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta ona.')
			return redirect('dna-proc-file-list', hashid=hashid)
	else: form = ProcFilesForm()
	context = {
		'group': group, 'proj': proj, 'proc': proc, 'form': form,
		'title': 'Aumenta Dokumentu', 'legend': 'Aumenta Dokumentu'
	}
	return render(request, 'proc/file_form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_admin'])
def dnaProcFileEdit(request, hashid, hashid2):
	group = get_roles(request)
	dna = c_user_dna(request.user)
	proc = get_object_or_404(Proc, hashed=hashid)
	objects = get_object_or_404(ProcFiles, hashed=hashid2)
	if request.method == 'POST':
		form = ProcFilesForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera ona.')
			return redirect('dna-proc-file-list', hashid=hashid)
	else: form = ProcFilesForm(instance=objects)
	context = {
		'group': group, 'proc': proc, 'form': form,
		'title': 'Altera Dokumentu', 'legend': 'Altera Dokumentu'
	}
	return render(request, 'proc/file_form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_admin'])
def dnaProcFileRem(request, hashid, pk):
	group = get_roles(request)
	objects = get_object_or_404(ProcFiles, pk=pk)
	objects.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('dna-proc-file-list', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_admin'])
def dnaProcFileLock(request, hashid, pk):
	group = get_roles(request)
	objects = get_object_or_404(ProcFiles, pk=pk)
	objects.is_lock = True
	objects.save()
	messages.success(request, f'Xavi.')
	return redirect('dna-proc-file-list', hashid=hashid)