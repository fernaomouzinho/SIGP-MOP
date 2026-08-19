from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import FileResponse, Http404
from eval.models import EvalFile, EvalLet, EvalLetAdnBack


def EvalFilePDF(request, pk):
	obj = get_object_or_404(EvalFile, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def EvalFilePDFBOQ(request, pk):
	obj = get_object_or_404(EvalFile, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file_boq.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')
 

def EvalFilePDFDesign(request, pk):
	obj = get_object_or_404(EvalFile, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file_design.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')
 

def EvalFilePDFSpec(request, pk):
	obj = get_object_or_404(EvalFile, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file_spec.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')
 

def EvalFilePDFMapQ(request, pk):
	obj = get_object_or_404(EvalFile, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file_mapq.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def EvalFilePDFDocOther(request, pk):
	obj = get_object_or_404(EvalFile, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file_docoth.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def EvalLetPDF(request, hashid):
	obj = get_object_or_404(EvalLet, hashed=hashid)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')

#PDF ADN
def EvalFileAdnPDFRS(request, pk):
	obj = get_object_or_404(EvalLetAdnBack, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def EvalFileAdnPDFBOQ(request, pk):
	obj = get_object_or_404(EvalLetAdnBack, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file_boq.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')
 

def EvalFileAdnPDFDesign(request, pk):
	obj = get_object_or_404(EvalLetAdnBack, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file_design.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')
 

def EvalFileAdnPDFSpec(request, pk):
	obj = get_object_or_404(EvalLetAdnBack, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file_spec.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')
 

def EvalFileAdnPDFMapQ(request, pk):
	obj = get_object_or_404(EvalLetAdnBack, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file_mapq.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def EvalFileAdnPDFDocOther(request, pk):
	obj = get_object_or_404(EvalLetAdnBack, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file_docoth.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')