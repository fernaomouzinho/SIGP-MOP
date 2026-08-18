import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conf.decorators import allowed_users
from eval.models import Eval
from invoice.models import Invoice
from proc.models import Proc
from finance.models import CPVReq, CPV, PO
from ver.models import Ver
from insp.models import Insp
from track.models import CPVReqJustify, CPVJustify, POJustify,\
	EvalJustify, InvJustify, ProcJustify, VerJustify, VerJustify2, InspJustify, InspJustify2
from track.forms import CPVReqJustifyForm, CPVJustifyForm, POJustifyForm,\
	EvalJustifyForm, InvJustifyForm, ProcJustifyForm,\
	VerJustifyForm, VerJustify2Form, InspJustifyForm, InspJustify2Form
from conf.user_utils import c_user_dep, c_user_dgaf, c_user_div, c_user_dna, c_user_dnof, c_user_eng, c_user_min, c_user_sec
from conf.utils import getnewid
from users.decorators import allowed_users
from sigp.utils import get_roles


@login_required
@allowed_users(allowed_roles=['sigp_dnof','sigp_dgaf'])
def CPVReqJustAdd(request, hashid):
	group = get_roles(request)
	cpvreq = get_object_or_404(CPVReq, hashed=hashid)
	if request.method == 'POST':
		newid, _ = getnewid(CPVReqJustify)
		form = CPVReqJustifyForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.cpvreq = cpvreq
			if 'sigp_dnof' in group: instance.is_dnof  = True
			else: instance.is_dgaf  = True
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta succesu.')
			return redirect('track-cpvreq-det', hashid=hashid)
	else: form = CPVReqJustifyForm()
	context = {
		'group':group, 'cpvreq':cpvreq, 'form':form, 'page':'cpvreq',
		'title': 'Aumenta Justifikasaun', 'legend': 'Aumenta Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dnof','sigp_dgaf'])
def CPVReqJustEdit(request, hashid, pk):
	group = get_roles(request)
	cpvreq = get_object_or_404(CPVReq, hashed=hashid)
	obj = get_object_or_404(CPVReqJustify, pk=pk)
	if request.method == 'POST':
		form = CPVJustifyForm(request.POST, instance=obj)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera succesu.')
			return redirect('track-cpvreq-det', hashid=hashid)
	else: form = CPVJustifyForm(instance=obj)
	context = {
		'group':group, 'cpvreq':cpvreq, 'form':form, 'page':'cpvreq',
		'title': 'Altera Justifikasaun', 'legend': 'Altera Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dnof','sigp_dgaf'])
def CPVReqJustRem(request, hashid, pk):
	obj = get_object_or_404(CPVReqJustify, pk=pk)
	obj.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('track-cpvreq-det', hashid=hashid)
###
@login_required
@allowed_users(allowed_roles=['sigp_dnof','sigp_dgaf'])
def CPVJustAdd(request, hashid):
	group = get_roles(request)
	dnof = c_user_dnof(request.user)
	dgaf = c_user_dgaf(request.user)
	cpv = get_object_or_404(CPV, hashed=hashid)
	if request.method == 'POST':
		newid, _ = getnewid(CPVJustify)
		form = CPVJustifyForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.cpv = cpv
			if 'sigp_dnof' in group: 
				instance.div = dnof
				instance.is_dnof  = True
			else: 
				instance.dg = dgaf
				instance.is_dgaf  = True
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta susesu.')
			return redirect('track-cpv-det', hashid=hashid)
	else: form = CPVJustifyForm()
	context = {
		'group': group, 'cpv':cpv, 'form': form, 'page': 'cpv',
		'title': 'Aumenta Justifikasaun', 'legend': 'Aumenta Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dnof','sigp_dgaf'])
def CPVJustEdit(request, hashid, pk):
	group = get_roles(request)
	cpv = get_object_or_404(CPV, hashed=hashid)
	objects = get_object_or_404(CPVJustify, pk=pk)
	if request.method == 'POST':
		form = CPVJustifyForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera susesu.')
			return redirect('track-cpv-det', hashid=hashid)
	else: form = CPVJustifyForm(instance=objects)
	context = {
		'group':group, 'cpv':cpv, 'form':form, 'page':'cpv',
		'title': 'Altera Justifikasaun', 'legend': 'Altera Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dnof','sigp_dgaf'])
def CPVJustRem(request, hashid, pk):
	group = get_roles(request)
	obj = get_object_or_404(CPVJustify, pk=pk)
	obj.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('track-cpv-det', hashid=hashid)
