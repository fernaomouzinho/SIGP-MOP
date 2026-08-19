from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from project.models import ProjectEst
from eval.models import Eval, EvalFile, EvalLet, EvalTrack
from proc.models import Proc, ProcComp
from conf.user_utils import c_user_div, c_user_dna, c_user_dnof
from users.decorators import allowed_users
from sigp.utils import get_roles


@allowed_users(allowed_roles=['sigp_div','sigp_div_s','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_admin'])
def divEvalLetADNList(request, hashid):
	group = get_roles(request)
	div = c_user_div(request.user)
	dna = c_user_dna(request.user)
	eval = get_object_or_404(Eval, hashed=hashid)
	track = EvalTrack.objects.filter(eval=eval).first()
	evaldisp = EvalDisp.objects.filter(eval=eval).first()
	objects = EvalLetter.objects.filter(eval=eval, is_adn=True).all()
	context = {
		'group': group, 'eval': eval, 'evaldisp': evaldisp, 'objects': objects, 'track': track,
		'title': 'Karta Husi ADN', 'legend': 'Karta Husi ADN',
	}
	return render(request, 'eval_adn/adn_list.html', context)


@allowed_users(allowed_roles=['sigp_div','sigp_div_s','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_admin'])
def EvalLetADNList(request):
	group = get_roles(request)
	objects = Eval.objects.filter().all().order_by('-date','id')
	years = Eval.objects.filter().distinct().values('date__year').all()
	context = {
		'group': group, 'eval': eval, 'objects': objects, 'years': years,
		'title': 'Lista Avaliasaun ToR', 'legend': 'Lista Avaliasaun ToR'
	}
	return render(request, 'eval_adn/eval_list.html', context)


@allowed_users(allowed_roles=['sigp_div','sigp_div_s','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_admin'])
def EvalLetADNYear(request, year):
	group = get_roles(request)
	objects = Eval.objects.filter(date__year=year).all().order_by('-date','id')
	years = Eval.objects.filter().distinct().values('date__year').all()
	context = {
		'group': group, 'eval': eval, 'objects': objects, 'years': years,
		'title': f'Lista Avaliasaun ToR Tinan {year}', 'legend': f'Lista Avaliasaun ToR Tinan {year}'
	}
	return render(request, 'eval_adn/eval_list.html', context)


@allowed_users(allowed_roles=['sigp_div','sigp_div_s','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_admin'])
def EvalLetADNDet(request, hashid):
	group = get_roles(request)
	eval = get_object_or_404(Eval, hashed=hashid)
	objects = EvalLetter.objects.filter(eval=eval).all()
	check = EvalLetter.objects.filter(eval=eval, is_confirm=False).first()
	context = {
		'group': group, 'eval': eval, 'objects': objects, 'check': check, 'pagepdf': 'pdfadn',
		'title': 'Lista Karta Husi ADN', 'legend': 'Lista Karta Husi ADN',
	}
	return render(request, 'eval_adn/adn_list2.html', context)
