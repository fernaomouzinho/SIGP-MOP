from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from custom.models import Division
from conf.user_utils import c_user_dg
from users.decorators import allowed_users
from sigp.utils import get_roles


@login_required
def rdgDash(request):
	group = get_roles(request)
	dg = c_user_dg(request.user)
	divs = Division.objects.filter(dg=dg).all()
	context = {
		'group': group, 'divs': divs,
		'title': 'Sumariu Projetu', 'legend': 'Sumariu Projetu',
	}
	return render(request, 'reportdiv/dash_dg.html', context)
### PAY
@login_required
def rdgHome(request):
	group = get_roles(request)
	dg = c_user_dg(request.user)
	divs = Division.objects.filter(dg=dg).all()
	context = {
		'group': group, 'divs': divs, 'page': 'ppay', 'page2':'pg',
		'title': 'Sumariu Pagamentu', 'legend': 'Sumariu Pagamentu',
	}
	return render(request, 'reportdiv/dash_dg.html', context)

@login_required
def rdgAnnHome(request):
	group = get_roles(request)
	dg = c_user_dg(request.user)
	divs = Division.objects.filter(dg=dg).all()
	context = {
		'group': group, 'divs': divs, 'page': 'ppay', 'page2': 'pann',
		'title': 'Sumariu Pagamentu', 'legend': 'Sumariu Pagamentu',
	}
	return render(request, 'reportdiv/dash_dg.html', context)
###