###
@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dgaf'])
def POJustAdd(request, hashid):
	group = get_roles(request)
	po = get_object_or_404(PO, hashed=hashid)
	if request.method == 'POST':
		newid, _ = getnewid(POJustify)
		form = POJustifyForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.po = po
			if 'sigp_dna' in group: instance.is_dna  = True
			else: instance.is_dgaf  = True
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta susesu.')
			return redirect('track-po-det', hashid=hashid)
	else: form = POJustifyForm()
	context = {
		'group':group, 'po':po, 'form':form, 'page':'po',
		'title': 'Aumenta Justifikasaun', 'legend': 'Aumenta Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dnof','sigp_dgaf'])
def POJustEdit(request, hashid, pk):
	group = get_roles(request)
	po = get_object_or_404(PO, hashed=hashid)
	obj = get_object_or_404(POJustify, pk=pk)
	if request.method == 'POST':
		form = POJustifyForm(request.POST, instance=obj)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera susesu.')
			return redirect('track-po-det', hashid=hashid)
	else: form = POJustifyForm(instance=obj)
	context = {
		'group':group, 'po':po, 'form':form, 'page':'po',
		'title': 'Altera Justifikasaun', 'legend': 'Altera Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dgaf'])
def POJustRem(request, hashid, pk):
	obj = get_object_or_404(POJustify, pk=pk)
	obj.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('track-po-det', hashid=hashid)
###
@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_gabm'])
def EvalJustAdd(request, hashid):
	group = get_roles(request)
	eval = get_object_or_404(Eval, hashed=hashid)
	if request.method == 'POST':
		newid, _ = getnewid(EvalJustify)
		form = EvalJustifyForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.eval = eval
			if 'sigp_gabm' in group: instance.is_uvip  = False
			else: instance.is_uvip  = True
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta susesu.')
			return redirect('track-eval-det', hashid=hashid)
	else: form = EvalJustifyForm()
	context = {
		'group': group, 'eval': eval, 'form': form, 'page': 'eval',
		'title': 'Aumenta Justifikasaun', 'legend': 'Aumenta Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_gabm'])
def EvalJustEdit(request, hashid, pk):
	group = get_roles(request)
	eval = get_object_or_404(Eval, hashed=hashid)
	objects = get_object_or_404(EvalJustify, pk=pk)
	if request.method == 'POST':
		form = EvalJustifyForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera susesu.')
			return redirect('track-eval-det', hashid=hashid)
	else: form = EvalJustifyForm(instance=objects)
	context = {
		'group': group, 'eval': eval, 'form': form, 'page': 'eval',
		'title': 'Altera Justifikasaun', 'legend': 'Altera Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_gabm'])
def EvalJustRem(request, hashid, pk):
	obj = get_object_or_404(EvalJustify, pk=pk)
	obj.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('track-eval-det', hashid=hashid)
###
@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dgaf','sigp_gabm'])
def ProcJustAdd(request, hashid):
	group = get_roles(request)
	dna = c_user_dna(request.user)
	dgaf = c_user_dgaf(request.user)
	proc = get_object_or_404(Proc, hashed=hashid)
	if request.method == 'POST':
		newid, _ = getnewid(ProcJustify)
		form = ProcJustifyForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.proc = proc
			if 'sigp_dna' in group: instance.is_dna  = True
			elif 'sigp_dgaf' in group: instance.is_dgaf  = True
			elif 'sigp_gabm' in group: instance.is_gab  = True
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta susesu.')
			return redirect('track-proc-det', hashid=hashid)
	else: form = ProcJustifyForm()
	context = {
		'group': group, 'proc': proc, 'form': form, 'page': 'proc',
		'title': 'Aumenta Justifikasaun', 'legend': 'Aumenta Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dgaf','sigp_gabm'])
def ProcJustEdit(request, hashid, pk):
	group = get_roles(request)
	proc = get_object_or_404(Proc, hashed=hashid)
	objects = get_object_or_404(ProcJustify, pk=pk)
	if request.method == 'POST':
		form = ProcJustifyForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera susesu.')
			return redirect('track-proc-det', hashid=hashid)
	else: form = ProcJustifyForm(instance=objects)
	context = {
		'group': group, 'proc': proc, 'form': form, 'page': 'proc',
		'title': 'Altera Justifikasaun', 'legend': 'Altera Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dgaf','sigp_gabm'])
def ProcJustRem(request, hashid, pk):
	obj = get_object_or_404(ProcJustify, pk=pk)
	obj.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('track-proc-det', hashid=hashid)
