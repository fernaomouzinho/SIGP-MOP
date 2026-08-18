import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from conf.decorators import allowed_users
from django.contrib import messages
from project.models import Project
from eval.models import Eval, EvalDisp, EvalLetter, EvalTrack
from eval.forms import EvalDispForm
from conf.user_utils import c_user_dg, c_user_dgaf, c_user_div, c_user_dna, c_user_dnof
from conf.utils import getnewid
from users.decorators import allowed_users
from sigp.utils import get_roles

### DGAF
@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_dgaf_s','sigp_admin'])
def dgafEvalDispList(request):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	objects = Eval.objects.filter().all().order_by('-date','id')
	years = Eval.objects.filter().distinct().values('date__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': 'Lista Avaliasaun ToR', 'legend': 'Lista Avaliasaun ToR'
	}
	return render(request, 'eval_disp/dgaf_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_dgaf_s','sigp_admin'])
def dgafEvalDispYear(request, year):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	objects = Eval.objects.filter(date__year=year).all().order_by('-date','id')
	years = Eval.objects.filter().distinct().values('date__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Lista Avaliasaun ToR Tinan {year}', 'legend': f'Lista Avaliasaun ToR Tinan {year}'
	}
	return render(request, 'eval_disp/dgaf_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_dgaf_s','sigp_admin'])
def dgafEvalDispDet(request, hashid):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	eval = get_object_or_404(Eval, hashed=hashid)
	proj = eval.project
	objects = EvalDisp.objects.filter(eval=eval).all()
	context = {
		'group': group, 'eval': eval, 'proj': proj, 'objects': objects,
		'title': 'Detalha Avaliasaun ToR', 'legend': 'Detalha Avaliasaun ToR'
	}
	return render(request, 'eval_disp/dgaf_detail.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf','sigp_dgaf_s','sigp_admin'])
def dgafEvalDispADNLet(request, hashid, pk):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	eval = get_object_or_404(Eval, hashed=hashid)
	proj = eval.project
	disp = get_object_or_404(EvalDisp, pk=pk)
	objects = EvalLetter.objects.filter(eval=eval, is_dgaf=True).all()
	context = {
		'group': group, 'eval': eval, 'proj': proj, 'disp':disp, 'objects': objects,
		'title': 'Detalha Avaliasaun ToR', 'legend': 'Detalha Avaliasaun ToR'
	}
	return render(request, 'eval_disp/dgaf_detail.html', context)
###
@login_required
@allowed_users(allowed_roles=['sigp_dgaf_s','sigp_admin'])
def EvalDispAdd(request, hashid):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	eval = get_object_or_404(Eval, hashed=hashid)
	proj = eval.project
	track = EvalTrack.objects.filter(eval=eval).first()
	if request.method == 'POST':
		newid, new_hashid = getnewid(EvalDisp)
		form = EvalDispForm(dgaf, request.POST, request.FILES)
		if form.is_valid():		
			instance = form.save(commit=False)
			instance.id = newid
			instance.project = eval.project
			instance.eval = eval
			instance.dg = dgaf
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta ona.')
			return redirect('dgaf-eval-disp-det', hashid=hashid)
	else: form = EvalDispForm(dgaf)
	context = {
		'group': group, 'eval': eval, 'proj': proj, 'form': form,
		'title': f'Aumenta Despacho', 'legend': f'Aumenta Despacho'
	}
	return render(request, 'eval_disp/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf_s','sigp_admin'])
def EvalDispEdit(request, hashid, pk):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	eval = get_object_or_404(Eval, hashed=hashid)
	objects = get_object_or_404(EvalDisp, pk=pk)
	proj = eval.project
	if request.method == 'POST':
		form = EvalDispForm(dgaf, request.POST, request.FILES, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera ona.')
			return redirect('dgaf-eval-disp-det', hashid=hashid)
	else: form = EvalDispForm(dgaf, instance=objects)
	context = {
		'group': group, 'eval': eval, 'proj': proj, 'form': form,
		'title': f'Altera Despacho', 'legend': f'Altera Despacho'
	}
	return render(request, 'eval_disp/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf_s','sigp_admin'])
def EvalDispRem(request, hashid, pk):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	eval = get_object_or_404(Eval, hashed=hashid)
	objects = get_object_or_404(EvalDisp, pk=pk)
	objects.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('dgaf-eval-disp-det', hashid=hashid)

@login_required
@allowed_users(allowed_roles=['sigp_dgaf_s','sigp_admin'])
def EvalDispSend(request, hashid, pk):
	group = get_roles(request)
	dgaf = c_user_dgaf(request.user)
	eval = get_object_or_404(Eval, hashed=hashid)
	objects = get_object_or_404(EvalDisp, pk=pk)
	objects.is_send = True
	objects.save()
	track = EvalTrack.objects.filter(eval=eval).first()
	track.is_adn_in_2 = True
	track.date_adn_in_2 = datetime.datetime.now()
	track.is_dgaf_in = True
	track.date_dgaf_in = datetime.datetime.now()
	track.stages = "ADN mai DGPOFA."
	track.percent = 67
	track.save()
	messages.success(request, f'Manda ona.')
	return redirect('dgaf-eval-disp-det', hashid=hashid)
### DNA
@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_div','sigp_div_s', 'sigp_admin'])
def divEvalDispList(request):
	group = get_roles(request)
	if 'sigp_div' in group or 'sigp_div_s' in group: div = c_user_div(request.user)
	elif 'sigp_dna' in group or 'sigp_dna_s' in group: div = c_user_dna(request.user)
	elif 'sigp_dnof' in group or 'sigp_dnof_s' in group: div = c_user_dnof(request.user)
 
	objects = EvalDisp.objects.filter(to=div).all().order_by('-date','id')
	years = EvalDisp.objects.filter().distinct().values('date__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': 'Despacho DG ba Avaliasaun ToR', 'legend': 'Despacho DG ba Avaliasaun ToR'
	}
	return render(request, 'eval_disp/div_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_div','sigp_div_s', 'sigp_admin'])
def divEvalDispYear(request, year):
	group = get_roles(request)
	if 'sigp_dna' in group or 'sigp_dna_s' in group: div = c_user_dna(request.user)
	elif 'sigp_div' in group or 'sigp_div_s' in group: div = c_user_div(request.user)
	objects = EvalDisp.objects.filter(to=div, date__year=year).all().order_by('-date','id')
	years = EvalDisp.objects.filter().distinct().values('date__year').all()
	context = {
		'group': group, 'objects': objects, 'years': years,
		'title': f'Despacho DG ba Avaliasaun ToR Tinan {year}', 'legend': f'Despacho DG ba Avaliasaun ToR Tinan {year}'
	}
	return render(request, 'eval_disp/div_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_div','sigp_div_s', 'sigp_admin'])
def divEvalDispDet(request, hashid):
	group = get_roles(request)
	obj = get_object_or_404(EvalDisp, hashed=hashid)
	eval = obj.eval
	proj = obj.project
	context = {
		'group': group, 'eval': eval, 'proj': proj, 'obj': obj,
		'title': 'Detalha Despacho ba Avaliasaun ToR', 'legend': 'Detalha Despacho ba Avaliasaun ToR'
	}
	return render(request, 'eval_disp/div_detail.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_div','sigp_div_s', 'sigp_admin'])
def EvalDispRead(request, hashid):
	group = get_roles(request)
	objects = get_object_or_404(EvalDisp, hashed=hashid)
	objects.is_read = True
	objects.save()
	messages.success(request, f'Simu ona.')
	return redirect('div-eval-disp-det', hashid=hashid)