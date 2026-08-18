from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Min, Max
from conf.user_utils import c_user_div
from custom.models import PCategory, Sector
from project.models import Project, ProjectLoc
from contract.models import Contract, ContractComp
from users.decorators import allowed_users
from sigp.utils import get_roles

@allowed_users(allowed_roles=['sigp_admin'])
def home(request):
	group = get_roles(request)
	div = []
	if 'sigp_div' in group:
		div = c_user_div(request.user)
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
		p_cats,p_secs = [],[]
		cats = PCategory.objects.filter().all()
		for cat in cats:
			cat_a = Project.objects.filter(owner=div, pcategory=cat).all().count()
			p_cats.append([cat,cat_a])
		secs = Sector.objects.filter().all()
		for sec in secs:
			sec_a = Project.objects.filter(owner=div, sector=sec).all().count()
			p_secs.append([sec,sec_a])
		tot_type = Project.objects.filter(owner=div).distinct().values('ptype').all().count()
		tot_comp = ContractComp.objects.filter(contract__project__owner=div, is_main=True).distinct().values('company').all().count()
		tot_loc = ProjectLoc.objects.filter(project__owner=div).distinct().values('municipality').all().count()
		year_min = Project.objects.filter(owner=div).aggregate(Min('year__year'))
		year_max = Project.objects.filter(owner=div).aggregate(Max('year__year'))
		tot_year = Project.objects.filter(owner=div).all().count()
	else:
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
		p_cats,p_secs = [],[]
		cats = PCategory.objects.filter().all()
		for cat in cats:
			cat_a = Project.objects.filter(pcategory=cat).all().count()
			p_cats.append([cat,cat_a])
		secs = Sector.objects.filter().all()
		for sec in secs:
			sec_a = Project.objects.filter(sector=sec).all().count()
			p_secs.append([sec,sec_a])
		tot_type = Project.objects.filter().distinct().values('ptype').all().count()
		tot_comp = ContractComp.objects.filter(is_main=True).distinct().values('company').all().count()
		tot_loc = ProjectLoc.objects.filter().distinct().values('municipality').all().count()
		year_min = Project.objects.aggregate(Min('year__year'))
		year_max = Project.objects.aggregate(Max('year__year'))
		tot_year = Project.objects.filter().all().count()
	context = {
		'group': group, 't_proj': t_proj, 't_new': t_new, 't_rollover': t_rollover, 't_ongoing': t_ongoing, 't_notstarted': t_notstarted, 't_pending': t_pending, 't_comp': t_comp,
		't_imp': t_imp, 't_onprog': t_onprog, 't_delay': t_delay, 't_abandon': t_abandon, 't_pho': t_pho, 't_fho': t_fho,
		'p_cats': p_cats, 'p_secs': p_secs, 'tot_type': tot_type, 'tot_comp': tot_comp, 'tot_loc': tot_loc,
		'year_min': year_min, 'year_max': year_max, 'tot_year': tot_year, 'div':div,
		'pk1':1, 'pk2':2, 'pk3':3, 'pk4':4, 'pk5':5, 
		'title': 'Dashboard', 'legend': 'Dashboard',
	}
	if 'sigp_div' in group: return render(request, 'home/div_home.html', context)
	else: return render(request, 'home/home.html', context)

def error_404(request, exception):
        data = {}
        return render(request,'home/404.html', data)

def error_500(request):
        data = {}
        return render(request,'home/500.html', data)
