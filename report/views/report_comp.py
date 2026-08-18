import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.db.models import Sum
from contract.models import Contract, Amendment, ContractComp
from payment.models import Payment
from contract.models import Amendment, ContractComp
from custom.models import StatusPlan
from company.models import Company
from conf.utils import date_dist
from users.decorators import allowed_users
from sigp.utils import get_roles


@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rCompProjSum(request):
    group = get_roles(request)
    statuss = StatusPlan.objects.all()
    today = datetime.date.today()
    thisyear = today.year
    lastyear = thisyear-1
    years = [thisyear,lastyear]
    comps = ContractComp.objects.exclude(company__isnull=True).distinct().values('company').all()
    objects,objects2 = [],[]
    for i in comps:
        comp = Company.objects.filter(id=i['company']).first()
        tot_i_a = Contract.objects.filter(contractcomp__company=comp).all().count()
        obj1_1,obj1_2 = [],[]
        for ii in statuss:
            tot_ii_a = Contract.objects.filter(contractcomp__company=comp, project__status=ii).all().count()
            obj1_1.append([ii,tot_ii_a])
          
        for ij in years:
            ij_a = Contract.objects.filter(contractcomp__company=comp, start_date__year=ij).all().count()
            obj1_2.append([ij,ij_a])
        objects.append([comp,tot_i_a,obj1_1])   
        objects2.append([comp,obj1_2])
    
    context = {
        'group': group, 'statuss': statuss, 'years': years, 'objects': objects, 'objects2': objects2,
        'title': 'Sumariu Projetu Baseia Compania', 'legend': 'Sumariu Projetu Baseia Compania'
    }
    return render(request, 'report_comp/proj_sum.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rCompProjList(request, pk):
    group = get_roles(request)
    comp = get_object_or_404(Company, pk=pk)
    conts = Contract.objects.filter(contractcomp__company=comp).all()
    objects = []
    for i in conts:
        amend = Amendment.objects.get(contract=i)
        pay = Payment.objects.filter(contract=i).last()
        objects.append([i,amend,pay])
    tot_cont = Amendment.objects.filter(contract__contractcomp__company=comp).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
    if tot_cont: tot_cont
    else: tot_cont = 0
    subtitle = f'Compania {comp}'
    context = {
        'group': group, 'comp': comp, 'objects': objects, 'tot_cont': tot_cont,
        'subtitle': subtitle, 'title': 'Lista Projetu', 'legend': 'Lista Projetu'
    }
    return render(request, 'report_comp/proj_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rCompProjStatusList(request, pk, pk2):
    group = get_roles(request)
    comp = get_object_or_404(Company, pk=pk)
    status = get_object_or_404(StatusPlan, pk=pk2)
    conts = Contract.objects.filter(contractcomp__company=comp, project__status=status).all()
    objects = []
    for i in conts:
        amend = Amendment.objects.get(contract=i)
        pay = Payment.objects.filter(contract=i).last()
        objects.append([i,amend,pay])
    tot_cont = Amendment.objects.filter(contract__contractcomp__company=comp, contract__project__status=status).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
    if tot_cont: tot_cont
    else: tot_cont = 0
    subtitle = f'Compania {comp}'
    context = {
        'group': group, 'comp': comp, 'objects': objects, 'tot_cont': tot_cont,
        'subtitle': subtitle, 'title': f'Lista Projetu {status}',
        'legend': f'Lista Projetu {status}'
    }
    return render(request, 'report_comp/proj_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rCompProjYearList(request, pk, year):
    group = get_roles(request)
    comp = get_object_or_404(Company, pk=pk)
    conts = Contract.objects.filter(contractcomp__company=comp, start_date__year=year).all()
    objects = []
    for i in conts:
        amend = Amendment.objects.get(contract=i)
        pay = Payment.objects.filter(contract=i).last()
        objects.append([i,amend,pay])
    tot_cont = Amendment.objects.filter(contract__contractcomp__company=comp, contract__start_date__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
    if tot_cont: tot_cont
    else: tot_cont = 0
    subtitle = f'Compania {comp}'
    context = {
        'group': group, 'year': year, 'comp': comp, 'objects': objects, 'tot_cont': tot_cont, 'page': 'pyear',
        'subtitle': subtitle, 'title': f'Lista Projetu Tinan {year}',
        'legend': f'Lista Projetu Tinan {year}'
    }
    return render(request, 'report_comp/proj_list.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rCompSearch(request):
    group = get_roles(request)
    statuss = StatusPlan.objects.all()
    queryset_list = Company.objects.filter().all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(name__icontains=query).distinct()
    else:
        queryset_list = Company.objects.none()
    objects = []
    for i in queryset_list:
        tot_i_a = Contract.objects.filter(contractcomp__company=i).all().count()
        obj1_1 = []
        for ii in statuss:
            tot_ii_a = Contract.objects.filter(contractcomp__company=i, project__status=ii).all().count()
            obj1_1.append([ii,tot_ii_a])
        objects.append([i,tot_i_a,obj1_1])
    tot = queryset_list.count()
    if not query: query = ""
    context = {
        'group': group, 'statuss': statuss, 'objects': objects, 'tot': tot, 'query': query,
        'title': f'Lista Compania', 'legend': f'Lista Compania'
    }
    return render(request, 'report_comp/search.html', context)
#
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_dnof','sigp_dnof_s','sigp_dgaf','sigp_dgaf_s','sigp_dg','sigp_min','sigp_min_s','sigp_vice','sigp_vice_s','sigp_op','sigp_gabm','sigp_uivp'])
def rContLimitList(request):
    group = get_roles(request)
    today = datetime.date.today()
    thisyear = today.year
    conts = Contract.objects.filter().exclude(status_id=5).all()
    objects = []
    for i in conts:
        a = i.start_date.year
        b = thisyear - a
        c = (today-i.start_date).days
        amend = Amendment.objects.get(contract=i)
        pay = Payment.objects.filter(contract=i).last()
        if b > 2:
            objects.append([i,amend,pay,b,c])
    context = {
        'group': group, 'objects': objects, 'page': 'pdash',
        'title': f'Lista Projetu Liu Tinan 2', 'legend': f'Lista Projetu Liu Tinan 2',
    }
    return render(request, 'report_comp/cont_limit_list.html', context)