###
@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dnof','sigp_dgaf','sigp_vice_s','sigp_min_s'])
def InvJustifyAdd(request, hashid):
	group = get_roles(request)
	dna = c_user_dna(request.user)
	dnof = c_user_dna(request.user)
	dgaf = c_user_dgaf(request.user)
	min = c_user_min(request.user)
	inv = get_object_or_404(Invoice, hashed=hashid)
	if request.method == 'POST':
		newid, _ = getnewid(InvJustify)
		form = InvJustifyForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.invoice = inv
			if "sigp_dna" in group or "sigp_dna_s" in group:
				instance.div = dna
				instance.is_dna = True

			elif "sigp_dnof" in group or "sigp_dnof_s" in group:
				instance.div = dnof
				instance.is_dnof = True

			elif "sigp_dgaf" in group or "sigp_dgaf_s" in group:
				instance.dg = dgaf
				instance.is_dgaf = True

			elif "sigp_vice_s" in group:
				instance.min = min
				instance.is_vice = True

			elif "sigp_min_s" in group:
				instance.min = min
				instance.is_min = True
    
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta susesu.')
			return redirect('track-inv-det', hashid=hashid)
	else: form = InvJustifyForm()
	context = {
		'group': group, 'inv': inv, 'form': form, 'page': 'inv',
		'title': 'Aumenta Justifikasaun', 'legend': 'Aumenta Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna_s','sigp_dnof_s','sigp_dgaf_s','sigp_vice_s','sigp_min_s'])
def InvJustifyEdit(request, hashid, pk):
	group = get_roles(request)
	inv = get_object_or_404(Invoice, hashed=hashid)
	objects = get_object_or_404(InvJustify, pk=pk)
	if request.method == 'POST':
		form = InvJustifyForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera susesu.')
			return redirect('track-proc-det', hashid=hashid)
	else: form = InvJustifyForm(instance=objects)
	context = {
		'group': group, 'inv': inv, 'form': form, 'page': 'inv',
		'title': 'Altera Justifikasaun', 'legend': 'Altera Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dgaf'])
def InvJustifyRem(request, hashid, pk):
	group = get_roles(request)
	proc = get_object_or_404(Proc, hashed=hashid)
	objects = get_object_or_404(ProcJustify, pk=pk)
	objects.delete()
	messages.success(request, f'Apaga ona.')
	return redirect('track-proc-det', hashid=hashid)
###
# @login_required
# @allowed_users(allowed_roles=['dna','dnof','div','dep','sec','eng'])
# def VerJustifyAdd(request, hashid):
# 	group = request.user.groups.all()[0].name
# 	dna = c_user_dna(request.user)
# 	dnof = c_user_dna(request.user)
# 	div = c_user_div(request.user)
# 	dep = c_user_dep(request.user)
# 	sec = c_user_sec(request.user)
# 	eng = c_user_eng(request.user)
# 	verdiv = get_object_or_404(VerLetDiv, hashed=hashid)
# 	if request.method == 'POST':
# 		newid, _ = getnewid(VerJustify)
# 		form = VerJustifyForm(request.POST)
# 		if form.is_valid():
# 			instance = form.save(commit=False)
# 			instance.id = newid
# 			instance.verdiv = verdiv
# 			if group == "dep": 
# 				instance.dep = dep
# 				instance.is_dep  = True
# 			elif group == "sec": 
# 				instance.sec = sec
# 				instance.is_sec  = True
# 			elif group == "eng": 
# 				instance.eng = eng
# 				instance.is_eng  = True
# 			elif group == "dna" or group == "dna_s": 
# 				instance.div = dna
# 				instance.is_div  = True
# 			elif group == "dnof" or group == "dnof_s": 
# 				instance.div = dnof
# 				instance.is_div  = True
# 			else: 
# 				instance.div = div
# 				instance.is_div  = True
# 			instance.datetime = datetime.datetime.now()
# 			instance.user = request.user
# 			instance.save()
# 			messages.success(request, f'Aumenta succesu.')
# 			return redirect('track-ver-det', hashid=hashid)
# 	else: form = VerJustifyForm()
# 	context = {
# 		'group': group, 'verdiv':verdiv, 'form': form, 'page': 'ver',
# 		'title': 'Aumenta Justifikasaun', 'legend': 'Aumenta Justifikasaun'
# 	}
# 	return render(request, 'track/form.html', context)

