from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from project.models import ProjectEst
from eval.models import Eval, EvalFile, EvalLet, EvalTrack, EvalFITrack, EvalLetAdnBack, EvalLetCNABack
from conf.user_utils import c_user_div, c_user_dna, c_user_dnof
from ver.models import Ver
from users.decorators import allowed_users
from sigp.utils import get_roles

### DIV

@allowed_users(allowed_roles=['sigp_div','sigp_dna','sigp_dnof'])
def divEvalList(request):
    group = get_roles(request)
    div = c_user_div(request.user)
    objects = Eval.objects.filter(div=div).all().order_by("-date")
    context = {
        'group':group, 'objects':objects,
        'module': 'Lista Avaliasaun ToR', 'title': 'Lista Avaliasaun ToR', 'legend': 'Lista ToR'
    }
    return render(request, 'eval_div/list.html', context)

@allowed_users(allowed_roles=['sigp_div','sigp_dna','sigp_dnof'])
def divEvalDetail(request, hashid):
    group = get_roles(request)
    if 'sigp_div' in group: div = c_user_div(request.user)
    elif 'sigp_dna' in group: div = c_user_dna(request.user)
    elif 'sigp_dnof' in group: div = c_user_dnof(request.user)
    eval = get_object_or_404(Eval, hashed=hashid)
    projest = ProjectEst.objects.filter(project=eval.proj).first()
    track = EvalTrack.objects.filter(eval=eval).first()
    files = EvalFile.objects.filter(eval=eval).all()
    context = {
        'group':group, 'eval':eval, 'projest':projest, 'track':track, 'files':files,
        'module': 'Formulariu Pedidu ba Avaliasaun ToR', 'title': 'Detallu Avaliasaun ToR', 'legend': 'Detallu Avaliasaun ToR',
    }
    return render(request, 'eval_div/detail.html', context)
### UIVP
@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalList(request):
    group = get_roles(request)
    objects = Eval.objects.filter().all().order_by("-date")
    context = {
        'group':group, 'objects':objects,
        'module': 'Avaliasaun ToR', 'title': 'Lista Avaliasaun', 'legend': 'Lista Avaliasaun'
    }
    return render(request, 'eval_uvip/list.html', context)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalList2(request, hashid):
    group = get_roles(request)
    eval = get_object_or_404(Eval, hashed=hashid)
    proj = eval.proj
    projest = ProjectEst.objects.filter(project=proj).first()
    track = EvalTrack.objects.filter(eval=eval).first()
    trackfi = EvalFITrack.objects.filter(eval=eval).first()
    files = EvalFile.objects.filter(eval=eval).all()
    lets = EvalLet.objects.filter(eval=eval).all()
    let = EvalLet.objects.filter(eval=eval).last()
    letadn =EvalLetAdnBack.objects.filter(evallet=let)
    objects = Ver.objects.all()
    context = {
        'group':group, 'eval':eval, 'proj':proj, 'projest':projest, 'track':track, 'files':files,'let':let,'letadn':letadn,
        'lets':lets, 'trackfi':trackfi, 'p1':1, 'p2':2, 'p3':3, 'objects':objects,
        'module': 'Avaliasaun ToR', 'title': 'Detallu Avaliasaun', 'legend': 'Detallu Avaliasaun', 'legend2': 'Lista Despaxu ba Sekasaun',
    }
    return render(request, 'eval_uvip/list_2.html', context)

