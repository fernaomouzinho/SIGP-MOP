import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conf.decorators import allowed_users
from django.db import IntegrityError
from project.models import ProjectEst
from eval.models import Eval, EvalFile, EvalLet, EvalTrack
from eval.forms import EvalLetForm, EvalLetForm3,EvalLetForm4
from conf.utils import getnewid
from conf.utils import getnewid,write_roman
from users.decorators import allowed_users
from sigp.utils import get_roles

# GAB
# @login_required
# @allowed_users(allowed_roles=['gab'])
# def gabEvalList(request):
#     group = request.user.groups.all()[0].name
#     objects = Eval.objects.filter().all().order_by("-date")
#     context = {
#         'group': group, 'objects': objects,
#         'module': 'ToR', 'title': 'Lista Avaliasaun ToR', 'legend': 'Lista Avaliasaun ToR'
#     }
#     return render(request, 'eval_gab/list.html', context)

# @login_required
# @allowed_users(allowed_roles=['gab'])
# def gabEvalDet(request, hashid):
#     group = request.user.groups.all()[0].name
#     eval = get_object_or_404(Eval, hashed=hashid)
#     proj = eval.project
#     projest = ProjectEst.objects.filter(project=proj).first()
#     track = EvalTrack.objects.filter(eval=eval).first()
#     files = EvalFile.objects.filter(eval=eval).all()
#     if group == "min" or group == "min_s":
#         objects = EvalLetter.objects.filter(eval=eval, is_min=True).all()
#         let_rels = EvalLetter.objects.filter(eval=eval, is_adn=False, is_min=False).all()
#     elif group == "vice" or group == "vice_s":
#         objects = EvalLetter.objects.filter(eval=eval, is_vice=True).all()
#         let_rels = EvalLetter.objects.filter(eval=eval, is_adn=False, is_vice=False).all()
#     let_adns = EvalLetter.objects.filter(eval=eval, is_adn=True).all()
#     context = {
#         'group': group, 'eval': eval, 'proj': proj, 'projest': projest, 'files': files, 'track': track,
#         'objects': objects, 'let_rels': let_rels, 'let_adns': let_adns, 
#         'module': 'Avaliasaun ToR', 'title': 'Detalha Avaliasaun', 'legend': 'Detalha Avaliasaun',
#     }
#     return render(request, 'eval_gab/detairl.html', context)

###
# @login_required
# @allowed_users(allowed_roles=['gab'])
# def gabEvalLetAdd(request, hashid):
#     group = request.user.groups.all()[0].name
#     eval = get_object_or_404(Eval, hashed=hashid)
#     if request.method == 'POST':
#         newid, new_hashid = getnewid(EvalLetter)
#         form = EvalLetterGabForm(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.id = newid
#             instance.project = eval.project
#             instance.eval = eval
#             if group == "min_s": instance.is_min = True
#             elif group == "vice_s": instance.is_vice = True
#             instance.datetime = datetime.datetime.now()
#             instance.user = request.user
#             instance.hashed = new_hashid
#             instance.save()
#             messages.success(request, f'Aumenta ona.')
#             return redirect('gab-eval-det', hashid=hashid)
#     else: form = EvalLetterGabForm()
#     context = {
#         'group': group, 'eval': eval, 'form': form, 'page': 'pdet',
#         'title': f'Aumenta Karta', 'legend': f'Aumenta Karta'
#     }
#     return render(request, 'eval_gab/form.html', context)


