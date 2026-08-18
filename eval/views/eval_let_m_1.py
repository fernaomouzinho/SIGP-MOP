import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conf.decorators import allowed_users
from eval.models import Eval, EvalLet, EvalTrack, EvalFITrack
from eval.forms import EvalLetForm2
from users.decorators import allowed_users
from sigp.utils import get_roles

### div
@login_required
@allowed_users(allowed_roles=['sigp_sdiv','sigp_dna','sigp_dnof'])
def divEvalSend(request, hashid):
    eval = get_object_or_404(Eval, hashed=hashid)
    eval.is_send = True
    eval.save()
    proj = eval.proj
    fi = proj.pcategory.id
    
    if fi == 1: 
        eval.is_adn = True
        eval.is_cna = True
        eval.save()
        track = EvalFITrack.objects.filter(eval=eval).first()
        percent = 7
    else:
        track = EvalTrack.objects.filter(eval=eval).first()
        percent = 13
    track.is_div_out = True
    track.date_div_out = datetime.datetime.now()
    track.stages = "DIV ba UIVP"
    track.percent = percent
    track.save()
    messages.success(request, f'DIV ba UIVP.')
    return redirect('div-eval-det', hashid=hashid)
#
@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalIn(request, pk):
    eval = get_object_or_404(Eval, pk=pk)
    eval.is_read = True
    eval.save()
    proj = eval.proj
    fi = proj.pcategory.id
    if fi == 1:
        track = EvalFITrack.objects.filter(eval=eval).first()
        track.is_uvip_in_1 = True
        track.date_uvip_in_1 = datetime.datetime.now()
        percent = 14
    else:
        track = EvalTrack.objects.filter(eval=eval).first()
        track.is_uvip_in = True
        track.date_uvip_in = datetime.datetime.now()
        percent = 25
    track.stages = "UIVP Simu"
    track.percent = percent
    track.save()
    messages.success(request, f'UIVP Simu.')
    return redirect('uvip-eval-det', hashid=eval.hashed)

#
@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalVerStart(request, hashid):
    eval = get_object_or_404(Eval, hashed=hashid)
    proj = eval.proj
    
    fi = proj.pcategory.id
    if fi == 1:
        track = EvalFITrack.objects.filter(eval=eval).first()
        track.is_ver_start = True
        track.date_ver_start = datetime.datetime.now()
        track.percent = 19
    else:
        track = EvalTrack.objects.filter(eval=eval).first()
        track.is_ver_start = True
        track.date_ver_start = datetime.datetime.now()
        track.percent = 30
    
    track.stages = "Verifikasaun hahu"
    track.save()
    messages.success(request, f'Verifikasaun hahu.')
    return redirect('uvip-eval-list2', hashid=hashid)


@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalVerEnd(request, hashid):
    eval = get_object_or_404(Eval, hashed=hashid)
    proj = eval.proj
    
    fi = proj.pcategory.id
    if fi == 1:
        track = EvalFITrack.objects.filter(eval=eval).first()
        track.is_ver_end = True
        track.date_ver_end = datetime.datetime.now()
        track.percent = 25
    else:
        track = EvalTrack.objects.filter(eval=eval).first()
        track.is_ver_end = True
        track.date_ver_end = datetime.datetime.now()
        track.percent = 35
        
    track.stages = "Verifikasaun remata"
    track.save()
    messages.success(request, f'Verifikasaun remata.')
    return redirect('uvip-eval-det', hashid=hashid)


@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalNext1(request, pk):
    obj = get_object_or_404(EvalLet, pk=pk)
    obj.is_send = True
    obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalTrack.objects.filter(eval=eval).first()
    track.is_uvip_out_1 = True
    track.date_uvip_out_1 = datetime.datetime.now()
    track.is_adn_in = False
    track.date_adn_in = None
    track.stages = "UIVP ba ADN"
    track.percent = 38
    track.save()
    messages.success(request, f'UIVP ba ADN.')
    return redirect('uvip-eval-det', hashid=eval.hashed)


@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalADNIn(request, pk):
    eval = get_object_or_404(Eval, pk=pk)
    track = EvalTrack.objects.filter(eval=eval).first()
    track.is_adn_in = True
    track.date_adn_in = datetime.datetime.now()
    track.stages = "ADN mai UIVP"
    track.percent = 50
    track.save()
    messages.success(request, f'ADN mai UIVP.')
 
    return redirect('uvip-eval-det', hashid=eval.hashed)


@login_required
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalNext2(request, pk):
    obj = get_object_or_404(EvalLet, pk=pk)
    obj.is_send = True
    obj.is_back = False
    obj.comment = None
    obj.save()
    eval = obj.eval
    track = EvalTrack.objects.filter(eval=eval).first()
    track.is_uvip_out_2 = True
    track.date_uvip_out_2 = datetime.datetime.now()
    track.stages = "UIVP ba Gabinete Ministru"
    track.percent = 63
    track.save()
    messages.success(request, f'UIVP ba Gabinete Ministru.')
    return redirect('uvip-eval-det', hashid=eval.hashed)

### gab
@login_required
@allowed_users(allowed_roles=['sigp_gabm'])
def gabEvalBack(request, hashid):
    group = get_roles(request)
    obj = get_object_or_404(EvalLet, hashed=hashid)
    eval = obj.eval
    fi = eval.proj.pcategory.id
    if fi == 1: track = EvalFITrack.objects.filter(eval=eval).first()
    else: track = EvalTrack.objects.filter(eval=eval).first()
    if request.method == 'POST':
        form = EvalLetForm2(request.POST, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_back = True
            instance.is_send = False
            instance.is_read = False
            instance.datetime = datetime.datetime.now()
            instance.user = request.user
            instance.save()
            obj.status = "Gabinete Ministru Manda Fila"
            obj.save()
            if fi == 1:
                track.is_uvip_out_1 = False
                track.date_uvip_out_1 = None
                track.stages = "Gabinete Ministru fila ba UIVP"
                track.percent = 13
                track.save()
            else:
                track.is_uvip_out_2 = False
                track.date_uvip_out_2 = None
                track.stages = "Gabinete Ministru fila ba UIVP"
                track.percent = 38
                track.save()
            messages.success(request, f'Gabinete Ministru fila ba UIVP.')
            return redirect('gab-eval-det', hashid=eval.hashed)
    else: form = EvalLetForm2(instance=obj)
    context = {
        'group': group, 'eval':eval, 'obj':obj, 'form':form,
        'title': 'Komentariu Manda Fila', 'legend': 'Komentariu Manda Fila'
    }
    return render(request, 'eval_gab/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_gabm'])
def gabEvalIn(request, pk):
    obj = get_object_or_404(EvalLet, pk=pk)
    obj.is_read = True
    obj.save()
    eval = obj.eval
    track = EvalTrack.objects.filter(eval=eval).first()
    track.is_gab_in = True
    track.date_gab_in = datetime.datetime.now()
    track.stages = "Gabinete Ministru Simu"
    track.percent = 86
    track.save()
    messages.success(request, f'Gabinete Ministru Simu.')
    return redirect('gab-eval-det', hashid=eval.hashed)
###