import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from eval.models import Eval, EvalTrack, EvalFITrack
from track.models import EvalJustify
from conf.user_utils import c_user_div, c_user_dnof, c_user_dna
from users.decorators import allowed_users
from sigp.utils import get_roles


@login_required
def trackEvalList(request):
    group = get_roles(request)
    evals = Eval.objects.filter().all().order_by('-date','id')
    mop_count = 0
    adn_count = 0
    sgp_count = 0

    for track in EvalFITrack.objects.all():
        entity = track.current_entity()
        if entity == "MOP":
            mop_count += 1
        elif entity == "ADN":
            adn_count += 1
        elif entity == "SGP":
            sgp_count += 1
   
    objects = []
    for i in evals:
        percent = 0
        if i.is_cna == False: track = EvalTrack.objects.filter(eval=i).last()
        else: track = EvalFITrack.objects.filter(eval=i).last()
        if track: 
            if track.percent: percent = track.percent
        objects.append([i,track,percent])
    context = {
        'group': group, 'objects': objects, 'mop_count': mop_count, 'adn_count': adn_count, 'sgp_count': sgp_count,
        'title': 'Track Avaliasaun ToR', 'legend': 'Track Avaliasaun ToR', 'legend1': f'Total Avaliasaun Projetu',
    }
    return render(request, 'track/eval_list.html', context)

@login_required
def trackdivEvalList(request):
    group = get_roles(request)
    
    if "sigp_dna" in group:
        div = c_user_dna(request.user)

    elif "sigp_dnof" in group:
        div = c_user_dnof(request.user)

    elif "sigp_div" in group:
        div = c_user_div(request.user)
    
    evals = Eval.objects.filter(div=div).all().order_by('-date','id')
    objects = []
    for i in evals:
        percent = 0
        if i.is_cna == False: track = EvalTrack.objects.filter(eval=i).last()
        else: track = EvalFITrack.objects.filter(eval=i).last()
        if track: 
            if track.percent: percent = track.percent
        objects.append([i,track,percent])
    context = {
        'group': group, 'objects': objects,
        'title': 'Track Avaliasaun ToR', 'legend': 'Track Avaliasaun ToR'
    }
    return render(request, 'track/eval_list.html', context)

@login_required
def trackEvalDet(request, hashid):
    group = get_roles(request)
    eval = get_object_or_404(Eval, hashed=hashid)
    proj = eval.proj
    track = EvalTrack.objects.filter(eval=eval).last()
    trackfi = EvalFITrack.objects.filter(eval=eval).last()
    today = datetime.date.today()
    percent,obj_days,percent2 = 0,[],0
    if track:
        if track.percent: percent = track.percent
        a,b,c,d,e,f,g,h = "","","","","","","",""
        if track.is_div_out == True and track.is_uvip_in == False:
            a = (today-track.date_div_out).days
        elif track.is_uvip_in == True:
            a = (track.date_uvip_in-track.date_div_out).days	
        #ADN
        if eval.is_adn == True:		
            if track.is_uvip_in == True and track.is_uvip_out_1 == False:
                b = (today-track.date_uvip_in).days
            if track.is_uvip_out_1 == True:
                b = (track.date_uvip_out_1-track.date_uvip_in).days
            if track.is_uvip_out_1 == True and track.is_adn_in == False:
                c = (today-track.date_uvip_out_1).days
            if track.is_adn_in == True:
                c = (track.date_adn_in-track.date_uvip_out_1).days
            if track.is_adn_in == True and track.is_uvip_out_2 == False:
                d = (today-track.date_adn_in).days
            if track.is_uvip_out_2 == True:
                d = (track.date_uvip_out_2-track.date_adn_in).days
            if track.is_uvip_out_2 == True and track.is_gab_in == False:
                e = (today-track.date_uvip_out_2).days
            elif track.is_gab_in == True and track.is_appr == False:
                e = (track.date_gab_in-track.date_uvip_out_2).days
            elif track.is_appr == True:
                e = (track.date_appr-track.date_gab_in).days
            if track.is_appr == True and track.is_end == False:
                f = (today-track.date_appr).days
            elif track.is_end == True:
                f = (track.date_end-track.date_appr).days
        else:
            if track.is_uvip_in == True and track.is_uvip_out_2 == False:
                b = (today-track.date_uvip_in).days
            if track.is_uvip_out_2 == True:
                b = (track.date_uvip_out_2-track.date_uvip_in).days
            if track.is_uvip_out_2 == True and track.is_gab_in == False:
                e = (today-track.date_uvip_out_2).days
            elif track.is_gab_in == True and track.is_appr == False:
                e = (track.date_gab_in-track.date_uvip_out_2).days
            elif track.is_appr == True:
                e = (track.date_appr-track.date_gab_in).days
            if track.is_appr == True and track.is_end == False:
                f = (today-track.date_appr).days
            elif track.is_end == True:
                f = (track.date_end-track.date_appr).days
        obj_days.append([a,b,c,d,e,f,g,h])
    justs = EvalJustify.objects.filter(eval=eval).all()
    context = {
        'group':group, 'proj':proj, 'eval':eval, 'track':track, 'trackfi':trackfi, 'percent':percent,
        'obj_days':obj_days, 'justs':justs, 'user':request.user, 'percent2':percent2,
        'title': 'Track Avaliasaun ToR', 'legend': 'Track Avaliasaun ToR'
    }
    return render(request, 'track/eval_det.html', context)