@login_required
@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalLetAdd(request, hashid):
    group = get_roles(request)
    eval = get_object_or_404(Eval, hashed=hashid)
    
    if request.method == 'POST':
        newid, new_hashid = getnewid(EvalLet)
        form = EvalLetForm(request.POST, request.FILES,eval=eval)
        mt = datetime.datetime.today().month
        yr = datetime.datetime.today().year
        rom_num = write_roman(mt)
        
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                data = form.cleaned_data
                number = data['number']
                eval_number = "%s/GAB-MOP/%s/%s" % (number,rom_num,yr)
                if EvalLet.objects.filter(number=eval_number).exists():
                    form.add_error('number', f"'{eval_number}' eziste ona.")
                else:
                    instance.id = newid
                    instance.number = eval_number
                    instance.eval = eval
                    instance.datetime = datetime.datetime.now()
                    instance.user = request.user
                    instance.hashed = new_hashid
                    instance.save()
                    messages.success(request, f'Aumenta ona.')
                    return redirect('gab-eval-det', hashid=hashid)
        
            except IntegrityError as e:
                # Friendly message for duplicate
                form.add_error('number', f"'{number}' eziste ona.")
                
    else: form = EvalLetForm(eval=eval)
    context = {
        'group':group, 'eval':eval, 'form':form,
        'title': f'Aumenta Karta', 'legend': f'Aumenta Karta'
    }
    return render(request, 'eval_gab/form.html', context)


@login_required
@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalLetEdit(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(EvalLet, hashed=hashid)
    eval = obj.eval
    
    if request.method == 'POST':
        form = EvalLetForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            try:    
                instance = form.save(commit=False)
                data = form.cleaned_data
                number = data['number']
                if EvalLet.objects.filter(number=number).exists():
                    form.add_error('number', f"'{number}' eziste ona.")
                else:
                    instance.datetime = datetime.datetime.now()
                    instance.user = request.user
                    instance.save()
                    messages.success(request, f'Altera ona.')
                return redirect('gab-eval-det', hashid=eval.hashed)
            except IntegrityError as e:
            # Friendly message for duplicate
                form.add_error('number', f"'{number}' eziste ona.")
    
    else: form = EvalLetForm(instance=obj)
    context = {
        'group':group, 'eval':eval, 'form':form,
        'title': f'Altera Karta', 'legend': f'Altera Karta'
    }
    return render(request, 'eval_gab/form.html', context)


# @login_required
# @allowed_users(allowed_roles=['sigp_gabm'])
# def gabEvalLetEdit(request, hashid, pk):
# 	group = request.user.groups.all()[0].name
# 	eval = get_object_or_404(Eval, hashed=hashid)
# 	objects = get_object_or_404(EvalLetter, pk=pk)
# 	if request.method == 'POST':
# 		form = EvalLetterGabForm(request.POST, request.FILES, instance=objects)
# 		if form.is_valid():
# 			instance = form.save(commit=False)
# 			instance.datetime = datetime.datetime.now()
# 			instance.user = request.user
# 			instance.save()
# 			messages.success(request, f'Aumenta ona.')
# 			return redirect('gab-eval-det', hashid=hashid)
# 	else: form = EvalLetterGabForm(instance=objects)
# 	context = {
# 		'group': group, 'eval': eval, 'form': form, 'page': 'pdet',
# 		'title': f'Altera Karta', 'legend': f'Altera Karta'
# 	}
# 	return render(request, 'eval_gab/form.html', context)

# @login_required
# @allowed_users(allowed_roles=['gab'])
# def gabEvalLetRem(request, hashid, pk):
# 	group = request.user.groups.all()[0].name
# 	eval = get_object_or_404(Eval, hashed=hashid)
# 	objects = get_object_or_404(EvalLetter, pk=pk)
# 	objects.delete()
# 	messages.success(request, f'Hamos ona.')
# 	return redirect('gab-eval-det', hashid=hashid)


@login_required
@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalLetRem(request, pk):
    obj = get_object_or_404(EvalLet, pk=pk)
    eval = obj.eval
    obj.delete()
    trackfile = EvalTrack.objects.filter(eval=eval).first()	
    trackfile.is_gab_out_1 = False
    trackfile.date_gab_out_1 = None
    trackfile.save()
    messages.success(request, f'Hamos ona.')
    return redirect('gab-eval-det', hashid=eval.hashed)