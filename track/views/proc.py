import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from proc.models import Proc, ProcTrack, ProcReqTrack, ProcResTrack
from track.models import ProcJustify
from users.decorators import allowed_users
from sigp.utils import get_roles


def trackProcList(request):
	group = get_roles(request)
	procs = Proc.objects.filter().all().order_by('-date')
	objects = []
	for i in procs:
		req = ProcReqTrack.objects.filter(proc=i).first()
		res = ProcResTrack.objects.filter(proc=i).first()
		percent1,percent2 = 0,0
		if req: 
			if req.percent: percent1 = req.percent
		if res:
			if res.percent: percent2 = res.percent
		objects.append([i,req,percent1,res,percent2])
	context = {
		'group': group, 'objects': objects,
		'title': 'Track Tender', 'legend': 'Track Tender'
	}
	return render(request, 'track/proc_list.html', context)


def trackProcDet(request, hashid):
	group = get_roles(request)
	proc = get_object_or_404(Proc, hashed=hashid)
	track1 = ProcReqTrack.objects.filter(proc=proc).first()
	track2 = ProcResTrack.objects.filter(proc=proc).first()
	track3 = ProcTrack.objects.filter(proc=proc).first()
	today = datetime.date.today()
	percent1,percent2,obj_days1,obj_days2 = 0,0,[],[]
	if track1:
		if track1.percent: percent1 = track1.percent
		if track2.percent: percent2 = track2.percent
		a1,b1,c1,d1,e1 = "","","","",""
		a2,b2,c2,d2,e2 = "","","","",""
		#dna
		if track1.is_start == True and track1.is_dna_out == False: 
			a1 = (today-track1.date_start).days
		elif track1.is_dna_out == True:
			a1 = (track1.date_dna_out-track1.date_start).days
		#dgaf
		if track1.is_dna_out == True and track1.is_dgaf_in_1 == False: 
			b1 = (today-track1.date_dna_out).days
		elif track1.is_dgaf_in_1 == True and track1.is_dgaf_out_1 == False:
			b1 = (today-track1.date_dgaf_in_1).days
		elif track1.is_dgaf_out_1 == True:
			b1 = (track1.date_dgaf_out_1-track1.date_dgaf_in_1).days
		#gab
		if track1.is_dgaf_out_1 == True and track1.is_gab_in == False: 
			c1 = (today-track1.date_dgaf_out_1).days
		elif track1.is_gab_in == True and track1.is_gab_out == False:
			c1 = (today-track1.date_gab_in).days
		elif track1.is_gab_out == True:
			c1 = (track1.date_gab_out-track1.date_gab_in).days
		#dgaf
		if track1.is_gab_out == True and track1.is_dgaf_in_2 == False: 
			d1 = (today-track1.date_gab_out).days
		elif track1.is_dgaf_in_2 == True and track1.is_dgaf_out_2 == False:
			d1 = (today-track1.date_dgaf_in_2).days
		elif track1.is_dgaf_out_2 == True:
			d1 = (track1.date_dgaf_out_2-track1.date_dgaf_in_2).days
		#dna
		if track1.is_dgaf_out_2 == True and track1.is_dna_in == False: 
			e1 = (today-track1.date_dgaf_out_2).days
		elif track1.is_dna_in == True and track1.is_end == False:
			e1 = (today-track1.date_dna_in).days
		elif track1.is_end == True:
			e1 = (track1.date_end-track1.date_dna_in).days
		obj_days1.append([a1,b1,c1,d1,e1])
		### RES
		#dna
		if track2.is_start == True and track2.is_dna_out == False: 
			a2 = (today-track2.date_start).days
		elif track2.is_dna_out == True:
			a2 = (track2.date_dna_out-track2.date_start).days
		#dgaf
		if track2.is_dna_out == True and track2.is_dgaf_in_1 == False: 
			b2 = (today-track2.date_dna_out).days
		elif track2.is_dgaf_in_1 == True and track2.is_dgaf_out_1 == False:
			b2 = (today-track2.date_dgaf_in_1).days
		elif track2.is_dgaf_out_1 == True:
			b2 = (track2.date_dgaf_out_1-track2.date_dgaf_in_1).days
		#gab
		if track2.is_dgaf_out_1 == True and track2.is_gab_in == False: 
			c2 = (today-track2.date_dgaf_out_1).days
		elif track2.is_gab_in == True and track2.is_gab_out == False:
			c2 = (today-track2.date_gab_in).days
		elif track2.is_gab_out == True:
			c2 = (track2.date_gab_out-track2.date_gab_in).days
		#dgaf
		if track2.is_gab_out == True and track2.is_dgaf_in_2 == False: 
			d2 = (today-track2.date_gab_out).days
		elif track2.is_dgaf_in_2 == True and track2.is_dgaf_out_2 == False:
			d2 = (today-track2.date_dgaf_in_2).days
		elif track2.is_dgaf_out_2 == True:
			d2 = (track2.date_dgaf_out_2-track2.date_dgaf_in_2).days
		#dna
		if track2.is_dgaf_out_2 == True and track2.is_dna_in == False: 
			e2 = (today-track2.date_dgaf_out_2).days
		elif track2.is_dna_in == True and track2.is_end == False:
			e2 = (today-track2.date_dna_in).days
		elif track2.is_end == True:
			e2 = (track2.date_end-track2.date_dna_in).days
		obj_days2.append([a2,b2,c2,d2,e2])
	justs = ProcJustify.objects.filter(proc=proc).all()
	context = {
		'group':group, 'proj':proc.proj, 'proc':proc, 'track1':track1, 'track2':track2, 
		'track3':track3, 'percent1':percent1, 'percent2':percent2,
		'obj_days1':obj_days1,'obj_days2':obj_days2, 'justs':justs,
		'title': 'Track Tender', 'legend': 'Track Tender'
	}
	return render(request, 'track/proc_det.html', context)
###