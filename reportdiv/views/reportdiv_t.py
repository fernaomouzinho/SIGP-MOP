from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from custom.models import Division, PCategory, Sector, Capital, StatusProj
from project.models import Project, ProjectLoc
from contract.models import Contract, ContractComp, ContractYear
from custom.models import StatusPlan, StatusImp
from conf.user_utils import c_user_div, c_user_dna, c_user_dnof
from users.decorators import allowed_users
from sigp.utils import get_roles


def rdivDash(request):
	group = get_roles(request)
	div = []
	if "sigp_dna" in group:
		div = c_user_dna(request.user)

	elif "sigp_dnof" in group:
		div = c_user_dnof(request.user)

	elif "sigp_div" in group:
		div = c_user_div(request.user)
	
	context = {
		'group': group, 'div': div,
		'title': 'Sumariu Projetu', 'legend': 'Sumariu Projetu',
	}
	return render(request, 'reportdiv_t/dash_div.html', context)


def rdivProjDash(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	t_proj = Project.objects.filter(owner=div).count()
	t_new = Project.objects.filter(owner=div, statusproj_id=1).all().count()
	t_rollover = Project.objects.filter(owner=div, statusproj_id=2).all().count()
	
	t_notstarted = Project.objects.filter(owner=div, status_id=1).all().count()
	t_ongoing = Project.objects.filter(owner=div, status_id=2).all().count()
	t_pending = Project.objects.filter(owner=div, status_id=3).all().count()
	t_comp = Project.objects.filter(owner=div, status_id=4).all().count()
	#
	t_imp = Contract.objects.filter(project__owner=div).count()
	t_onprog = Contract.objects.filter(project__owner=div, status_id=1).all().count()
	t_delay = Contract.objects.filter(project__owner=div, status_id=2).all().count()
	t_abandon = Contract.objects.filter(project__owner=div, status_id=3).all().count()
	t_pho = Contract.objects.filter(project__owner=div, status_id=4).all().count()
	t_fho = Contract.objects.filter(project__owner=div, status_id=5).all().count()
	#
	p_cats,p_secs,p_caps = [],[],[]
	cats = PCategory.objects.filter().all()
	for cat in cats:
		cat_a = Project.objects.filter(owner=div, pcategory=cat).all().count()
		p_cats.append([cat,cat_a])
	secs = Sector.objects.filter().all()
	for sec in secs:
		sec_a = Project.objects.filter(owner=div, sector=sec).all().count()
		p_secs.append([sec,sec_a])
	caps = Capital.objects.filter().all()
	for cap in caps:
		cap_a = Project.objects.filter(owner=div, capital=cap).all().count()
		p_caps.append([cap,cap_a])
	tot_type = Project.objects.filter(owner=div).distinct().values('ptype').all().count()
	tot_comp = ContractComp.objects.filter(contract__project__owner=div, is_main=True).distinct().values('company').all().count()
	tot_loc = ProjectLoc.objects.filter(municipality__isnull=False).distinct().values('municipality').all().count()
	years = Project.objects.filter().distinct().values('year__year').order_by('-year__year')
	context = {
		'group': group, 'div': div, 't_proj': t_proj, 't_new': t_new, 't_rollover': t_rollover, 't_ongoing': t_ongoing, 't_notstarted': t_notstarted, 't_pending': t_pending, 't_comp': t_comp,
		't_imp': t_imp, 't_onprog': t_onprog, 't_delay': t_delay, 't_abandon': t_abandon, 't_pho': t_pho, 't_fho': t_fho,
		'p_cats': p_cats, 'p_secs': p_secs, 'p_caps': p_caps, 'tot_type': tot_type, 'tot_comp': tot_comp, 'tot_loc': tot_loc,
		'years': years, 'pk1': 1, 'pk2': 2, 'pk3': 3, 'pk4': 4, 'pk5': 5, 'page': 'pdiv',
		'title': 'Sumariu Projetu', 'legend': 'Sumariu Projetu',
	}
	return render(request, 'reportdiv_t/dash.html', context)


def rdivProjYearDash(request, pk, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	t_proj = Project.objects.filter(owner=div, year__year=year).count()
	t_new = Project.objects.filter(owner=div, statusproj_id=1, year__year=year).all().count()
	t_rollover = Project.objects.filter(owner=div, statusproj_id=2).all().count()
	
	t_notstarted = Project.objects.filter(owner=div, status_id=1, year__year=year).all().count()
	t_ongoing = Project.objects.filter(owner=div, status_id=2, year__year=year).all().count()
	t_pending = Project.objects.filter(owner=div, status_id=3, year__year=year).all().count()
	t_comp = Project.objects.filter(owner=div, status_id=4, year__year=year).all().count()
	#
	t_imp = ContractYear.objects.filter(contract__project__owner=div, year=year).count()
	t_onprog = ContractYear.objects.filter(contract__project__owner=div, contract__status_id=1, year=year).all().count()
	t_delay = ContractYear.objects.filter(contract__project__owner=div, contract__status_id=2, year=year).all().count()
	t_abandon = ContractYear.objects.filter(contract__project__owner=div, contract__status_id=3, year=year).all().count()
	t_pho = ContractYear.objects.filter(contract__project__owner=div, contract__status_id=4, year=year).all().count()
	t_fho = ContractYear.objects.filter(contract__project__owner=div, contract__status_id=5, year=year).all().count()
	#
	p_cats,p_secs,p_caps = [],[],[]
	cats = PCategory.objects.filter().all()
	for cat in cats:
		cat_a = Project.objects.filter(owner=div, pcategory=cat, year__year=year).all().count()
		p_cats.append([cat,cat_a])
	secs = Sector.objects.filter().all()
	for sec in secs:
		sec_a = Project.objects.filter(owner=div, sector=sec, year__year=year).all().count()
		p_secs.append([sec,sec_a])
	caps = Capital.objects.filter().all()
	for cap in caps:
		cap_a = Project.objects.filter(owner=div, capital=cap, year__year=year).all().count()
		p_caps.append([cap,cap_a])
	years = Project.objects.filter().distinct().values('year__year').order_by('-year__year')
	
	context = {
		'group': group, 'div': div, 'year': year, 't_proj': t_proj, 't_new': t_new, 't_rollover': t_rollover, 't_ongoing': t_ongoing, 't_notstarted': t_notstarted, 't_pending': t_pending, 't_comp': t_comp,
		't_imp': t_imp, 't_onprog': t_onprog, 't_delay': t_delay, 't_abandon': t_abandon, 't_pho': t_pho, 't_fho': t_fho,
		'p_cats': p_cats, 'p_secs': p_secs, 'p_caps': p_caps, 'years': years, 
		'pk1': 1, 'pk2': 2, 'pk3': 3, 'pk4': 4, 'pk5': 5, 'page': 'pdiv',
		'title': f'Sumariu Projetu Tinan {year}', 'legend': f'Sumariu Projetu Tinan {year}',
	}
	return render(request, 'reportdiv_t/dash_year.html', context)
### PROJ

def rdivProjList(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = Project.objects.filter(owner=div).all()
	years = Project.objects.filter(owner=div).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'objects': objects, 'years': years, 'page': 'pdash',
		'subtitle': subtitle, 'title': f'Lista Projetu', 'legend': f'Lista Projetu',
	}
	return render(request, 'reportdiv_t/proj_list.html', context)


def rdivProjYearList(request, pk, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = Project.objects.filter(owner=div, year__year=year).all()
	years = Project.objects.filter(owner=div).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'year': year, 'objects': objects, 'years': years, 'page': 'pyear',
		'subtitle': subtitle, 'title': f'Lista Projetu Tinan {year}', 'legend': f'Lista Projetu Tinan {year}',
	}
	return render(request, 'reportdiv_t/proj_list.html', context)
#

def rdivProjStatusPList(request, pk, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	status = get_object_or_404(StatusProj, pk=pk2)
	objects = Project.objects.filter(owner=div, statusproj=status).all()
	years = Project.objects.filter(owner=div, statusproj=status).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'status': status, 'objects': objects, 'years': years, 'page': 'pdash',
		'subtitle': subtitle, 'title': f'Lista Projetu {status}', 'legend': f'Lista Projetu {status}',
	}
	return render(request, 'reportdiv_t/proj_statusp_list.html', context)


def rdivProjStatusPYearList(request, pk, pk2, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	status = get_object_or_404(StatusProj, pk=pk2)
	objects = Project.objects.filter(owner=div, statusproj=status, year__year=year).all()
	years = Project.objects.filter(owner=div, statusproj=status).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'year': year, 'status': status, 'objects': objects, 'years': years, 'page': 'pyear',
		'subtitle': subtitle, 'title': f'Lista Projetu {status} Tinan {year}', 'legend': f'Lista Projetu {status} Tinan {year}',
	}
	return render(request, 'reportdiv_t/proj_statusp_list.html', context)
#

def rdivProjStatusList(request, pk, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	status = get_object_or_404(StatusPlan, pk=pk2)
	objects = Project.objects.filter(owner=div, status=status).all()
	years = Project.objects.filter(owner=div, status=status).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'status': status, 'objects': objects, 'years': years, 'page': 'pdash',
		'subtitle': subtitle, 'title': f'Lista Projetu {status}', 'legend': f'Lista Projetu {status}',
	}
	return render(request, 'reportdiv_t/proj_status_list.html', context)


def rdivProjStatusYearList(request, pk, pk2, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	status = get_object_or_404(StatusPlan, pk=pk2)
	objects = Project.objects.filter(owner=div, status=status, year__year=year).all()
	years = Project.objects.filter(owner=div, status=status).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'year': year, 'status': status, 'objects': objects, 'years': years, 'page': 'pyear',
		'subtitle': subtitle, 'title': f'Lista Projetu {status} Tinan {year}', 'legend': f'Lista Projetu {status} Tinan {year}',
	}
	return render(request, 'reportdiv_t/proj_status_list.html', context)
### CATEGORY

def rdivPCatList(request, pk, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	pcat = get_object_or_404(PCategory, pk=pk2)
	objects = Project.objects.filter(owner=div, pcategory=pcat).all()
	years = Project.objects.filter(owner=div, pcategory=pcat).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'pcat': pcat, 'objects': objects, 'years': years, 'page': 'pdash',
		'subtitle': subtitle,
		'title': f'Lista Projetu {pcat.name} ({pcat.code})',
		'legend': f'Lista Projetu {pcat.name} ({pcat.code})',
	}
	return render(request, 'reportdiv_t/r_pcat_list.html', context)


def rdivPCatYearList(request, pk, pk2, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	pcat = get_object_or_404(PCategory, pk=pk2)
	objects = Project.objects.filter(owner=div, pcategory=pcat, year__year=year).all()
	years = Project.objects.filter(owner=div, pcategory=pcat).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'year': year, 'pcat': pcat, 'objects': objects, 'years': years, 'page': 'pyear',
		'subtitle': subtitle,
		'title': f'Lista Projetu {pcat.code} Tinan {year}',
		'legend': f'Lista Projetu {pcat.code} Tinan {year}',
	}
	return render(request, 'reportdiv_t/r_pcat_list.html', context)
### CAPITAL

def rdivPCapList(request, pk, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	pcap = get_object_or_404(Capital, pk=pk2)
	objects = Project.objects.filter(owner=div, capital=pcap).all()
	years = Project.objects.filter(owner=div, capital=pcap).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'pcap': pcap, 'objects': objects, 'years': years, 'page': 'pdash',
		'subtitle': subtitle, 'title': f'Lista Projetu {pcap.name} ({pcap.code})', 'legend': f'Lista Projetu {pcap.name} ({pcap.code})',
	}
	return render(request, 'reportdiv_t/r_pcap_list.html', context)


def rdivPCapYearList(request, pk, pk2, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	pcap = get_object_or_404(Capital, pk=pk2)
	objects = Project.objects.filter(owner=div, capital=pcap, year__year=year).all()
	years = Project.objects.filter(owner=div, capital=pcap).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'year': year, 'pcap': pcap, 'objects': objects, 'years': years, 'page': 'pyear',
		'subtitle': subtitle, 'title': f'Lista Projetu {pcap.code} Tinan {year}', 'legend': f'Lista Projetu {pcap.code} Tinan {year}',
	}
	return render(request, 'reportdiv_t/r_pcap_list.html', context)
### SECTOR

def rdivPSecList(request, pk, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	psec = get_object_or_404(Sector, pk=pk2)
	objects = Project.objects.filter(owner=div, sector=psec).all()
	years = Project.objects.filter(owner=div, sector=psec).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'psec': psec, 'objects': objects, 'years': years, 'page': 'pdash',
		'subtitle': subtitle, 'title': f'Lista Projetu {psec}', 'legend': f'Lista Projetu {psec}',
	}
	return render(request, 'reportdiv_t/r_psec_list.html', context)


def rdivPSecYearList(request, pk, pk2, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	psec = get_object_or_404(Sector, pk=pk2)
	objects = Project.objects.filter(owner=div, sector=psec, year__year=year).all()
	years = Project.objects.filter(owner=div, sector=psec).distinct().values('year__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'year': year, 'psec': psec, 'objects': objects, 'years': years, 'page': 'pyear',
		'subtitle': subtitle, 'title': f'Lista Projetu {psec} Tinan {year}', 'legend': f'Lista Projetu {psec} Tinan {year}',
	}
	return render(request, 'reportdiv_t/r_psec_list.html', context)
###

def rdivImpList(request, pk):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = ContractYear.objects.filter(contract__project__owner=div).all()
	tot_sum = ContractYear.objects.filter(contract__project__owner=div).aggregate(Sum('total')).get('total__sum', 0.00)
	years = Contract.objects.filter(project__owner=div).distinct().values('start_date__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'objects': objects, 'tot_sum': tot_sum, 'years': years, 'page': 'pdash',
		'subtitle': subtitle, 'title': f'Lista Projetu Executadu', 'legend': f'Lista Projetu Executadu',
	}
	return render(request, 'reportdiv_t/imp_list.html', context)


def rdivImpYearList(request, pk, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	objects = ContractYear.objects.filter(contract__project__owner=div, year=year).prefetch_related('contract__amendment').all()
	tot_sum = ContractYear.objects.filter(contract__project__owner=div, year=year).aggregate(Sum('total')).get('total__sum', 0.00)
	years = Contract.objects.filter().distinct().values('start_date__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'year': year, 'objects': objects, 'tot_sum': tot_sum, 'years': years, 'page': 'pyear',
		'subtitle': subtitle, 
		'title': f'Lista Projetu Executadu Tinan {year}', 
		'legend': f'Lista Projetu Executadu Tinan {year}',
	}
	return render(request, 'reportdiv_t/imp_list.html', context)
#

def rdivImpStatusList(request, pk, pk2):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	status = get_object_or_404(StatusImp, pk=pk2)
	objects = ContractYear.objects.filter(contract__status=status).all()
	tot_sum = ContractYear.objects.filter(contract__status=status).aggregate(Sum('total')).get('total__sum', 0.00)
	years = Contract.objects.filter(status=status).distinct().values('start_date__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'status': status, 'objects': objects, 'tot_sum': tot_sum, 'years': years, 'page': 'pdash',
		'subtitle': subtitle, 
		'title': f'Lista Projetu Executadu ho status {status}',
		'legend': f'Lista Projetu Executadu ho status {status}',
	}
	return render(request, 'reportdiv_t/imp_status_list.html', context)


def rdivImpStatusYearList(request, pk, pk2, year):
	group = get_roles(request)
	div = get_object_or_404(Division, pk=pk)
	status = get_object_or_404(StatusImp, pk=pk2)
	objects = ContractYear.objects.filter(contract__project__owner=div, contract__status=status, year=year).all()
	tot_sum = ContractYear.objects.filter(contract__project__owner=div, contract__status=status, year=year).aggregate(Sum('total')).get('total__sum', 0.00)
	years = Contract.objects.filter(status=status).distinct().values('start_date__year')
	subtitle = f'{div.name} ({div.code})'
	context = {
		'group': group, 'div': div, 'year': year, 'status': status, 'objects': objects, 'tot_sum': tot_sum, 'years': years, 'page': 'pyear',
		'subtitle': subtitle,
		'title': f'Lista Projetu Executadu ho status {status} Tinan {year}',
		'legend': f'Lista Projetu Executadu ho status {status} Tinan {year}',
	}
	return render(request, 'reportdiv_t/imp_status_list.html', context)
