import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conf.decorators import allowed_users
from proc.models import Proc, ProcLet, ProcReqTrack
from proc.forms import ProcLetForm2
from users.decorators import allowed_users
from sigp.utils import get_roles

### dna
@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcReqNext(request, pk):
	proc = get_object_or_404(Proc, pk=pk)
	track = ProcReqTrack.objects.get(proc=proc)
	track.is_dna_out = True
	track.date_dna_out = datetime.datetime.now()
	track.stages = "DNA ba DGAF"
	track.percent = 11
	track.save()
	messages.success(request, f'DNA ba DGAF.')
	return redirect('dna-proc-req-det', hashid=proc.hashed)
### dgaf
@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafProcReqIn1(request, pk):
	proc = get_object_or_404(Proc, pk=pk)
	track = ProcReqTrack.objects.get(proc=proc)
	track.is_dgaf_in_1 = True
	track.date_dgaf_in_1 = datetime.datetime.now()
	track.stages = "DGAF simu husi DNA"
	track.percent = 22
	track.save()
	messages.success(request, f'DGAF simu husi DNA.')
	return redirect('dgaf-proc-req-det', hashid=proc.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafProcReqNext1(request, pk):
	obj = get_object_or_404(ProcLet, pk=pk)
	obj.is_send = True
	obj.is_read = False
	obj.is_back = False
	obj.comment = None
	obj.status = "Manda ona ba Gabinete Ministru"
	obj.save()
	proc = obj.proc
	track = ProcReqTrack.objects.get(proc=proc)
	track.is_dgaf_out_1 = True
	track.date_dgaf_out_1 = datetime.datetime.now()
	track.stages = "DGAF ba Gabinete Ministro"
	track.percent = 33
	track.save()
	messages.success(request, f'DGAF ba Gabinete Ministro.')
	return redirect('dgaf-proc-req-det', hashid=proc.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafProcReqNextDNOF(request, pk):
	obj = get_object_or_404(ProcLet, pk=pk)
	obj.is_send = True
	obj.is_read = False
	obj.is_back = False
	obj.comment = None
	obj.status = "Manda ona ba DNOF"
	obj.save()
	messages.success(request, f'DGAF ba DNOF.')
	return redirect('dgaf-proc-req-det', hashid=obj.proc.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_dnof','sigp_admin'])
def dgafProcReqInDNOF(request, pk):
	obj = get_object_or_404(ProcLet, pk=pk)
	obj.is_send = True
	obj.is_read = True
	obj.is_back = False
	obj.comment = None
	obj.status = "DNOF simu ona"
	obj.save()
	messages.success(request, f'DNOF simu ona.')
	return redirect('dnof-cpvreq-list')
### gab
@login_required
@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabProcReqBack(request, hashid):
	group = get_roles(request)
	obj = get_object_or_404(ProcLet, hashed=hashid)
	proc = obj.proc
	track = ProcReqTrack.objects.filter(proc=proc).first()
	if request.method == 'POST':
		form = ProcLetForm2(request.POST, instance=obj)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.is_back = True
			instance.is_send = False
			instance.is_read = False
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			track.is_dgaf_out_1 = False
			track.date_dgaf_out_1 = None
			track.is_gab_in = False
			track.date_gab_in = None
			track.stages = "Gabinete fila ba DGAF"
			track.percent = 38
			track.save()
			messages.success(request, f'Gabinete fila ba DGAF.')
			return redirect('gab-proc-req-det', hashid=proc.hashed)
	else: form = ProcLetForm2(instance=obj)
	context = {
		'group': group, 'proc':proc, 'obj':obj, 'form':form, 'page':'req',
		'title': 'Komentariu Manda Fila', 'legend': 'Komentariu Manda Fila'
	}
	return render(request, 'proc_gab/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabProcReqIn(request, pk):
	obj = get_object_or_404(ProcLet, pk=pk)
	obj.is_read = True
	obj.save()
	proc = obj.proc
	track = ProcReqTrack.objects.get(proc=proc)
	track.is_gab_in = True
	track.date_gab_in = datetime.datetime.now()
	track.stages = "DGAF mai Gabinete"
	track.percent = 44
	track.save()
	messages.success(request, f'DGAF mai Gabinete.')
	return redirect('gab-proc-req-det', hashid=proc.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabProcReqNext(request, pk):
	obj = get_object_or_404(ProcLet, pk=pk)
	obj.is_send = True
	obj.is_read = False
	obj.is_back = False
	obj.comment = None
	obj.status = "Manda ona ba DGAF"
	obj.save()
	proc = obj.proc
	track = ProcReqTrack.objects.get(proc=proc)
	track.is_gab_out = True
	track.date_gab_out = datetime.datetime.now()
	track.stages = "Gabinete ba DGAF"
	track.percent = 56
	track.save()
	messages.success(request, f'Gabinete ba DGAF.')
	return redirect('gab-proc-req-det', hashid=proc.hashed)
### dgaf
@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafProcReqIn2(request, pk):
	obj = get_object_or_404(ProcLet, pk=pk)
	obj.is_read = True
	obj.save()
	proc = obj.proc
	track = ProcReqTrack.objects.get(proc=proc)
	track.is_dgaf_in_2 = True
	track.date_dgaf_in_2 = datetime.datetime.now()
	track.stages = "Gabinete mai DGAF"
	track.percent = 67
	track.save()
	messages.success(request, f'Gabinete mai DGAF.')
	return redirect('dgaf-proc-req-det', hashid=proc.hashed)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_admin'])
def dgafProcReqNext2(request, pk):
	obj = get_object_or_404(ProcLet, pk=pk)
	obj.is_send = True
	obj.is_read = False
	obj.is_back = False
	obj.comment = None
	obj.status = "Manda ona ba DNA"
	obj.save()
	proc = obj.proc
	track = ProcReqTrack.objects.get(proc=proc)
	track.is_dgaf_out_2 = True
	track.date_dgaf_out_2 = datetime.datetime.now()
	track.stages = "DGAF ba DNA"
	track.percent = 78
	track.save()
	messages.success(request, f'DGAF ba DNA.')
	return redirect('dgaf-proc-req-det', hashid=proc.hashed)
### dna
@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_admin'])
def dnaProcReqIn(request, pk):
	obj = get_object_or_404(ProcLet, pk=pk)
	obj.is_read = True
	obj.save()
	proc = obj.proc
	track = ProcReqTrack.objects.get(proc=proc)
	track.is_dna_in = True
	track.date_dna_in = datetime.datetime.now()
	track.stages = "DGAF mai DNA"
	track.percent = 89
	track.save()
	messages.success(request, f'DGAF mai DNA.')
	return redirect('dna-proc-req-det', hashid=proc.hashed)