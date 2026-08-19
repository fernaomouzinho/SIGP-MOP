import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from invoice.models import Invoice, InvTrack
from track.models import InvJustify
from conf.user_utils import c_user_comp
from users.decorators import allowed_users
from sigp.utils import get_roles

def trackInvList(request):
    group = get_roles(request)
    invs = Invoice.objects.filter().all().order_by('-date')
    objects = []
    for i in invs:
        track = InvTrack.objects.filter(inv=i).first()
        contcomp = i.cont.contractcomp.first()
        percent = 0
        if track:
            if track.percent: percent = track.percent
        objects.append([i,track,percent, contcomp])
    context = {
        'group': group, 'objects': objects,
        'title': 'Track Resibu', 'legend': 'Track Resibu'
    }
    return render(request, 'track/inv_list.html', context)


def trackInvDet(request, hashid):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    track = InvTrack.objects.filter(inv=inv).first()
    contcomp = inv.cont.contractcomp.first()
    today = datetime.date.today()
    percent,obj_days = 0,[]
    if track:
        if track.percent: percent = track.percent
        a,b,c,d,e,f,g,h,i = 0,0,0,0,0,0,0,0,0
        # sup-uvip
        if track.is_sup_out == True and track.is_uvip_in == False: a = (today-track.date_sup_out).days
        elif track.is_uvip_in == True: a = (track.date_uvip_in-track.date_sup_out).days
        # uvip-ver
        if track.is_uvip_in == True and track.is_insp_start == False: b = (today-track.date_uvip_in).days
        elif track.is_insp_start == True and track.is_insp_end == False: b = (track.date_uvip_in-track.date_insp_start).days
        elif track.is_insp_end == True: b = (track.date_insp_end-track.date_insp_start).days
        if inv.is_adn == False:
            # ver
            if track.is_insp_end == True and track.is_uvip_out_2 == False: e = (today-track.date_insp_end).days
            elif track.is_uvip_out_2 == True: e = (track.date_uvip_out_2-track.date_insp_end).days
            # gab
            if track.is_gab_in == True and track.is_gab_out == False: f = (today-track.date_gab_in).days
            elif track.is_gab_out == True: f = (track.date_gab_out-track.date_gab_in).days
            # dgaf
            if track.is_dgaf_in == True and track.is_dgaf_out == False: g = (today-track.date_dgaf_in).days
            elif track.is_dgaf_out == True: g = (track.date_dgaf_out-track.date_dgaf_in).days
            # dna
            if track.is_dna_in == True and track.is_dna_out == False: h = (today-track.date_dna_in).days
            elif track.is_dna_out == True: h = (track.date_dna_out-track.date_dna_in).days
            # dnof
            if track.is_dnof_in == True and track.is_dnof_out == False: i = (today-track.date_dnof_in).days
            elif track.is_dnof_out == True: i = (track.date_dnof_out-track.date_dnof_in).days
        else:
            # ver
            if track.is_insp_end == True and track.is_uvip_out_1 == False: c = (today-track.date_insp_end).days
            elif track.is_uvip_out_1 == True: c = (track.date_uvip_out_1-track.date_insp_end).days
            # uvip-adn
            if track.is_uvip_out_1 == True and track.is_adn_in == False: d = (today-track.date_uvip_out_1).days
            elif track.is_adn_in == True: d = (track.date_adn_in-track.date_uvip_out_1).days
            # uvip-gab
            if track.is_adn_in == True and track.is_uvip_out_2 == False: e = (today-track.date_adn_in).days
            elif track.is_uvip_out_2 == True: e = (track.date_uvip_out_2-track.date_adn_in).days
            if inv.is_cna == False:
                # gab
                if track.is_gab_in == True and track.is_gab_out == False: f = (today-track.date_gab_in).days
                elif track.is_gab_out == True: f = (track.date_gab_out-track.date_gab_in).days
                # dgaf
                if track.is_dgaf_in == True and track.is_dgaf_out == False: g = (today-track.date_dgaf_in).days
                elif track.is_dgaf_out == True: g = (track.date_dgaf_out-track.date_dgaf_in).days
            else:
                if track.is_gab_in == True and track.is_gab_out == False: f = (today-track.date_gab_in).days
                elif track.is_gab_out == True: f = (track.date_gab_out-track.date_gab_in).days
            # dna
            if track.is_dna_in == True and track.is_dna_out == False: h = (today-track.date_dna_in).days
            elif track.is_dna_out == True: h = (track.date_dna_out-track.date_dna_in).days
            # dnof
            if track.is_dnof_in == True and track.is_dnof_out == False: i = (today-track.date_dnof_in).days
            elif track.is_dnof_out == True: i = (track.date_dnof_out-track.date_dnof_in).days
        total = a+b+c+d+e+f+g+h+i
        obj_days.append([a,b,c,d,e,f,g,h,i,total])
    
    justs = InvJustify.objects.filter(inv=inv).all()
    context = {
        'group': group, 'inv': inv, 'contcomp':contcomp,'track': track, 'percent': percent,
        'obj_days': obj_days, 'justs': justs,
        'title': ' Track Resibu', 'legend': 'Track Resibu'
    }
    return render(request, 'track/inv_det.html', context)
