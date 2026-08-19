from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import FileResponse, Http404
from finance.models import CPV, CPVReq, CPVLetter, PO, PRT, EV, FinFiles, POLetter


def CPVReqPDF(request, hashid):
	obj = get_object_or_404(CPVReq, hashed=hashid)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def CPVPDF(request, hashid):
	obj = get_object_or_404(CPV, hashed=hashid)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def CPVLetPDF(request, hashid):
	obj = get_object_or_404(CPVLetter, hashed=hashid)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def POPDF(request, hashid):
	obj = get_object_or_404(PO, hashed=hashid)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def POLetPDF(request, hashid):
	obj = get_object_or_404(POLetter, hashed=hashid)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def PRTPDF(request, hashid):
	obj = get_object_or_404(PRT, hashed=hashid)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def EVPDF(request, hashid):
	obj = get_object_or_404(EV, hashed=hashid)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def FinFilePDF(request, pk):
	obj = get_object_or_404(FinFiles, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')