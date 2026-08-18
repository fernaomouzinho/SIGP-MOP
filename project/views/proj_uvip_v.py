import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from sigp.utils import get_roles
from project.models import Project, ProjectLoc, ProjectEst
from employee.models import EmployeePos, EmployeeUser 


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin','sigp_dna','sigp_op', 'sigp_bd','sigp_bd_eng'])
def uvipProjList(request):
    group = get_roles(request)
    
    if 'sigp_admin' not in group:
        empuser = EmployeeUser.objects.filter(user=request.user.id).first()
        emppos  = EmployeePos.objects.filter(id=empuser.id).first()
    objects = Project.objects.filter().all().order_by("-year",'id')
    years = Project.objects.filter().distinct().values('year__year').all().order_by('year__year')
    if 'sigp_admin' not in group:
        context = {
            'group': group, 'objects': objects, 'years': years,'emppos':emppos,
            'module_name': 'Modulu Projetu', 'title': f'Lista Projetu', 'legend': f'Lista Projetu'
        }
    else:
         context = {
            'group': group, 'objects': objects, 'years': years,
            'module_name': 'Modulu Projetu', 'title': f'Lista Projetu', 'legend': f'Lista Projetu'
        }
    return render(request, 'project_uvip/list.html', context)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin','sigp_op','sigp_bd','sigp_bd_eng'])
def uvipProjDetail(request, hashid):
    group = get_roles(request)

    if 'sigp_admin' not in group:
        empuser = EmployeeUser.objects.filter(user=request.user.id).first()
        emppos  = EmployeePos.objects.filter(id=empuser.id).first()
    proj = get_object_or_404(Project, hashed=hashid)
    loc = ProjectLoc.objects.filter(project=proj).first()
    est = ProjectEst.objects.filter(project=proj).first()
    
    if 'sigp_admin' not in group:
        context = {
            'group': group, 'proj': proj, 'loc': loc, 'est': est, 'page': 'pdet','emppos':emppos,
            'title': 'Detallu Projetu', 'legend': 'Detallu Projetu',
        }
    else:
        context = {
            'group': group, 'proj': proj, 'loc': loc, 'est': est, 'page': 'pdet',
            'title': 'Detallu Projetu', 'legend': 'Detallu Projetu',
        }
    return render(request, 'project_uvip/detail.html', context)


@allowed_users(allowed_roles=['sigp_uivp','sigp_admin','sigp_op','sigp_bd','sigp_bd_eng'])
def uvipProjYear(request, year):
    group = get_roles(request)
    objects = Project.objects.filter(year__year=year).all().order_by("-year","id")
    years = Project.objects.filter().distinct().values('year__year').all().order_by('year__year')
    context = {
        'group': group, 'objects': objects, 'years': years,
        'module_name': 'Modulu Projetu', 'title': f'Lista Projetu Tinan {year}', 'legend': f'Lista Projetu Tinan {year}'
    }
    return render(request, 'project_uvip/list_year.html', context)
#

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin','sigp_op','sigp_bd','sigp_bd_eng'])
def ProjRawData(request):
    group = get_roles(request)
    projs = Project.objects.filter().all().order_by("-year","id")
    objects = []
    for i in projs:
        a = ProjectLoc.objects.filter(project=i).first()
        b = ProjectEst.objects.filter(project=i).first()
        objects.append([i,a,b])
    context = {
        'group': group, 'objects': objects,
        'title': f'Raw Data', 'legend': f'Raw Data'
    }
    return render(request, 'project_uvip/raw_data.html', context)
