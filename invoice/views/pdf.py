from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import FileResponse, Http404
from invoice.models import Invoice, CertPay, PayRecom, InvLet
from users.decorators import allowed_users
from sigp.utils import get_roles


@allowed_users(allowed_roles=['sigp_dgaf', 'sigp_admin'])
def InvPDF(request, hashid):
	group = get_roles(request)
	objects = get_object_or_404(Invoice, hashed=hashid)
	file = str(settings.BASE_DIR)+str(objects.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


@allowed_users(allowed_roles=['sigp_dgaf', 'sigp_admin'])
def CertPDF(request, hashid):
	group = get_roles(request)
	objects = get_object_or_404(CertPay, hashed=hashid)
	file = str(settings.BASE_DIR)+str(objects.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


@allowed_users(allowed_roles=['sigp_dgaf', 'sigp_admin'])
def RecomPDF(request, hashid):
	group = get_roles(request)
	obj = get_object_or_404(PayRecom, hashed=hashid)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


@allowed_users(allowed_roles=['sigp_dgaf', 'sigp_admin'])
def InvLetPDF(request, hashid):
	group = get_roles(request)
	obj = get_object_or_404(InvLet, hashed=hashid)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')