@allowed_users(allowed_roles=['sigp_uivp','sigp_admin'])
def uvipEvalDetail(request, hashid):
    group = get_roles(request)
    eval = get_object_or_404(Eval, hashed=hashid)
    proj = eval.proj
    projest = ProjectEst.objects.filter(project=proj).first()
    track = EvalTrack.objects.filter(eval=eval).first()
    trackfi = EvalFITrack.objects.filter(eval=eval).first()
    files = EvalFile.objects.filter(eval=eval).all()
    lets = EvalLet.objects.filter(eval=eval).all()
    let = EvalLet.objects.filter(eval=eval).last()
    letadn =EvalLetAdnBack.objects.all()
    la=[]
    for a in letadn:
        b = a.evallet.pk
        la.append(b)
    ladn = la
    vers = Ver.objects.filter(eval=eval).last()
    vers_1 = Ver.objects.filter(eval=eval).all()
    context = {
        'group':group, 'eval':eval, 'vers':vers, 'vers_1':vers_1,'proj':proj, 'projest':projest, 'track':track, 'files':files,
        'let':let,'letadn':letadn, 'ladn':ladn,
        'lets':lets, 'trackfi':trackfi, 'p1':1, 'p2':2, 'p3':3,
        'module': 'Avaliasaun ToR', 'title': 'Detallu Avaliasaun', 'legend': 'Detallu Avaliasaun',
    }
    return render(request, 'eval_uvip/detail.html', context)
### Gab
@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalList(request):
    group = get_roles(request)
    objects = Eval.objects.filter().all().order_by("-date")
    context = {
        'group':group, 'objects':objects,
        'module': 'Avaliasaun ToR', 'title': 'Lista Avaliasaun', 'legend': 'Lista Avaliasaun'
    }
    return render(request, 'eval_gab/list.html', context)

@allowed_users(allowed_roles=['sigp_gabm','sigp_admin'])
def gabEvalDetail(request, hashid):
    group = get_roles(request)
    eval = get_object_or_404(Eval, hashed=hashid)
    proj = eval.proj
    fi = proj.pcategory.id
    projest = ProjectEst.objects.filter(project=proj).first()
    track = EvalTrack.objects.filter(eval=eval).first()
    trackfi = EvalFITrack.objects.filter(eval=eval).first()
    files = EvalFile.objects.filter(eval=eval).all()
    lets = EvalLet.objects.filter(eval=eval).all()
    let = EvalLet.objects.filter(eval=eval).last()
    letadn =EvalLetAdnBack.objects.all()
    letcna =EvalLetCNABack.objects.filter(evallet=let).last()
    print(letcna)
    la=[]
    for a in letadn:
        b = a.evallet.pk
        la.append(b)
    ladn = la
    context = {
        'group':group, 'eval':eval, 'proj':proj, 'fi':fi, 'projest':projest, 'track':track, 'files':files,
        'let':let,'letadn':letadn, 'ladn':ladn, 'letcna':letcna,
        'lets':lets, 'trackfi':trackfi,
        'module': 'Avaliasaun ToR', 'title': 'Detallu Avaliasaun', 'legend': 'Detallu Avaliasaun',
    }
    return render(request, 'eval_gab/detail.html', context)

### DNA
@allowed_users(allowed_roles=['sigp_admin','sigp_dna'])
def dnaEvalList(request):
    group = get_roles(request)
    objects = Eval.objects.filter(is_end=True).all().order_by("-date")
    context = {
        'group':group, 'objects':objects,
        'module': 'Avaliasaun ToR', 'title': 'Lista Avaliasaun', 'legend': 'Lista Avaliasaun'
    }
    return render(request, 'eval_dna/list.html', context)

@allowed_users(allowed_roles=['sigp_admin','sigp_dna'])
def dnaEvalDetail(request, hashid):
    group = get_roles(request)
    eval = get_object_or_404(Eval, hashed=hashid)
    proj = eval.proj
    projest = ProjectEst.objects.filter(project=proj).first()
    files = EvalFile.objects.filter(eval=eval).all()
    lets = EvalLet.objects.filter(eval=eval).all()
    context = {
        'group':group, 'eval':eval, 'proj':proj, 'projest':projest, 'files':files,
        'lets':lets, 
        'module': 'Avaliasaun ToR', 'title': 'Detallu Avaliasaun', 'legend': 'Detallu Avaliasaun',
    }
    return render(request, 'eval_dna/detail.html', context)