###

def compTrackInvList(request):
    group = get_roles(request)
    comp = c_user_comp(request.user)
    invs = Invoice.objects.filter(cont__contractcomp__company=comp).all().order_by('-date')
    objects = []
    for i in invs:
        track = InvTrack.objects.filter(inv=i).first()
        percent = 0
        if track:
            if track.percent: percent = track.percent
        objects.append([i,track,percent,comp])
    context = {
        'group': group, 'objects': objects,
        'title': 'Track Resibu', 'legend': 'Track Resibu'
    }
    return render(request, 'track/inv_c_list.html', context)


def compTrackInvDet(request, hashid):
    group = get_roles(request)
    inv = get_object_or_404(Invoice, hashed=hashid)
    track = InvTrack.objects.filter(inv=inv).first()
    contcomp = inv.cont.contractcomp.first()
    today = datetime.date.today()
    percent,obj_days = 0,[]
    if track:
        if track.percent: percent = track.percent
        a,b,c,d,e,f,g,h,i = 0,0,0,0,0,0,0,0,0
        # sup-uvip
        if track.is_sup_out == True and track.is_uvip_in == False: a = (today-track.date_sup_out).days
        elif track.is_uvip_in == True: a = (track.date_uvip_in-track.date_sup_out).days
        # uvip-ver
        if track.is_uvip_in == True and track.is_insp_start == False: b = (today-track.date_uvip_in).days
        elif track.is_insp_start == True and track.is_insp_end == False: b = (track.date_uvip_in-track.date_insp_start).days
        elif track.is_insp_end == True: b = (track.date_insp_end-track.date_insp_start).days
        if inv.is_adn == False:
            # ver
            if track.is_insp_end == True and track.is_uvip_out_2 == False: e = (today-track.date_insp_end).days
            elif track.is_uvip_out_2 == True: e = (track.date_uvip_out_2-track.date_insp_end).days
            # gab
            if track.is_gab_in == True and track.is_gab_out == False: f = (today-track.date_gab_in).days
            elif track.is_gab_out == True: f = (track.date_gab_out-track.date_gab_in).days
            # dgaf
            if track.is_dgaf_in == True and track.is_dgaf_out == False: g = (today-track.date_dgaf_in).days
            elif track.is_dgaf_out == True: g = (track.date_dgaf_out-track.date_dgaf_in).days
            # dna
            if track.is_dna_in == True and track.is_dna_out == False: h = (today-track.date_dna_in).days
            elif track.is_dna_out == True: h = (track.date_dna_out-track.date_dna_in).days
            # dnof
            if track.is_dnof_in == True and track.is_dnof_out == False: i = (today-track.date_dnof_in).days
            elif track.is_dnof_out == True: i = (track.date_dnof_out-track.date_dnof_in).days
        else:
            # ver
            if track.is_insp_end == True and track.is_uvip_out_1 == False: c = (today-track.date_insp_end).days
            elif track.is_uvip_out_1 == True: c = (track.date_uvip_out_1-track.date_insp_end).days
            # uvip-adn
            if track.is_uvip_out_1 == True and track.is_adn_in == False: d = (today-track.date_uvip_out_1).days
            elif track.is_adn_in == True: d = (track.date_adn_in-track.date_uvip_out_1).days
            # uvip-gab
            if track.is_adn_in == True and track.is_uvip_out_2 == False: e = (today-track.date_adn_in).days
            elif track.is_uvip_out_2 == True: e = (track.date_uvip_out_2-track.date_adn_in).days
            if inv.is_sgp == False:
                # gab
                if track.is_gab_in == True and track.is_gab_out == False: f = (today-track.date_gab_in).days
                elif track.is_gab_out == True: f = (track.date_gab_out-track.date_gab_in).days
                # dgaf
                if track.is_dgaf_in == True and track.is_dgaf_out == False: g = (today-track.date_dgaf_in).days
                elif track.is_dgaf_out == True: g = (track.date_dgaf_out-track.date_dgaf_in).days
            else:
                if track.is_gab_in == True and track.is_gab_out == False: f = (today-track.date_gab_in).days
                elif track.is_gab_out == True: f = (track.date_gab_out-track.date_gab_in).days
            # dna
            if track.is_dna_in == True and track.is_dna_out == False: h = (today-track.date_dna_in).days
            elif track.is_dna_out == True: h = (track.date_dna_out-track.date_dna_in).days
            # dnof
            if track.is_dnof_in == True and track.is_dnof_out == False: i = (today-track.date_dnof_in).days
            elif track.is_dnof_out == True: i = (track.date_dnof_out-track.date_dnof_in).days
        total = a+b+c+d+e+f+g+h+i
        obj_days.append([a,b,c,d,e,f,g,h,i,total])
    
    justs = InvJustify.objects.filter(inv=inv).all()
    context = {
        'group': group, 'inv': inv,'contcomp':contcomp, 'track': track, 'percent': percent,
        'obj_days': obj_days, 'justs': justs,
        'title': 'Track Resibu', 'legend': 'Track Resibu'
    }
    return render(request, 'track/inv_c_det.html', context)