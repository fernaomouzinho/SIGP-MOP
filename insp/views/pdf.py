from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import FileResponse, Http404
from insp.models import Insp, InspSecEng


def InspPDF(request, pk):
	obj = get_object_or_404(Insp, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def InspSecPDF(request, pk):
	obj = get_object_or_404(InspSecEng, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def InspSecPDF2(request, pk):
	obj = get_object_or_404(InspSecEng, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file2.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')


def InspSecPDF3(request, pk):
	obj = get_object_or_404(InspSecEng, pk=pk)
	file = str(settings.BASE_DIR)+str(obj.file3.url)
	try:
		if file: return FileResponse(open(file, 'rb'), content_type='application/pdf')
		else: return FileResponse(open(file, 'rb'))
	except FileNotFoundError: raise Http404('not found')
