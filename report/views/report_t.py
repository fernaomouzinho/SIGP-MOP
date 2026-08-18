from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles
from django.db.models import Sum
from custom.models import Division, PCategory, Sector, Capital, StatusProj, PCat
from project.models import Project, ProjectLoc
from contract.models import Contract, ContractComp, ContractYear
from custom.models import StatusPlan, StatusImp
from django.db.models import Count
from eval.models import EvalFITrack

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rProjDash(request):
    group = get_roles(request)
    t_proj = Project.objects.filter().count()
    t_new = Project.objects.filter(statusproj_id=1).all().count()
    t_rollover = Project.objects.filter(statusproj_id=2).all().count()
    
    t_notstarted = Project.objects.filter(status_id=1).all().count()
    t_ongoing = Project.objects.filter(status_id=2).all().count()
    t_pending = Project.objects.filter(status_id=3).all().count()
    t_comp = Project.objects.filter(status_id=4).all().count()
    #
    t_imp = Contract.objects.filter().count()
    t_onprog = Contract.objects.filter(status_id=1).all().count()
    t_delay = Contract.objects.filter(status_id=2).all().count()
    t_abandon = Contract.objects.filter(status_id=3).all().count()
    t_pho = Contract.objects.filter(status_id=4).all().count()
    t_fho = Contract.objects.filter(status_id=5).all().count()
    #
    p_mopcats,p_cats,p_secs,p_caps = [],[],[],[]
    mopcats = PCat.objects.filter().all()
    for mopcat in mopcats:
        mopcats_a = Project.objects.filter(pcat=mopcat).all().count()
        p_mopcats.append([mopcat,mopcats_a])
    cats = PCategory.objects.filter().all()
    for cat in cats:
        cat_a = Project.objects.filter(pcategory=cat).all().count()
        p_cats.append([cat,cat_a])
    secs = Sector.objects.filter().all()
    for sec in secs:
        sec_a = Project.objects.filter(sector=sec).all().count()
        p_secs.append([sec,sec_a])
    caps = Capital.objects.filter().all()
    for cap in caps:
        cap_a = Project.objects.filter(capital=cap).all().count()
        p_caps.append([cap,cap_a])
    tot_type = Project.objects.filter().distinct().values('ptype').all().count()
    tot_comp = ContractComp.objects.filter(is_main=True).distinct().values('company').all().count()
    tot_loc = ProjectLoc.objects.filter(municipality__isnull=False).distinct().values('municipality').all().count()
    years = Project.objects.filter().distinct().values('year__year').order_by('-year__year')
    context = {
        'group': group, 't_proj': t_proj, 't_new': t_new, 't_rollover': t_rollover, 't_ongoing': t_ongoing, 't_notstarted': t_notstarted, 't_pending': t_pending, 't_comp': t_comp,
        't_imp': t_imp, 't_onprog': t_onprog, 't_delay': t_delay, 't_abandon': t_abandon, 't_pho': t_pho, 't_fho': t_fho,
        'p_cats': p_cats, 'p_secs': p_secs, 'p_caps': p_caps, 'tot_type': tot_type, 'tot_comp': tot_comp, 'tot_loc': tot_loc,
        'years': years, 'p_mopcats':p_mopcats,
        'title': 'Sumariu Projetu', 'legend': 'Sumariu Projetu',
    }
    return render(request, 'report_t/dash.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rProjYearDash(request, year):
    group = get_roles(request)
    t_proj = Project.objects.filter(year__year=year).count()
    
    t_notstarted = Project.objects.filter(status_id=1, year__year=year).all().count()
    t_ongoing = Project.objects.filter(status_id=2, year__year=year).all().count()
    t_pending = Project.objects.filter(status_id=3, year__year=year).all().count()
    t_comp = Project.objects.filter(status_id=4, year__year=year).all().count()
    #
    t_imp = ContractYear.objects.filter(year=year).count()
    t_onprog = ContractYear.objects.filter(contract__status_id=1, year=year).all().count()
    t_delay = ContractYear.objects.filter(contract__status_id=2, year=year).all().count()
    t_abandon = ContractYear.objects.filter(contract__status_id=3, year=year).all().count()
    t_pho = ContractYear.objects.filter(contract__status_id=4, year=year).all().count()
    t_fho = ContractYear.objects.filter(contract__status_id=5, year=year).all().count()
    #
    p_mopcats,p_cats,p_secs,p_caps = [],[],[],[]
    mopcats = PCat.objects.filter().all()
    for mopcat in mopcats:
        mopcats_a = Project.objects.filter(pcat=mopcat).all().count()
        p_mopcats.append([mopcat,mopcats_a])
    cats = PCategory.objects.filter().all()
    for cat in cats:
        cat_a = Project.objects.filter(pcategory=cat, year__year=year).all().count()
        p_cats.append([cat,cat_a])
    secs = Sector.objects.filter().all()
    for sec in secs:
        sec_a = Project.objects.filter(sector=sec, year__year=year).all().count()
        p_secs.append([sec,sec_a])
    caps = Capital.objects.filter().all()
    for cap in caps:
        cap_a = Project.objects.filter(capital=cap, year__year=year).all().count()
        p_caps.append([cap,cap_a])
    years = Project.objects.filter().distinct().values('year__year').order_by('-year__year')
    
    context = {
        'group': group, 'year': year, 't_proj': t_proj, 't_ongoing': t_ongoing, 't_notstarted': t_notstarted, 't_pending': t_pending, 't_comp': t_comp,
        't_imp': t_imp, 't_onprog': t_onprog, 't_delay': t_delay, 't_abandon': t_abandon, 't_pho': t_pho, 't_fho': t_fho,
        'p_cats': p_cats, 'p_secs': p_secs, 'p_caps': p_caps, 'p_mopcats':p_mopcats,
        'years': years, 'pk1': 1, 'pk2': 2, 'pk3': 3, 'pk4': 4, 'pk5': 5,
        'title': f'Sumariu Projetu Tinan {year}', 'legend': f'Sumariu Projetu Tinan {year}',
    }
    return render(request, 'report_t/dash_year.html', context)
### PROJ
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rProjList(request):
    group = get_roles(request)
    objects = Project.objects.filter().all()
    years = Project.objects.filter().distinct().values('year__year')
    context = {
        'group': group, 'objects': objects, 'years': years, 'page': 'pdash',
        'title': f'Lista Projetu', 'legend': f'Lista Projetu',
    }
    return render(request, 'report_t/proj_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rProjYearList(request, year):
    group = get_roles(request)
    objects = Project.objects.filter(year__year=year).all()
    years = Project.objects.filter().distinct().values('year__year')
    context = {
        'group': group, 'year': year, 'objects': objects, 'years': years, 'page': 'pyear',
        'title': f'Lista Projetu Tinan {year}', 'legend': f'Lista Projetu Tinan {year}',
    }
    return render(request, 'report_t/proj_list.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rProjStatusPList(request, pk):
    group = get_roles(request)
    status = get_object_or_404(StatusProj, pk=pk)
    objects = Project.objects.filter(statusproj=status).all()
    years = Project.objects.filter(statusproj=status).distinct().values('year__year')
    context = {
        'group': group, 'status': status, 'objects': objects, 'years': years, 'page': 'pdash',
        'title': f'Lista Projetu {status}', 'legend': f'Lista Projetu {status}',
    }
    return render(request, 'report_t/proj_statusp_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rProjStatusPYearList(request, pk, year):
    group = get_roles(request)
    status = get_object_or_404(StatusProj, pk=pk)
    objects = Project.objects.filter(statusproj=status, year__year=year).all()
    years = Project.objects.filter(statusproj=status).distinct().values('year__year')
    context = {
        'group': group, 'year': year, 'status': status, 'objects': objects, 'years': years, 'page': 'pyear',
        'title': f'Lista Projetu {status} Tinan {year}', 'legend': f'Lista Projetu {status} Tinan {year}',
    }
    return render(request, 'report_t/proj_statusp_list.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rProjStatusList(request, pk):
    group = get_roles(request)
    status = get_object_or_404(StatusPlan, pk=pk)
    objects = Project.objects.filter(status=status).all()
    years = Project.objects.filter(status=status).distinct().values('year__year')
    context = {
        'group': group, 'status': status, 'objects': objects, 'years': years, 'page': 'pdash',
        'title': f'Lista Projetu {status}', 'legend': f'Lista Projetu {status}',
    }
    return render(request, 'report_t/proj_status_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rProjStatusYearList(request, pk, year):
    group = get_roles(request)
    status = get_object_or_404(StatusPlan, pk=pk)
    objects = Project.objects.filter(status=status, year__year=year).all()
    years = Project.objects.filter(status=status).distinct().values('year__year')
    context = {
        'group': group, 'year': year, 'status': status, 'objects': objects, 'years': years, 'page': 'pyear',
        'title': f'Lista Projetu {status} Tinan {year}', 'legend': f'Lista Projetu {status} Tinan {year}',
    }
    return render(request, 'report_t/proj_status_list.html', context)
### MOPCATEGORY
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPMopCatList(request, pk):
    group = get_roles(request)
    pcat = get_object_or_404(PCat, pk=pk)
    objects = Project.objects.filter(pcat=pcat).all()
    years = Project.objects.filter(pcat=pcat).distinct().values('year__year')
    context = {
        'group': group, 'pcat': pcat, 'objects': objects, 'years': years, 'page': 'pdash',
        'title': f'Lista Projetu {pcat.name} ({pcat.code})', 'legend': f'Lista Projetu {pcat.name} ({pcat.code})',
    }
    return render(request, 'report_t/r_pmopcat_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPMopCatYearList(request, pk, year):
    group = get_roles(request)
    pcat = get_object_or_404(PCat, pk=pk)
    objects = Project.objects.filter(pcat=pcat, year__year=year).all()
    years = Project.objects.filter(pcat=pcat).distinct().values('year__year')
    context = {
        'group': group, 'year': year, 'pcat': pcat, 'objects': objects, 'years': years, 'page': 'pyear',
        'title': f'Lista Projetu {pcat.code} Tinan {year}', 'legend': f'Lista Projetu {pcat.code} Tinan {year}',
    }
    return render(request, 'report_t/r_pmopcat_list.html', context)
### CATEGORY
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPCatList(request, pk):
    group = get_roles(request)
    pcat = get_object_or_404(PCategory, pk=pk)
    objects = Project.objects.filter(pcategory=pcat).all()
    years = Project.objects.filter(pcategory=pcat).distinct().values('year__year')
    
    context = {
        'group': group, 'pcat': pcat, 'objects': objects, 'years': years, 'page': 'pdash', 
        'title': f'Lista Projetu {pcat.name} ({pcat.code})', 'legend': f'Lista Projetu {pcat.name} ({pcat.code})','legend1': f'Verifikasaun Projetu {pcat.name} ({pcat.code})','legend2': f'Inspeksaun Projetu {pcat.name} ({pcat.code})',
    }
    return render(request, 'report_t/r_pcat_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPCatYearList(request, pk, year):
    group = get_roles(request)
    pcat = get_object_or_404(PCategory, pk=pk)
    objects = Project.objects.filter(pcategory=pcat, year__year=year).all()
    years = Project.objects.filter(pcategory=pcat).distinct().values('year__year')
    context = {
        'group': group, 'year': year, 'pcat': pcat, 'objects': objects, 'years': years, 'page': 'pyear',
        'title': f'Lista Projetu {pcat.code} Tinan {year}', 'legend': f'Lista Projetu {pcat.code} Tinan {year}',
    }
    return render(request, 'report_t/r_pcat_list.html', context)
### CAPITAL
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPCapList(request, pk):
    group = get_roles(request)
    pcap = get_object_or_404(Capital, pk=pk)
    objects = Project.objects.filter(capital=pcap).all()
    years = Project.objects.filter(capital=pcap).distinct().values('year__year')
    context = {
        'group': group, 'pcap': pcap, 'objects': objects, 'years': years, 'page': 'pdash',
        'title': f'Lista Projetu {pcap.name} ({pcap.code})', 'legend': f'Lista Projetu {pcap.name} ({pcap.code})',
    }
    return render(request, 'report_t/r_pcap_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPCapYearList(request, pk, year):
    group = get_roles(request)
    pcap = get_object_or_404(Capital, pk=pk)
    objects = Project.objects.filter(capital=pcap, year__year=year).all()
    years = Project.objects.filter(capital=pcap).distinct().values('year__year')
    context = {
        'group': group, 'year': year, 'pcap': pcap, 'objects': objects, 'years': years, 'page': 'pyear',
        'title': f'Lista Projetu {pcap.code} Tinan {year}', 'legend': f'Lista Projetu {pcap.code} Tinan {year}',
    }
    return render(request, 'report_t/r_pcap_list.html', context)
### SECTOR
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPSecList(request, pk):
    group = get_roles(request)
    psec = get_object_or_404(Sector, pk=pk)
    objects = Project.objects.filter(sector=psec).all()
    years = Project.objects.filter(sector=psec).distinct().values('year__year')
    context = {
        'group': group, 'psec': psec, 'objects': objects, 'years': years, 'page': 'pdash',
        'title': f'Lista Projetu {psec}', 'legend': f'Lista Projetu {psec}',
    }
    return render(request, 'report_t/r_psec_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rPSecYearList(request, pk, year):
    group = get_roles(request)
    psec = get_object_or_404(Sector, pk=pk)
    objects = Project.objects.filter(sector=psec, year__year=year).all()
    years = Project.objects.filter(sector=psec).distinct().values('year__year')
    context = {
        'group': group, 'year': year, 'psec': psec, 'objects': objects, 'years': years, 'page': 'pyear',
        'title': f'Lista Projetu {psec} Tinan {year}', 'legend': f'Lista Projetu {psec} Tinan {year}',
    }
    return render(request, 'report_t/r_psec_list.html', context)
###
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rImpList(request):
    group = get_roles(request)
    objects = ContractYear.objects.filter().all()
    tot_sum = ContractYear.objects.filter().aggregate(Sum('total')).get('total__sum', 0.00)
    years = Contract.objects.filter().distinct().values('start_date__year')
    context = {
        'group': group, 'objects': objects, 'tot_sum': tot_sum, 'years': years, 'page': 'pdash',
        'title': f'Lista Projetu Executadu', 'legend': f'Lista Projetu Executadu',
    }
    return render(request, 'report_t/imp_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rImpYearList(request, year):
    group = get_roles(request)
    objects = ContractYear.objects.filter(year=year).all()
    tot_sum = ContractYear.objects.filter(year=year).aggregate(Sum('total')).get('total__sum', 0.00)
    years = Contract.objects.filter().distinct().values('start_date__year')
    context = {
        'group': group, 'year': year, 'objects': objects, 'tot_sum': tot_sum, 'years': years, 'page': 'pyear',
        'title': f'Lista Projetu Executadu Tinan {year}', 'legend': f'Lista Projetu Executadu Tinan {year}',
    }
    return render(request, 'report_t/imp_list.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rImpStatusList(request, pk):
    group = get_roles(request)
    status = get_object_or_404(StatusImp, pk=pk)
    objects = ContractYear.objects.filter(contract__status=status).all()
    tot_sum = ContractYear.objects.filter(contract__status=status).aggregate(Sum('total')).get('total__sum', 0.00)
    years = Contract.objects.filter(status=status).distinct().values('start_date__year')
    context = {
        'group': group, 'status': status, 'objects': objects, 'tot_sum': tot_sum, 'years': years, 'page': 'pdash',
        'title': f'Lista Projetu Executadu ho status {status}', 'legend': f'Lista Projetu Executadu ho status {status}',
    }
    return render(request, 'report_t/imp_status_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rImpStatusYearList(request, pk, year):
    group = get_roles(request)
    status = get_object_or_404(StatusImp, pk=pk)
    objects = ContractYear.objects.filter(contract__status=status, year=year).all()
    tot_sum = ContractYear.objects.filter(contract__status=status, year=year).aggregate(Sum('total')).get('total__sum', 0.00)
    years = Contract.objects.filter(status=status).distinct().values('start_date__year')
    context = {
        'group': group, 'year': year, 'status': status, 'objects': objects, 'tot_sum': tot_sum, 'years': years, 'page': 'pyear',
        'title': f'Lista Projetu Executadu ho status {status} Tinan {year}', 'legend': f'Lista Projetu Executadu ho status {status} Tinan {year}',
    }
    return render(request, 'report_t/imp_status_list.html', context)
###
@login_required
def rDivList(request):
    group = get_roles(request)
    divs = Division.objects.all()
    context = {
        'group': group, 'divs': divs,
        'title': 'Sumariu Projetu', 'legend': 'Sumariu Projetu',
    }
    return render(request, 'report_t/div_list.html', context)