# @login_required
# @allowed_users(allowed_roles=['dna','dnof','div','dep','sec','eng'])
# def VerJustifyEdit(request, hashid, pk):
# 	group = request.user.groups.all()[0].name
# 	verdiv = get_object_or_404(VerLetDiv, hashed=hashid)
# 	objects = get_object_or_404(VerJustify, pk=pk)
# 	if request.method == 'POST':
# 		form = VerJustifyForm(request.POST, instance=objects)
# 		if form.is_valid():
# 			instance = form.save(commit=False)
# 			instance.datetime = datetime.datetime.now()
# 			instance.user = request.user
# 			instance.save()
# 			messages.success(request, f'Altera succesu.')
# 			return redirect('track-ver-det', hashid=hashid)
# 	else: form = VerJustifyForm(instance=objects)
# 	context = {
# 		'group': group, 'verdiv':verdiv, 'form': form, 'page': 'ver',
# 		'title': 'Altera Justifikasaun', 'legend': 'Altera Justifikasaun'
# 	}
# 	return render(request, 'track/form.html', context)

# @login_required
# @allowed_users(allowed_roles=['dna','dnof','div','dep','sec','eng'])
# def VerJustifyRem(request, hashid, pk):
# 	objects = get_object_or_404(VerJustify, pk=pk)
# 	objects.delete()
# 	messages.success(request, f'Hapaga ona.')
# 	return redirect('track-ver-det', hashid=hashid)
###

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_sec','sigp_eng'])
def VerJustifyAdd(request, hashid):
	group = get_roles(request)
	sec = c_user_sec(request.user)
	eng = c_user_eng(request.user)
	ver = get_object_or_404(Ver, hashed=hashid)
	if request.method == 'POST':
		newid, _ = getnewid(VerJustify2)
		form = InspJustify2Form(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.ver = ver
			if "sigp_uivp" in group:
				instance.is_uvip = True

			elif "sigp_sec" in group:
				instance.sec = sec
				instance.is_sec = True

			elif "sigp_eng" in group:
				instance.eng = eng
				instance.is_eng = True
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta susesu.')
			return redirect('track-ver-det', hashid=hashid)
	else: form = InspJustify2Form()
	context = {
		'group': group, 'ver':ver, 'form': form, 'page': 'ver',
		'title': 'Aumenta Justifikasaun', 'legend': 'Aumenta Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_sec','sigp_eng'])
def VerJustifyEdit(request, hashid, pk):
	group = get_roles(request)
	ver = get_object_or_404(Ver, hashed=hashid)
	obj = get_object_or_404(VerJustify2, pk=pk)
	if request.method == 'POST':
		form = VerJustify2Form(request.POST, instance=obj)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera susesu.')
			return redirect('track-ver-det', hashid=hashid)
	else: form = VerJustify2Form(instance=obj)
	context = {
		'group': group, 'ver':ver, 'form': form, 'page': 'ver',
		'title': 'Altera Justifikasaun', 'legend': 'Altera Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_sec','sigp_eng'])
def VerJustifyRem(request, hashid, pk):
	obj = get_object_or_404(VerJustify2, pk=pk)
	obj.delete()
	messages.success(request, f'Hamos ona.')
	return redirect('track-ver-det', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_sec','sigp_eng'])
def InspJustifyAdd(request, hashid):
	group = get_roles(request)
	sec = c_user_sec(request.user)
	eng = c_user_eng(request.user)
	insp = get_object_or_404(Insp, hashed=hashid)
	if request.method == 'POST':
		newid, _ = getnewid(InspJustify2)
		form = InspJustify2Form(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.insp = insp
			if "sigp_uivp" in group:
				instance.is_uvip = True

			elif "sigp_sec" in group:
				instance.sec = sec
				instance.is_sec = True

			elif "sigp_eng" in group:
				instance.eng = eng
				instance.is_eng = True
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Aumenta susesu.')
			return redirect('track-insp-det', hashid=hashid)
	else: form = InspJustify2Form()
	context = {
		'group': group, 'insp':insp, 'form': form, 'page': 'insp',
		'title': 'Aumenta Justifikasaun', 'legend': 'Aumenta Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_sec','sigp_eng'])
def InspJustifyEdit(request, hashid, pk):
	group = get_roles(request)
	insp = get_object_or_404(Insp, hashed=hashid)
	obj = get_object_or_404(InspJustify2, pk=pk)
	if request.method == 'POST':
		form = InspJustify2Form(request.POST, instance=obj)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera susesu.')
			return redirect('track-insp-det', hashid=hashid)
	else: form = InspJustify2Form(instance=obj)
	context = {
		'group': group, 'insp':insp, 'form': form, 'page': 'insp',
		'title': 'Altera Justifikasaun', 'legend': 'Altera Justifikasaun'
	}
	return render(request, 'track/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_sec','sigp_eng'])
def InspJustifyRem(request, hashid, pk):
	obj = get_object_or_404(InspJustify2, pk=pk)
	obj.delete()
	messages.success(request, f'Hamos ona.')
	return redirect('track-insp-det', hashid=hashid)