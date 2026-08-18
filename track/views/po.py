import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from finance.models import PO, POTrack
from track.models import POJustify
from users.decorators import allowed_users
from sigp.utils import get_roles


@login_required
def trackPOList(request):
	group = get_roles(request)
	objs = PO.objects.filter(cont__project__is_end=False).all().order_by('id')
	objects = []
	for i in objs:
		track = POTrack.objects.filter(po=i).first()
		objects.append([i,track])
	context = {
		'group': group, 'objects': objects,
		'title': 'Track PO', 'legend': 'Track PO'
	}
	return render(request, 'track/po_list.html', context)

@login_required
def trackPODet(request, hashid):
	group = get_roles(request)
	po = get_object_or_404(PO, hashed=hashid)
	cont = po.cont
	proj = cont.project
	track = POTrack.objects.filter(po=po).first()
	today = datetime.date.today()
	percent,obj_days = 0,[]
	percent = 0
	if track:
		if track.percent: percent = track.percent
		a,b,c,d = 0,0,0,0
		if track.is_dna_out == True and track.is_dgaf_in == False: 
			a = (today-track.date_dna_out).days
		elif track.is_dgaf_in == True and track.is_appr == False: 
			a = (track.date_dgaf_in-track.date_dna_out).days
		elif track.is_appr == True and track.is_dgaf_out == False: 
			a = (track.date_appr-track.date_dgaf_in).days
		elif track.is_dgaf_out == True: 
			a = (track.date_dgaf_out-track.date_dgaf_in).days
		if track.is_dgaf_out == True and track.is_dna_in == False: 
			b = (today-track.date_dgaf_out).days
		elif track.is_dna_in == True and track.is_end == False:
			b = (track.date_dna_in-track.date_dgaf_out).days
		elif track.is_end == True:
			b = (track.date_end-track.date_dna_in).days
		total = a+b+c+d
		obj_days.append([a,b,c,d,total])
	justs = POJustify.objects.filter(po=po).all()
	context = {
		'group':group, 'proj':proj, 'po':po, 'track':track, 'percent':percent,
		'obj_days': obj_days, 'justs': justs,
		'title': 'Track PO', 'legend': 'Track PO'
	}
	return render(request, 'track/po_det.html', context)