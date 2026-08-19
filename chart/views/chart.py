import numpy as np
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q, Min, Max
from custom.models import Division, PCategory, Sector, PType
from project.models import Project, ProjectLoc
from contract.models import Contract, ContractComp
from custom.models import StatusPlan, StatusImp

def ChartDash(request):	
	group = request.user.groups.all()[0].name
	years = Project.objects.filter().distinct().values('year__year').all().order_by('-year__year')
	context = {
		'group': group, 'years': years,
		'title': 'Grafiku Jeral', 'legend': 'Grafiku Jeral',
	}
	return render(request, 'chart/dash.html', context)


def ChartDashYear(request, year):	
	group = request.user.groups.all()[0].name
	years = Project.objects.filter().distinct().values('year__year').all().order_by('-year__year')
	context = {
		'group': group, 'year': year, 'years': years,
		'title': f'Grafiku Tinan {year}', 'legend': f'Grafiku Tinan {year}',
	}
	return render(request, 'chart/dash_year.html', context)
###

def divChartDash(request, pk):	
	group = request.user.groups.all()[0].name
	div = get_object_or_404(Division, pk=pk)
	years = Project.objects.filter(owner=div).distinct().values('year__year').all().order_by('-year__year')
	context = {
		'group': group, 'div':div, 'years': years,
		'title': 'Grafiku Jeral', 'legend': 'Grafiku Jeral',
	}
	return render(request, 'chartdiv/dash.html', context)


def divChartDashYear(request, pk, year):	
	group = request.user.groups.all()[0].name
	div = get_object_or_404(Division, pk=pk)
	years = Project.objects.filter(owner=div).distinct().values('year__year').all().order_by('-year__year')
	context = {
		'group': group, 'div':div, 'year':year, 'years':years,
		'title': f'Grafiku Tinan {year}', 'legend': f'Grafiku Tinan {year}',
	}
	return render(request, 'chartdiv/dash_year.html', context)