#
@login_required
def trackEvalDet2(request, hashid):
    group = get_roles(request)
    eval = get_object_or_404(Eval, hashed=hashid)
    proj = eval.proj
    track = EvalFITrack.objects.filter(eval=eval).last()
    today = datetime.date.today()
    percent,obj_days,percent2 = 0,[],0
    if track:
        if track.percent: percent = track.percent
        a,b,c,d,e,f,g,h = "","","","","","","",""
        if track.is_div_out == True and track.is_uvip_in_1 == False: a = (today-track.date_div_out).days
        elif track.is_uvip_in_1 == True: a = (track.date_uvip_in_1-track.date_div_out).days	
        #
        if track.is_uvip_out_1 == True and track.is_gab_in_1 == False: b = (today-track.date_uvip_out_1).days
        elif track.is_gab_in_1 == True and track.is_appr == False: b = (track.date_gab_in_1-track.date_uvip_out_1).days	
        elif track.is_appr == True: b = (track.date_appr-track.date_gab_in_1).days	
        #
        if track.is_appr == True and track.is_uvip_out_2 == False: c = (today-track.date_appr).days
        elif track.is_uvip_out_2 == True and track.is_uvip_in_3 == False: c = (today-track.date_uvip_out_2).days	
        elif track.is_uvip_in_3 == True: c = (track.date_uvip_in_3-track.date_uvip_out_2).days	
        #
        if track.is_uvip_out_3 == True and track.is_uvip_in_4 == False: d = (today-track.date_uvip_in_3).days
        elif track.is_uvip_in_4 == True: d = (track.date_uvip_in_4-track.date_uvip_in_3).days	
        #
        if track.is_uvip_in_4 == True and track.is_uvip_out_4 == False: e = (today-track.date_uvip_in_4).days
        elif track.is_uvip_out_4 == True: e = (track.date_uvip_out_4-track.date_uvip_in_4).days	
        #
        if track.is_uvip_out_4 == True and track.is_gab_in_2 == False: f = (today-track.date_uvip_out_4).days
        # elif track.is_gab_in_2 == True and track.is_let_appr == False: f = (track.date_gab_in_2-track.date_uvip_out_4).days	
        # elif track.is_let_appr == True: f = (track.date_let_appr-track.date_gab_in_2).days	
        #
        # if track.is_let_appr == True and track.is_uvip_out_5 == False: g = (today-track.date_let_appr).days
        # elif track.is_uvip_out_5 == True: g = (track.date_uvip_out_5-track.date_let_appr).days	
        
        obj_days.append([a,b,c,d,e,f,g,h])
    justs = EvalJustify.objects.filter(eval=eval).all()
    context = {
        'group':group, 'proj':proj, 'eval':eval, 'track':track, 'percent':percent,
        'obj_days':obj_days, 'justs':justs, 'user':request.user, 'percent2':percent2,
        'title': 'Track Avaliasaun ToR', 'legend': 'Track Avaliasaun ToR'
    }
    return render(request, 'track/eval_det2.html', context)
