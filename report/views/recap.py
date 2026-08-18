import numpy as np
import datetime
from django.shortcuts import render
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from conf.decorators import allowed_users
from django.db.models import Sum
from itertools import chain
from django.db.models.functions import Coalesce
from decimal import Decimal
from django.contrib.humanize.templatetags.humanize import intcomma
from project.models import Project, ProjectEst
from contract.models import Contract, ContractYear, ContractComp,Amendment
from payment.models import Payment, PaymentFiscal,PaymentPortal
from proc.models import Proc,ProcReqTrack
from custom.models import PCat, PCategory, StatusImp,StatusPlan, Capital, Division, Year, DG, Program
from invoice.models import Invoice, CertPay,PayRecom,InvTrack,InvLetAdnBack
from finance.models import TPO
from report.utils_recap import rRecapPortalPay, rRecapVericationADN, rRecapVericationINT,rRecapVericationADNINT, rRecapInspectionADN, rRecapInspectionINT, rRecapInspectionADNINT, rRecapCompImpProj
from eval.models import Eval,EvalTrack,EvalFITrack,EvalLetAdnBack,EvalLetCNABack
from ver.models import Ver, VerSecEng, VerTracks
from insp.models import Insp, InspTracks
from company.models import Company
from datetime import date
current_year = date.today().year
from users.decorators import allowed_users
from sigp.utils import get_roles

# @login_required
# @allowed_users(allowed_roles=['admin','dna','uivp','dnof','gab','dgaf','min','op','gab','uivp'])
# def rRecapDash(request):
#     group = request.user.groups.all()[0].name
#     objects = []
#     capi = Capital.objects.filter().all()
#     a,b,c,d,e,f,g,h,i,j = 0,0,0,0,0,0,0,0,0,0
#     date = datetime.date.today()

#     for cap in capi:
#         a = Project.objects.filter(capital=cap, statusproj_id=2).all().count()
#         b = Project.objects.filter(capital=cap, statusproj_id=1).all().count()
#         c = a+b
#         d = Contract.objects.filter(project__capital=cap).all().exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)

#         e = Payment.objects.filter(contract__project__capital=cap).all().exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
#         i = PaymentFiscal.objects.filter(contract__project__capital=cap).all().exclude(com_amount=0).aggregate(Sum('com_amount')).get('com_amount',0.00)

#         if e != None:
#             if i != None:
#                 j = float(e)+float(i)

#         if d != None:
#             if e:
#                 val = 100*(e/d)
#                 f = round((val),2)
#                 g = round((float(d)-float(j)),2)
#                 h = round((float(g)/float(d))*100,2)
#             objects.append([cap.code.lower,cap,c,d,j,f,g,h])

#     objects2 = []
#     if objects: objects2 = np.array(objects)
#     tota = Project.objects.filter(statusproj_id=2).all().count()
#     totb = Project.objects.filter(statusproj_id=1).all().count()
#     totc = tota+totb

#     totd=sum(filter(None, objects2[:,3]))
#     tote=round(sum(filter(None, objects2[:,4])),2)
#     totf=sum(filter(None, objects2[:,5]))
#     totg=sum(filter(None, objects2[:,6]))
#     toth=round(sum(filter(None, objects2[:,7])),2)
#     obj_tot = [totc,totd,tote,totf,totg,toth]

#     years = Project.objects.distinct().values('year__year').all().order_by('-year__year')
#     context = {
#         'group': group, 'years': years, 'objects':objects, 'obj_tot':obj_tot,
#         'title': 'Rekapitulasaun', 'legend': 'Rekapitulasaun'
#     }
#     return render(request, 'report_recap/dash.html', context)


@login_required
@allowed_users(allowed_roles=['sigp_admin', 'sigp_dna', 'sigp_uivp', 'sigp_dnof', 'sigp_gabm', 'sigp_dgaf', 'sigp_min', 'sigp_op'])
def rRecapDash(request):
    group = get_roles(request)

    # Get data from helper function
    objects, obj_tot = rRecapPortalPay(PCategory)
    objects_1, objects_1_tot = rRecapVericationADN(PCategory)
    objects_2,objects_2_tot = rRecapVericationINT(Capital)
    objects_22,objects_22_tot = rRecapVericationADNINT(Capital)
    objects_3, objects_3_tot = rRecapInspectionADN(PCategory)
    objects_4, objects_4_tot = rRecapInspectionINT(Capital)
    objects_44, objects_44_tot = rRecapInspectionADNINT(Capital)
    objects_5, objects_6 = rRecapCompImpProj(ContractComp)
    
    statuss = StatusPlan.objects.all()
    today = datetime.date.today()
    thisyear = today.year
    lastyear = thisyear-1
    year2 = [thisyear,lastyear]

    years = Project.objects.values('year__year').distinct().order_by('-year__year')

    context = {
        'group': group,
        'years': years,
        'objects': objects,
        'obj_tot': obj_tot,
        'objects_1': objects_1,
        'objects_1_tot':objects_1_tot,
        'objects_2': objects_2,
        'objects_2_tot':objects_2_tot,
        'objects_22': objects_22,
        'objects_22_tot':objects_22_tot,
        'objects_3': objects_3,
        'objects_3_tot':objects_3_tot,
        'objects_4': objects_4,
        'objects_4_tot':objects_4_tot,
        'objects_44': objects_44,
        'objects_44_tot':objects_44_tot,
        'objects_5': objects_5,
        'objects_6': objects_6,
        'statuss': statuss,
        'year2': year2,
        'title': 'Rekapitulasaun',
        'legend': 'Rekapitulasaun'
    }
    return render(request, 'report_recap/dash.html', context)

@login_required   
@allowed_users(allowed_roles=['sigp_admin', 'sigp_dna', 'sigp_uivp', 'sigp_dnof', 'sigp_gab', 'sigp_dgaf', 'sigp_min', 'sigp_op'])   
def rRecapVerProjList1(request, pcat, stage):
    objects = []
    evaltrack =[]
    if pcat == 'cd':
        if stage == 'a':
            objects = ProjectEst.objects.filter(project__capital__code='CD', project__book_id__in=[2,3], project__statusproj_id=1, project__is_adn='True').all().order_by('-project__id')
        elif stage == 'b':
            objects = ProjectEst.objects.filter(project__capital__code='CD', project__book_id__in=[6], project__statusproj_id=1, project__is_adn='True').all().order_by('-project__id')
        elif stage == 'c':
            objects = ProjectEst.objects.filter(project__capital__code='CD', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True').all().order_by('-project__id')
        elif stage == 'd':
            # Submisaun Dokumentu ba UIVP   
            objects = VerTracks.objects.filter(ver__eval__proj__capital__code='CD', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', is_start='True').all().order_by('ver__eval__proj__id')   
        elif stage == 'e':
            # Total Dokumentus Nebe Sei Iha Prosesu Verifikasaun UIVP
            objects = VerTracks.objects.filter(ver__eval__proj__capital__code='CD', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', is_start='True', is_end='False').all().order_by('ver__eval__proj__id')   
        elif stage == 'f':
            # Total Dokumentus Devolve Husi UIVP
            objects = VerSecEng.objects.filter(ver__eval__proj__capital__code='CD',  ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', ver__is_end='False', is_end='False', is_eng_back='True', is_eng_read='True', status='DEVOLVE').all().order_by('ver__eval__proj__id')
            vertrack = VerTracks.objects.filter(ver__eval__proj__capital__code='CD', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', is_start='True', is_end ='False').all().order_by('ver__eval__proj__id')  
        elif stage == 'g':   
            # Total Dokumentu Pasa iha Verifikasaun UIVP
            objects = VerTracks.objects.filter(ver__eval__proj__capital__code='CD', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', ver__is_end=True,is_start='True',is_end ='True').all().order_by('ver__eval__proj__id')
        elif stage == 'h':
            # Submisaun Dokumentu ba ADN
            lm_start = EvalTrack.objects.filter(eval__proj__capital_id=3,eval__proj__pcategory__code='LM',eval__proj__book_id__in=[2,3,6],eval__proj__statusproj_id=1,eval__proj__is_adn='True',is_ver_start='True').order_by('-eval__proj__id')
            fi_start = EvalFITrack.objects.filter(eval__proj__capital_id=3,eval__proj__pcategory__code='FI',eval__proj__book_id__in=[2,3,6],eval__proj__statusproj_id=1,eval__proj__is_adn='True',is_uvip_out_1='True').order_by('-eval__proj__id')
            objects = sorted(chain(lm_start, fi_start),key=lambda x: x.eval.proj.id,reverse=True)
        elif stage == 'i':
            # Projetu ne'ebe iha prosesu verifikaun ADN
            lm_start = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__is_adn='True', is_adn_in="False").order_by('-eval__proj__id')
            fi_start = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_uvip_in_2='False').all().order_by('-eval__proj__id')
            objects = sorted(chain(lm_start, fi_start),key=lambda x: x.eval.proj.id,reverse=True)
        elif stage == 'j':  
            # Devolve Husi ADN
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result="False", is_return="True").order_by('-evallet__eval__proj__id')
            evaltracklm  = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
            evaltrackfi  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
            evaltrack  = sorted(chain(evaltracklm, evaltrackfi),key=lambda x: x.eval.proj.id,reverse=True)
        elif stage == 'k':  
            # Devolve Husi ADN
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result="True", is_return="False").order_by('-evallet__eval__proj__id')
            evaltracklm  = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
            evaltrackfi  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
            evaltrack  = sorted(chain(evaltracklm, evaltrackfi),key=lambda x: x.eval.proj.id,reverse=True)
        
        elif stage == 'k1':  
            # Submit ba UIVP
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result="True", is_return="False").order_by('-evallet__eval__proj__id')
            evaltracklm  = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_adn_in='True').all().order_by('-eval__proj__id')
            evaltrackfi  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_uvip_in_2='True').all().order_by('-eval__proj__id')
            evaltrack  = sorted(chain(evaltracklm, evaltrackfi),key=lambda x: x.eval.proj.id,reverse=True)
            
        elif stage == 'k2':  
            # Submit ba UIVP
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result="True", is_return="False").order_by('-evallet__eval__proj__id')
            evaltracklm  = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_adn_in='True', eval__proj__projectest__adn__gt=0).all().order_by('-eval__proj__id')
            evaltrackfi  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_uvip_in_2='True', eval__proj__projectest__adn__gt=0).all().order_by('-eval__proj__id')
            evaltrack  = sorted(chain(evaltracklm, evaltrackfi),key=lambda x: x.eval.proj.id,reverse=True)
            objects1 = ProjectEst.objects.filter().all()
            
        elif stage == 'k3':  
            # Submit ba UIVP
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result="True", is_return="False").order_by('-evallet__eval__proj__id')
            evaltracklm  = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_gab_in='True', eval__proj__projectest__adn__gt=0).all().order_by('-eval__proj__id')
            evaltrackfi  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_gab_in_1='True', eval__proj__projectest__adn__gt=0).all().order_by('-eval__proj__id')
            evaltrack  = sorted(chain(evaltracklm, evaltrackfi),key=lambda x: x.eval.proj.id,reverse=True)
            objects1 = ProjectEst.objects.filter().all()
            
        elif stage == 'k4':  
            # Submit ba UIVP
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result="True", is_return="False").order_by('-evallet__eval__proj__id')
            evaltracklm  = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_appr='True', eval__proj__projectest__adn__gt=0).all().order_by('-eval__proj__id')
            evaltrackfi  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_appr='True', eval__proj__projectest__adn__gt=0).all().order_by('-eval__proj__id')
            evaltrack  = sorted(chain(evaltracklm, evaltrackfi),key=lambda x: x.eval.proj.id,reverse=True)
            objects1 = ProjectEst.objects.filter().all()
        
        elif stage == 'l':
            # Dokumentu Ba SGP
             objects =EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_appr='True', is_gab_out_1='True').all().order_by('-eval__proj__id')
        elif stage == 'm':
            # Dokumentu ba CNA
            objects =EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_appr='True',is_gab_out_3='True').all().order_by('-eval__proj__id') 
        elif stage == 'n':
            # Dokumentu Prosesa Husi CNA
            objects =EvalFITrack.objects.filter(evallet__eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', eval__is_end='False', is_end='False', is_appr='True', is_gab_out_3='True', is_gab_in_4='True').all().order_by('-eval__proj__id') 
        elif stage == 'o':
            # Dokumentu Devolve Husi CNA
            objects =EvalLetCNABack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='False',is_return='True').all().order_by('evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
        elif stage == 'p':
            # Rezultadu Dokumentu Husi CNA
            objects = EvalLetCNABack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='True',is_return='False').all().order_by('evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
        
        elif stage == 'p1':
            # Submete ba Gabinete Ministro
            objects = EvalLetCNABack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='True',is_return='False').all().order_by('evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
        
        elif stage == 'p2':
            # Gabinete Ministro Aprova
            objects = EvalLetCNABack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='True',is_return='False').all().order_by('evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
        
        elif stage == 'p3':
            # UIVP Implementa
            objects = EvalLetCNABack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='True',is_return='False').all().order_by('evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
        
        elif stage == 'q':
            # Dokumentu Ba DNA
            objects =Proc.objects.filter(proj__capital__code='CD', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='True', is_lock="True" ).all().order_by('-proj__id')
        elif stage == 'r':
            # Rekizasaun Dokumentu Iha DNA
            objects =Proc.objects.filter(proj__capital__code='CD', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='True', is_req_start="True", is_req_end='False').all().order_by('-proj__id')
        elif stage == 's':
            # Dokumentu ho Rezultadu Iha DNA
            objects =Proc.objects.filter(proj__capital__code='CD', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='True', is_res_start="True", is_res_end='True').all().order_by('-proj__id')
        elif stage == 't':
            # Dokumentu ba kontraktu
            objects =Contract.objects.filter(project__capital__code='CD', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True', status_id="7", is_complete='False').all().order_by('-project__id')   
                 
        elif stage == 'u':
            # MOntante ba kontraktu as liu
            objects =Contract.objects.filter(project__capital__code='CD', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True', status_id="7", total__lt=500000).all().order_by('-project__id')   
        
        elif stage == 'v':
            # MOntante ba kontraktu menos ou hanesan
            objects =Contract.objects.filter(project__capital__code='CD', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True', status_id="7", total__gte=500000).all().order_by('-project__id')   
                  
                 
    if pcat == 'lm':
        if stage == 'a':
            objects = ProjectEst.objects.filter(project__capital__code='CD', project__pcategory__code='LM',  project__book_id__in=[2,3], project__statusproj_id=1, project__is_adn='True').all().order_by('-project__id')
        elif stage == 'b':
            objects = ProjectEst.objects.filter(project__capital__code='CD', project__pcategory__code='LM',  project__book_id__in=[6], project__statusproj_id=1, project__is_adn='True').all().order_by('-project__id')
        elif stage == 'c':
            objects = ProjectEst.objects.filter(project__capital__code='CD', project__pcategory__code='LM',  project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True').all().order_by('-project__id')
        elif stage == 'd':
            # Submisaun Dokumentu ba UIVP   
            objects = VerTracks.objects.filter(ver__eval__proj__capital__code='CD', ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', is_start='True').all().order_by('ver__eval__proj__id')   
        elif stage == 'e':
            # Total Dokumentus Nebe Sei Iha Prosesu Verifikasaun UIVP
            objects = VerTracks.objects.filter(ver__eval__proj__capital__code='CD',  ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', is_start='True', is_end='False').all().order_by('ver__eval__proj__id')   
        elif stage == 'f':
            # Total Dokumentus Devolve Husi UIVP
            objects = VerSecEng.objects.filter(ver__eval__proj__capital__code='CD', ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', ver__is_end='False', is_end='False', is_eng_back='True', is_eng_read='True', status='DEVOLVE').all().order_by('ver__eval__proj__id')
            vertrack = VerTracks.objects.filter(ver__eval__proj__capital__code='CD', ver__eval__proj__pcategory__code='LM',ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', is_start='True', is_end ='False').all().order_by('ver__eval__proj__id')  
        elif stage == 'g':   
            # Total Dokumentu Pasa iha Verifikasaun UIVP
            objects = VerTracks.objects.filter(ver__eval__proj__capital__code='CD',  ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', ver__is_end=True,is_start='True',is_end ='True').all().order_by('ver__eval__proj__id')
        elif stage == 'h':
            # Submisaun Dokumentu ba ADN
            objects  = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='LM',eval__proj__book_id__in=[2,3,6],eval__proj__statusproj_id=1,eval__proj__is_adn='True',is_ver_start="True").order_by('-eval__proj__id') 
        elif stage == 'i':
            # Projetu ne'ebe iha prosesu verifikaun ADN
            objects = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='LM', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__is_adn='True', is_adn_in="False").order_by('-eval__proj__id')
        elif stage == 'j':  
            # Devolve Husi ADN
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__pcategory__code='LM',evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result="False", is_return="True").order_by('-evallet__eval__proj__id')
            evaltrack  = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='LM', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
        elif stage == 'k':  
            # Rezultadu Verifikaun ADN
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__pcategory__code='LM',evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='True', is_return='False').order_by('-evallet__eval__proj__id')
            evaltrack  = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='LM', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
        elif stage == 'k1':  
            # Submete ba UIVP
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__pcategory__code='LM',evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='True', is_return='False').order_by('-evallet__eval__proj__id')
            evaltrack  = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='LM', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_adn_in='True').all().order_by('-eval__proj__id')
        elif stage == 'k2':  
            # UIVP atualiza rezultad verifikasaun ADN
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__pcategory__code='LM',evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='True', is_return='False').order_by('-evallet__eval__proj__id')
            evaltrack  = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='LM', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_adn_in='True', eval__proj__projectest__adn__gt=0).all().order_by('-eval__proj__id')
            objects1 = ProjectEst.objects.filter().all()
        elif stage == 'k3':  
            # Submete ba Gabinete Ministro
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__pcategory__code='LM',evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='True', is_return='False').order_by('-evallet__eval__proj__id')
            evaltrack  = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='LM', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_gab_in_1='True').all().order_by('-eval__proj__id')
            objects1 = ProjectEst.objects.filter().all()
        elif stage == 'k4':  
            # Aprova Husi Gabinete Ministro
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__pcategory__code='LM',evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='True', is_return='False').order_by('-evallet__eval__proj__id')
            evaltrack  = EvalTrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='LM', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_appr='True').all().order_by('-eval__proj__id')
            objects1 = ProjectEst.objects.filter().all()
        
        
        #l
        #m
        #n
        #o
        #p
        #p1
        #p2
        #p3
        elif stage == 'q':
            # Dokumentu Ba DNA
            objects =Proc.objects.filter(proj__capital__code='CD', proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='True', is_lock="True" ).all().order_by('-proj__id')
        elif stage == 'r':
            # Rekizasaun Dokumentu Iha DNA
            objects =Proc.objects.filter(proj__capital__code='CD', proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='True', is_req_start="True", is_req_end='False').all().order_by('-proj__id')
        elif stage == 's':
            # Dokumentu ho Rzultadu Iha DNA
            objects =Proc.objects.filter(proj__capital__code='CD', proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='True', is_res_start="True", is_res_end='True').all().order_by('-proj__id')
        elif stage == 't':
            # Dokumentu ba kontraktu
            objects =Contract.objects.filter(project__capital__code='CD', project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True', status_id="7", is_complete='False').all().order_by('-project__id')   
        
        elif stage == 'u':
            # MOntante ba kontraktu as liu
            objects =Contract.objects.filter(project__capital__code='CD', project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True', status_id="7", total__lt=500000).all().order_by('-project__id')   
        
        elif stage == 'v':
            # MOntante ba kontraktu menos ou hanesan
            objects =Contract.objects.filter(project__capital__code='CD', project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True', status_id="7", total__gte=500000).all().order_by('-project__id')   
                  
          
    elif pcat == 'fi':
        if stage == 'a':
            objects = ProjectEst.objects.filter(project__capital__code='CD', project__pcategory__code='FI',  project__book_id__in=[2,3], project__statusproj_id=1, project__is_adn='True').all().order_by('-project__id')
        elif stage == 'b':
            objects = ProjectEst.objects.filter(project__capital__code='CD', project__pcategory__code='FI',  project__book_id__in=[6], project__statusproj_id=1, project__is_adn='True').all().order_by('-project__id')
        elif stage == 'c':
            objects = ProjectEst.objects.filter(project__capital__code='CD', project__pcategory__code='FI',  project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True').all().order_by('-project__id')
        elif stage == 'd':
            # Submisaun Dokumentu ba UIVP   
            objects = VerTracks.objects.filter(ver__eval__proj__capital__code='CD', ver__eval__proj__pcategory__code='FI', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', is_start='True').all().order_by('ver__eval__proj__id')   
        elif stage == 'e':
            # Total Dokumentus Nebe Sei Iha Prosesu Verifikasaun UIVP
            objects = VerTracks.objects.filter(ver__eval__proj__capital__code='CD',  ver__eval__proj__pcategory__code='FI', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', is_start='True', is_end='False').all().order_by('ver__eval__proj__id')   
        elif stage == 'f':
            # Total Dokumentus Devolve Husi UIVP
            objects = VerSecEng.objects.filter(ver__eval__proj__capital__code='CD', ver__eval__proj__pcategory__code='FI', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', ver__is_end='False', is_end='False', is_eng_back='True', is_eng_read='True', status='DEVOLVE').all().order_by('ver__eval__proj__id')
            vertrack = VerTracks.objects.filter(ver__eval__proj__capital__code='CD', ver__eval__proj__pcategory__code='FI',ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', is_start='True', is_end ='False').all().order_by('ver__eval__proj__id')  
        elif stage == 'g':   
            # Total Dokumentu Pasa iha Verifikasaun UIVP
            objects = VerTracks.objects.filter(ver__eval__proj__capital__code='CD',  ver__eval__proj__pcategory__code='FI', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', ver__is_end=True,is_start='True',is_end ='True').all().order_by('ver__eval__proj__id')
        elif stage == 'h':
            # Submisaun Dokumentu ba ADN
            objects = EvalFITrack.objects.filter(eval__proj__capital__code='CD',eval__proj__pcategory__code='FI',eval__proj__book_id__in=[2,3,6],eval__proj__statusproj_id=1,eval__proj__is_adn='True',is_uvip_out_1='True').order_by('-eval__proj__id')   
        elif stage == 'i':
             # Projetu ne'ebe iha prosesu verifikaun ADN
             objects = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_uvip_in_2='False').all().order_by('-eval__proj__id')
        elif stage == 'j':
           # Devolve Husi ADN
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD',evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, is_result='False', is_return='True').order_by('-evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
        elif stage == 'k': 
            # Rezultadu Verifikaun ADN
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD',evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1,evallet__eval__proj__is_adn='True', is_result='True', is_return='False').order_by('-evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')    
        elif stage == 'k1': 
            # Submete ba UIVP
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD',evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1,evallet__eval__proj__is_adn='True', is_result='True', is_return='False').order_by('-evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_uvip_in_2='True').all().order_by('-eval__proj__id')    
        elif stage == 'k2': 
            # Atualiza Rezultadu verifikasaun ADN
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD',evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1,evallet__eval__proj__is_adn='True', is_result='True', is_return='False').order_by('-evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_uvip_in_2='True' , eval__proj__projectest__adn__gt=0).all().order_by('-eval__proj__id')    
            objects1 = ProjectEst.objects.filter().all()
        elif stage == 'k3': 
            # Submete ba Gabinete Ministro
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD',evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1,evallet__eval__proj__is_adn='True', is_result='True', is_return='False').order_by('-evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_gab_in_1='True' , eval__proj__projectest__adn__gt=0).all().order_by('-eval__proj__id')    
            objects1 = ProjectEst.objects.filter().all()
        elif stage == 'k4': 
            # Aprova Gabinete Ministro
            objects  = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital__code='CD',evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1,evallet__eval__proj__is_adn='True', is_result='True', is_return='False').order_by('-evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_appr='True' , eval__proj__projectest__adn__gt=0).all().order_by('-eval__proj__id')    
            objects1 = ProjectEst.objects.filter().all()
        elif stage == 'l':
            # Dokumentu Ba SGP
             objects =EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_appr='True', is_gab_out_1='True').all().order_by('-eval__proj__id')
        elif stage == 'm':
            # Dokumentu ba CNA
            objects =EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_appr='True',is_gab_out_3='True').all().order_by('-eval__proj__id') 
        elif stage == 'n':
            # Dokumentu Prosesa Husi CNA
            objects =EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', eval__is_end='False', is_end='False', is_appr='True', is_gab_out_3='True', is_gab_in_4='True').all().order_by('-eval__proj__id')      
        elif stage == 'o':
            # Dokumentu Devolve Husi CNA
            objects = EvalLetCNABack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='False', is_return='True').all().order_by('evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
        elif stage == 'p':
            # Rezultadu Dokumentu Husi CNA
            objects = EvalLetCNABack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='True', is_return='False').all().order_by('evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True').all().order_by('-eval__proj__id')
    
        elif stage == 'p1':
            # Rezultadu Dokumentu Husi CNA
            objects = EvalLetCNABack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='True', is_return='False').all().order_by('evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True',is_gab_in_4='True').all().order_by('-eval__proj__id')
    
        elif stage == 'p2':
            # Rezultadu Dokumentu Husi CNA
            objects = EvalLetCNABack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='True', is_return='False').all().order_by('evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True',is_gab_sign='True').all().order_by('-eval__proj__id')
    
        elif stage == 'p3':
            # Rezultadu Dokumentu Husi CNA
            objects = EvalLetCNABack.objects.filter(evallet__eval__proj__capital__code='CD', evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, evallet__eval__proj__is_adn='True', is_result='True', is_return='False').all().order_by('evallet__eval__proj__id')
            evaltrack  = EvalFITrack.objects.filter(eval__proj__capital__code='CD', eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_uvip_out_5='True').all().order_by('-eval__proj__id')
        #q
        #r
        #s
        #t
        
        elif stage == 'u':
            # MOntante ba kontraktu as liu
            objects =Contract.objects.filter(project__capital__code='CD', project__pcategory__code='FI', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True', status_id="7", total__lt=500000).all().order_by('-project__id')   
        
        elif stage == 'v':
            # MOntante ba kontraktu menos ou hanesan
            objects =Contract.objects.filter(project__capital__code='CD', project__pcategory__code='FI', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True', status_id="7", total__gte=500000).all().order_by('-project__id')   
             
    
    if pcat == 'cd' or pcat == 'lm' or pcat == 'fi':
        if stage == 'a' or stage == 'b' or stage == 'c':  
            context = {'title': 'Lista Projetu','legend': 'Lista Projetu','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/proj_list.html', context)
        elif stage == 'd' or stage == 'e' or stage == 'g':
            context = {'pcat': pcat, 'stage': stage,'title': 'TRACK VERIFIKASAUN','legend': 'TRACK VERIFIKASAUN','objects':objects,}
            return render(request, 'track/ver_list.html', context)
        elif stage == 'f':
            context = {'pcat': pcat, 'stage': stage,'title': 'Lista Projetu Verifikasaun','legend': 'Lista Projetu Verifikasaun','objects':objects,'vertrack':vertrack}
            return render(request, 'report_recap/proj_eval_uivp_list.html', context)
        elif stage == 'h' or stage == 'i' or stage == 'l' or stage == 'm': 
            context = {'pcat': pcat, 'stage': stage, 'title': 'LISTA DOKUMENTU AVALIASAUN','legend': 'LISTA DOKUMENTU AVALIASAUN','objects':objects,'evaltrack':evaltrack}
            return render(request, 'track/eval_list.html', context)
        elif stage == 'j' or stage == 'k' or stage == 'k1' or stage == 'k3' or stage == 'o' or stage == 'p' or stage == 'p1' or stage == 'p2' or stage == 'p3':
            context = {'title': 'Lista Projetu Verifikasaun','legend': 'Lista Projetu Verifikasaun','objects': objects, 'pcat': pcat, 'stage': stage, 'evaltrack':evaltrack}
            return render(request, 'report_recap/proj_eval_adn_list.html', context)
        
        elif stage == 'k2' or stage == 'k3' or stage == 'k4':
            context = {'title': 'Rezultadu Lista Projetu Verifikasaun Husi ADN','legend': 'Rezultadu Lista Projetu Verifikasaun Husi ADN','objects': objects, 'pcat': pcat, 'stage': stage, 'evaltrack':evaltrack, 'objects1':objects1}
            return render(request, 'report_recap/update_estimation_adn.html', context)
        
        elif stage == 'q':
            context = {'title': 'Lista Tender iha DNA','legend': 'Lista Tender iha DNA','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/tender_list.html', context) 
        elif stage == 'r':
            context = {'title': 'TRACK REKIZASAUN CPV','legend': 'TRACK REKIZASAUN CPV','objects':objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'proc_dna/req_list.html', context)
        elif stage == 's':
            context = {'title': 'LISTA REZULTADU TENDER','legend': 'LISTA REZULTADU TENDER','objects':objects,'pcat': pcat, 'stage': stage}
            return render(request, 'proc_dna/res_list.html', context)
        elif stage == 't' or stage == 'u' or stage == 'v':
            context = {'title': 'LISTA KONTRATU','legend': 'LISTA KONTRATU','objects':objects,'pcat': pcat, 'stage': stage}
            return render(request, 'contract/cont_list.html', context)
          
@login_required   
@allowed_users(allowed_roles=['sigp_admin', 'sigp_dna', 'sigp_uivp', 'sigp_dnof', 'sigp_gabm', 'sigp_dgaf', 'sigp_min', 'sigp_op'])   
def rRecapVerProjList2(request, pcat, stage):
    objects = []
    vertrack = []
    if pcat == 'lm':
        if stage == 'a':
            objects = ProjectEst.objects.filter(project__pcategory__code='LM',  project__book_id__in=[2,3], project__statusproj_id=1, project__is_adn='False').all().order_by('-project__id')
        elif stage == 'b':
            objects = ProjectEst.objects.filter(project__pcategory__code='LM',  project__book_id__in=[6], project__statusproj_id=1, project__is_adn='False').all().order_by('-project__id')
        elif stage == 'c':
            objects = ProjectEst.objects.filter(project__pcategory__code='LM',  project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='False').all().order_by('-project__id')
        elif stage == 'd':
            # Submisaun Dokumentu ba UIVP   
            objects = VerTracks.objects.filter(ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', is_start='True').all().order_by('ver__eval__proj__id')
        elif stage == 'e':
            # Total Dokumentus Nebe Sei Iha Prosesu Verifikasaun UIVP
            #objects = VerSecEng.objects.filter(ver__eval__proj__pcategory__code='LM',  ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', ver__is_end='False',is_end='False').all().order_by('ver__eval__proj__id')
            #vertrack = VerTracks.objects.filter(ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', is_start='True',is_end ='False').all().order_by('ver__eval__proj__id')
            objects = VerTracks.objects.filter(ver__eval__proj__capital__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', ver__is_end='False', is_start='True', is_end='False').all().order_by('ver__eval__proj__id')   
        elif stage == 'f':
            # Total Dokumentus Devolve Husi UIVP
            objects = VerSecEng.objects.filter(ver__eval__proj__pcategory__code='LM',  ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', ver__is_end='False', is_end='False', is_eng_back='True', is_eng_read='True', status='DEVOLVE').all().order_by('ver__eval__proj__id')
            vertrack = VerTracks.objects.filter(ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', is_start='True', is_end ='True').all().order_by('ver__eval__proj__id')
        elif stage == 'g':   
            # Total Dokumentu Pasa iha Verifikasaun UIVP
            objects = VerSecEng.objects.filter(ver__eval__proj__pcategory__code='LM',  ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', ver__is_end='True', is_end='True', is_eng_back='True', is_eng_read='True', status='PASA').all().order_by('ver__eval__proj__id')
            vertrack = VerTracks.objects.filter(ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', is_start='True').all().order_by('ver__eval__proj__id')
        elif stage == 'h':    
            # Total Dokumentus Submete Ba Gabinete Ministro
            objects = EvalTrack.objects.filter(eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='False', eval__ver__is_end='True', is_gab_in='True').all().order_by('eval__proj__id')
        elif stage == 'i':
            # Total Dokumentus Devolve Husi Gabinete Ministro
            objects = EvalTrack.objects.filter(eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='False', eval__ver__is_end='True', is_gab_in='True', eval__is_appr='False', eval__is_return='True').all().order_by('eval__proj__id')
        elif stage == 'j':
            # Total Dokumentus Aprovadu Husi Gabinete Ministro
            objects = EvalTrack.objects.filter(eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='False', eval__ver__is_end='True', is_gab_in='True', eval__is_appr='True', eval__is_return='False').all().order_by('eval__proj__id')
        elif stage == 'k':
            # Total Dokumentus Submete ba DNA
            objects = Proc.objects.filter(proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='False',).all().order_by('proj__id')
        elif stage == 'l':
            # Total Requisisaun iha prosesu ba DNA
            objects = Proc.objects.filter(proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='False', is_req_start='True', is_req_end='False').all().order_by('proj__id')
        elif stage == 'm':
            # Total Rezultadu Tender husi DNA
            objects = Proc.objects.filter(proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='False', is_res_start='True', is_res_end='True').all().order_by('proj__id')
        elif stage == 'n':
            # Total Kontratu Ba DNA ho status hein desizaun
            objects = Contract.objects.filter(project__pcategory__code='LM', project__book_id__in=[2,3,6],  project__statusproj_id=1, project__is_adn='False', status_id__in=[7], is_complete='False').all().order_by('project__id')
        elif stage == 'o':
            # Montante ba kontraktu as liu
            objects = Contract.objects.filter(project__pcategory__code='LM', project__book_id__in=[2,3,6],  project__statusproj_id=1, project__is_adn='False', status_id__in=[7], total__lt=500000).all().order_by('project__id')
        # elif stage == 'p':
        #     # Montante ba kontraktu menos ou hanesan
        #     objects = Contract.objects.filter(project__pcategory__code='LM', project__book_id__in=[2,3,6],  project__statusproj_id=1, project__is_adn='False', status_id__in=[7], total__gte=500000).all().order_by('project__id')
    
    
    if pcat == 'cd' or pcat == 'cm' or pcat == 'bs':
        if stage == 'a':
            objects = ProjectEst.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3], project__statusproj_id=1, project__is_adn='False').all().order_by('-project__id')
        elif stage == 'b':
            objects = ProjectEst.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[6], project__statusproj_id=1, project__is_adn='False').all().order_by('-project__id')
        elif stage == 'c':
            objects = ProjectEst.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='False').all().order_by('-project__id')
        elif stage == 'd':
            objects = VerTracks.objects.filter(ver__eval__proj__capital__code__iexact=pcat, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', is_start='True').all().order_by('ver__eval__proj__id')
        elif stage == 'e':
            # Total Dokumentus Nebe Sei Iha Prosesu Verifikasaun UIVP
            objects = VerSecEng.objects.filter(ver__eval__proj__capital__code__iexact=pcat, ver__eval__proj__pcategory__code='LM',  ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', ver__is_end='False',is_end='False').all().order_by('ver__eval__proj__id')
        elif stage == 'f':
            # Total Dokumentus Devolve Husi UIVP
            objects = VerSecEng.objects.filter(ver__eval__proj__capital__code__iexact=pcat, ver__eval__proj__pcategory__code='LM',  ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', ver__is_end='False', is_end='False', is_eng_back='True', is_eng_read='True', status='DEVOLVE').all().order_by('ver__eval__proj__id')
        elif stage == 'g':   
            # Total Dokumentu Pasa iha Verifikasaun UIVP
            objects = VerSecEng.objects.filter(ver__eval__proj__capital__code__iexact=pcat, ver__eval__proj__pcategory__code='LM',  ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', ver__is_end='True', is_end='True', is_eng_back='True', is_eng_read='True', status='PASA').all().order_by('ver__eval__proj__id')
        elif stage == 'h':    
            # Total Dokumentus Submete Ba Gabinete Ministro
            objects = EvalTrack.objects.filter(eval__proj__capital__code__iexact=pcat, eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='False', eval__ver__is_end='True', is_gab_in='True').all().order_by('eval__proj__id')
        elif stage == 'i':
            # Total Dokumentus Devolve Husi Gabinete Ministro
            objects = EvalTrack.objects.filter(eval__proj__capital__code__iexact=pcat, eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='False', eval__ver__is_end='True', is_gab_in='True', eval__is_appr='False', eval__is_return='True').all().order_by('eval__proj__id')
        elif stage == 'j':
            # Total Dokumentus Aprovadu Husi Gabinete Ministro
            objects = EvalTrack.objects.filter(eval__proj__capital__code__iexact=pcat, eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='False', eval__ver__is_end='True', is_gab_in='True', eval__is_appr='True', eval__is_return='False').all().order_by('eval__proj__id')
        elif stage == 'k':
            # Total Dokumentus Submete ba DNA
            objects = Proc.objects.filter(proj__capital__code__iexact=pcat, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='False',).all().order_by('proj__id')
            # Total Requisisaun iha prosesu ba DNA
        elif stage == 'l':
            objects = Proc.objects.filter(proj__capital__code__iexact=pcat, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='False', is_req_start='True', is_req_end='False').all().order_by('proj__id')
            # Total Rezultadu Tender husi DNA
        elif stage == 'm':
            objects = Proc.objects.filter(proj__capital__code__iexact=pcat, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='False', is_res_start='True', is_res_end='True').all().order_by('proj__id')
        elif stage == 'n':
            # Total Kontratu Ba DNA ho status hein desizaun
            objects = Contract.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3,6],  project__statusproj_id=1, project__is_adn='False', status_id__in=[7], is_complete='False').all().order_by('project__id')
        elif stage == 'o':
            # Montante ba kontraktu as liu
            objects = Contract.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3,6],  project__statusproj_id=1, project__is_adn='False', status_id__in=[7], total__lt=500000).all().order_by('project__id')
        # elif stage == 'p':
        #     # Montante ba kontraktu menos ou hanesan
        #     objects = Contract.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3,6],  project__statusproj_id=1, project__is_adn='False', status_id__in=[7], total__gte=500000).all().order_by('project__id')
   
     
    if pcat == 'lm' or pcat == 'cd' or pcat == 'cm' or pcat == 'bs':
        if stage == 'a' or stage == 'b' or stage == 'c':
            context = {'title': 'Lista Projetu','legend': 'Lista Projetu','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/proj_list2.html', context)
        
        elif stage == 'd' or stage == 'e':
            context = {'title': 'Lista Projetu','legend': 'Lista Projetu','objects': objects, 'pcat': pcat, 'stage': stage, 'vertrack':vertrack}
            return render(request, 'track/ver_list.html', context)
        
        elif stage == 'f' or stage == 'g':
            context = {'title': 'Lista Projetu Verifikasaun','legend': 'Lista Projetu Verifikasaun','objects': objects, 'pcat': pcat, 'stage': stage, 'vertrack':vertrack
                }
            return render(request, 'report_recap/proj_eval_uivp_list.html', context)
        
        elif stage == 'h' or stage == 'i' or stage == 'j':
            context = {'title': 'Evaluasaun Lista Projetu','legend': 'Evaluasaun Lista Projetu','objects': objects, 'pcat': pcat, 'stage': stage, 'vertrack':vertrack
                }
            return render(request, 'track/eval_list2.html', context)
        elif stage == 'k':
            context = {'title': 'Lista Tender iha DNA','legend': 'Lista Tender iha DNA','objects': objects, 'pcat': pcat, 'stage': stage, 'vertrack':vertrack}
            return render(request, 'report_recap/tender_list.html', context) 
        elif stage == 'l':
            context = {'title': 'LISTA REKIZASAUN TENDER','legend': 'LISTA REKIZASAUN TENDER','objects':objects,'pcat':pcat,'stage': stage }
            return render(request, 'proc_dna/req_list.html', context)
        elif stage == 'm':
            context = {'title': 'LISTA REZULTADU TENDER','legend': 'LISTA REZULTADU TENDER','objects':objects,'pcat':pcat}
            return render(request, 'proc_dna/res_list.html', context)
        elif stage == 'n' or stage == 'o':
            context = {'title': 'LISTA KONTRATU','legend': 'LISTA KONTRATU','objects':objects,'cap':pcat}
            return render(request, 'contract/cont_list.html', context)

@login_required   
@allowed_users(allowed_roles=['sigp_admin', 'sigp_dna', 'sigp_uivp', 'sigp_dnof', 'sigp_gabm', 'sigp_dgaf', 'sigp_min', 'sigp_op'])   
def rRecapVerProjList3(request, pcat, stage):
    objects = []
    vertrack = []
    
    if pcat == 'cd':
        if stage == 'a':
            objects = ProjectEst.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3], project__statusproj_id=1).all().order_by('-project__id')
        elif stage == 'b':
            objects = ProjectEst.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[6], project__statusproj_id=1).all().order_by('-project__id')
        elif stage == 'c':
            objects = ProjectEst.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='False').all().order_by('-project__id')
        elif stage == 'd':
            objects = VerTracks.objects.filter(ver__eval__proj__capital__code__iexact=pcat, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, is_start='True').all().order_by('ver__eval__proj__id')
        elif stage == 'e':
            # Total Dokumentus Nebe Sei Iha Prosesu Verifikasaun UIVP
            objects = VerSecEng.objects.filter(ver__eval__proj__capital__code__iexact=pcat, ver__eval__proj__pcategory__code='LM',  ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__is_end='False',is_end='False').all().order_by('ver__eval__proj__id')
        elif stage == 'f':
            # Total Dokumentus Devolve Husi UIVP
            objects = VerSecEng.objects.filter(ver__eval__proj__capital__code__iexact=pcat, ver__eval__proj__pcategory__code='LM',  ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__is_end='False', is_end='False', is_eng_back='True', is_eng_read='True', status='DEVOLVE').all().order_by('ver__eval__proj__id')
        elif stage == 'g':   
            # Total Dokumentu Pasa iha Verifikasaun UIVP
            objects = VerSecEng.objects.filter(ver__eval__proj__capital__code__iexact=pcat, ver__eval__proj__pcategory__code='LM',  ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__is_end='True', is_end='True', is_eng_back='True', is_eng_read='True', status='PASA').all().order_by('ver__eval__proj__id')
        elif stage == 'h':    
            # Total Dokumentus Submete Ba Gabinete Ministro
            objects = EvalTrack.objects.filter(eval__proj__capital__code__iexact=pcat, eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1,  eval__ver__is_end='True', is_gab_in='True').all().order_by('eval__proj__id')
        elif stage == 'i':
            # Total Dokumentus Devolve Husi Gabinete Ministro
            objects = EvalTrack.objects.filter(eval__proj__capital__code__iexact=pcat, eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__ver__is_end='True', is_gab_in='True', eval__is_appr='False', eval__is_return='True').all().order_by('eval__proj__id')
        elif stage == 'j':
            # Total Dokumentus Aprovadu Husi Gabinete Ministro
            objects = EvalTrack.objects.filter(eval__proj__capital__code__iexact=pcat, eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__ver__is_end='True', is_gab_in='True', eval__is_appr='True', eval__is_return='False').all().order_by('eval__proj__id')
        elif stage == 'k':
            # Total Dokumentus Submete ba DNA
            objects = Proc.objects.filter(proj__capital__code__iexact=pcat, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1).all().order_by('proj__id')
            # Total Requisisaun iha prosesu ba DNA
        elif stage == 'l':
            objects = Proc.objects.filter(proj__capital__code__iexact=pcat, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, is_req_start='True', is_req_end='False').all().order_by('proj__id')
            # Total Rezultadu Tender husi DNA
        elif stage == 'm':
            objects = Proc.objects.filter(proj__capital__code__iexact=pcat, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, is_res_start='True', is_res_end='True').all().order_by('proj__id')
        elif stage == 'n':
            # Total Kontratu Ba DNA ho status hein desizaun
            objects = Contract.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3,6],  project__statusproj_id=1, status_id__in=[7], is_complete='False').all().order_by('project__id')
        elif stage == 'o':
            # Montante ba kontraktu as liu
            objects = Contract.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3,6],  project__statusproj_id=1, status_id__in=[7], total__lt=100000).all().order_by('project__id')
        elif stage == 'p':
            # Montante ba kontraktu menos ou hanesan
            objects = Contract.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3,6],  project__statusproj_id=1, status_id__in=[7], total__gte=100000).all().order_by('project__id')
     
    if  pcat == 'cd':
        if stage == 'a' or stage == 'b' or stage == 'c':
            context = {'title': 'Lista Projetu','legend': 'Lista Projetu','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/proj_list2.html', context)
        
        elif stage == 'd' or stage == 'e':
            context = {'title': 'Lista Projetu','legend': 'Lista Projetu','objects': objects, 'pcat': pcat, 'stage': stage, 'vertrack':vertrack}
            return render(request, 'track/ver_list.html', context)
        
        elif stage == 'f' or stage == 'g':
            context = {'title': 'Lista Projetu Verifikasaun','legend': 'Lista Projetu Verifikasaun','objects': objects, 'pcat': pcat, 'stage': stage, 'vertrack':vertrack
                }
            return render(request, 'report_recap/proj_eval_uivp_list.html', context)
        
        elif stage == 'h' or stage == 'i' or stage == 'j':
            context = {'title': 'Evaluasaun Lista Projetu','legend': 'Evaluasaun Lista Projetu','objects': objects, 'pcat': pcat, 'stage': stage, 'vertrack':vertrack
                }
            return render(request, 'track/eval_list2.html', context)
        elif stage == 'k':
            context = {'title': 'Lista Tender iha DNA','legend': 'Lista Tender iha DNA','objects': objects, 'pcat': pcat, 'stage': stage, 'vertrack':vertrack}
            return render(request, 'report_recap/tender_list.html', context) 
        elif stage == 'l':
            context = {'title': 'LISTA REKIZASAUN TENDER','legend': 'LISTA REKIZASAUN TENDER','objects':objects,'pcat':pcat,'stage': stage }
            return render(request, 'proc_dna/req_list.html', context)
        elif stage == 'm':
            context = {'title': 'LISTA REZULTADU TENDER','legend': 'LISTA REZULTADU TENDER','objects':objects,'pcat':pcat}
            return render(request, 'proc_dna/res_list.html', context)
        elif stage == 'n' or stage == 'o' or stage == 'p':
            context = {'title': 'LISTA KONTRATU','legend': 'LISTA KONTRATU','objects':objects,'cap':pcat}
            return render(request, 'contract/cont_list.html', context)

@login_required   
@allowed_users(allowed_roles=['sigp_admin', 'sigp_dna', 'sigp_uivp', 'sigp_dnof', 'sigp_gab', 'sigp_dgaf', 'sigp_min', 'sigp_op'])   
def rRecapInspProjList1(request, pcat, stage):
    objects = []
    invtrack = []
    if pcat == 'cd':
        if stage == 'a':
            objects=Contract.objects.filter(project__capital__code='CD', project__book_id__in=[2,3], status=1, is_complete='False',project__is_adn='True').all().order_by('-project__id')
        elif stage == 'b':
            objects=Contract.objects.filter(project__capital__code='CD', project__book_id__in=[6], status=1, is_complete='False',project__is_adn='True').all().order_by('-project__id')
        elif stage == 'c':
            objects=Contract.objects.filter(project__capital__code='CD', project__book_id__in=[2,3,6], status=1, is_complete='False',project__is_adn='True').all().order_by('-project__id')
        elif stage == 'd':
            #invoice Husi Projetu
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__project__is_adn='True', inv__cont__is_complete='False', inv__is_lock='True', inv__is_ready='True').select_related('inv__cont__project','inv__cont__status','inv__cont__type').prefetch_related('inv__cont__contractcomp__company').order_by('-inv__cont__project__id')
        elif stage == 'e':
            # Prsosesu Inspeksaun Husi UIVP
            objects = InspTracks.objects.filter(insp__cont__project__capital__code='CD', insp__cont__project__book_id__in=[2,3,6], insp__cont__status=1, insp__cont__project__is_adn='True', is_start='True', is_end='False').all().order_by('insp__cont__project__id')
        elif stage == 'f':
            # UIVP Devolve 
            pass    
        elif stage == 'g':
            # UIVP Rekomenda pagamentu
            objects = CertPay.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_lock='True').order_by('inv__cont__project__id')  
        elif stage == 'h':
            # Submete ba ADN
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uvip_out_1='True').all().order_by('inv__cont__project__id')
        elif stage == 'i':
            # ADN Prosesu
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uvip_out_1='True', is_adn_in='False').all().order_by('inv__cont__project__id')
        elif stage == 'j':
            # ADN Devolve
            objects = InvLetAdnBack.objects.filter(invlet__inv__cont__project__capital__code='CD', invlet__inv__cont__project__book_id__in=[2,3,6], invlet__inv__cont__status=1, invlet__inv__cont__is_complete='False', invlet__inv__cont__project__is_adn='True', is_return='True').all().order_by('invlet__inv__cont__project__id')
        elif stage == 'k':
            # ADN Rekomenda pagamentu
            objects = PayRecom.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True').all().order_by('inv__cont__project__id')
        
        elif stage == 'l':
            # Submete ba UIVP
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_adn_in='True').all().order_by('inv__cont__project__id')
        # elif stage == 'm':
        #     # Prosesu UIVP
        #     objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uivp_out2='False').all().order_by('inv__cont__project__id')
        # elif stage == 'n':
            # UIVP Certifika Pagamentu
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uivp_out2='True').all().order_by('inv__cont__project__id')
        
        elif stage == 'o':
            # Submete ba Gabinete Ministro
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_gab_in='True').all().order_by('inv__cont__project__id')
        elif stage == 'p':
            # Gabinete Ministro Prosesu
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_gap_app='True').all().order_by('inv__cont__project__id')
        elif stage == 'q':
            # Submete ba DGAF
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True').all().order_by('inv__cont__project__id')
        elif stage == 'r':
            # Prosesu DGAF
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True', is_dnof_back_out='False').all().order_by('inv__cont__project__id')
        elif stage == 's':
            # Pagamentu Final
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True', is_dnof_back_out='True').all().order_by('inv__cont__project__id')
                 
    if pcat == 'lm':
        if stage == 'a':
            objects=Contract.objects.filter(project__capital__code='CD', project__pcategory__code='LM', project__book_id__in=[2,3], status=1, is_complete='False',project__is_adn='True').all().order_by('-project__id')
        elif stage == 'b':
            objects=Contract.objects.filter(project__capital__code='CD', project__pcategory__code='LM', project__book_id__in=[6], status=1, is_complete='False',project__is_adn='True').all().order_by('-project__id')
        elif stage == 'c':
            objects=Contract.objects.filter(project__capital__code='CD', project__pcategory__code='LM', project__book_id__in=[2,3,6], status=1, is_complete='False',project__is_adn='True').all().order_by('-project__id')  
        elif stage == 'd':
            # invoice Husi Projetu
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__project__is_adn='True', inv__cont__is_complete='False', inv__is_lock='True', inv__is_ready='True').select_related('inv__cont__project','inv__cont__status','inv__cont__type').prefetch_related('inv__cont__contractcomp__company').order_by('-inv__cont__project__id')
        elif stage == 'e':
            # Prsosesu Inspeksaun Husi UIVP
            objects = InspTracks.objects.filter(insp__cont__project__capital__code='CD', insp__cont__project__pcategory__code='LM', insp__cont__project__book_id__in=[2,3,6], insp__cont__status=1, insp__cont__project__is_adn='True', is_start='True', is_end='False').all().order_by('insp__cont__project__id')
        elif stage == 'f':
            # UIVP Devolve 
            pass
        elif stage == 'g':
            # UIVP Rekomenda pagamentu
            objects = CertPay.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_lock='True').all().order_by('inv__cont__project__id')
        elif stage == 'h':
            # Submete ba ADN
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uvip_out_1='True').all().order_by('inv__cont__project__id')
        elif stage == 'i':
            # ADN Prosesu
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uvip_out_1='True', is_adn_in='False').all().order_by('inv__cont__project__id')
        elif stage == 'j':
            # ADN Devolve
            objects = InvLetAdnBack.objects.filter(invlet__inv__cont__project__capital__code='CD', invlet__inv__cont__project__pcategory__code='LM', invlet__inv__cont__project__book_id__in=[2,3,6], invlet__inv__cont__status=1, invlet__inv__cont__is_complete='False', invlet__inv__cont__project__is_adn='True', is_return='True').all().order_by('invlet__inv__cont__project__id')
        elif stage == 'k':
             # ADN Rekomenda pagamentu
            objects = PayRecom.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True').all().order_by('inv__cont__project__id')
        elif stage == 'l':
            # Submete ba UIVP
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_adn_in='True').all().order_by('inv__cont__project__id')
        # elif stage == 'm':
        #     # Prosesu UIVP
        #     objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uivp_out2='False').all().order_by('inv__cont__project__id')
        # elif stage == 'n':
            # UIVP Certifika Pagamentu
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uivp_out2='True').all().order_by('inv__cont__project__id')
        elif stage == 'o':
            # Submete ba Gabinete Ministro
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_gab_in='True').all().order_by('inv__cont__project__id')
        elif stage == 'p':
            # Gabinete Ministro Aprova
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_gap_app='True').all().order_by('inv__cont__project__id')
        elif stage == 'q':
            # Submete ba DGAF
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True').all().order_by('inv__cont__project__id')
        elif stage == 'r':
            # Prosesu DGAF
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True', is_dnof_back_out='False').all().order_by('inv__cont__project__id')
        elif stage == 's':
            # Pagamentu Final
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True', is_dnof_back_out='True').all().order_by('inv__cont__project__id')
                  
    if pcat == 'fi':
        if stage == 'a':
            objects=Contract.objects.filter(project__capital__code='CD', project__pcategory__code='FI', project__book_id__in=[2,3], status=1, is_complete='False',project__is_adn='True').all().order_by('-project__id')
        elif stage == 'b':
            objects=Contract.objects.filter(project__capital__code='CD', project__pcategory__code='FI', project__book_id__in=[6], status=1, is_complete='False',project__is_adn='True').all().order_by('-project__id')
        elif stage == 'c':
            objects=Contract.objects.filter(project__capital__code='CD', project__pcategory__code='FI', project__book_id__in=[2,3,6], status=1, is_complete='False',project__is_adn='True').all().order_by('-project__id')
        elif stage == 'd':
            # invoice Husi Projetu
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__project__is_adn='True', inv__cont__is_complete='False', inv__is_lock='True', inv__is_ready='True').select_related('inv__cont__project','inv__cont__status','inv__cont__type').prefetch_related('inv__cont__contractcomp__company').order_by('-inv__cont__project__id')
        elif stage == 'e':
            # Prosesu Inspeksaun Husi UIVP
            objects = InspTracks.objects.filter(insp__cont__project__capital__code='CD',  insp__cont__project__pcategory__code='FI', insp__cont__project__book_id__in=[2,3,6], insp__cont__status=1, insp__cont__project__is_adn='True', is_start='True', is_end='False').all().order_by('insp__cont__project__id')
        elif stage == 'f':
            # UIVP Devolve 
            pass
        elif stage == 'g':
            # UIVP Rekomenda pagamentu
            objects = CertPay.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_lock='True').all().order_by('inv__cont__project__id')
        elif stage == 'h':
            # Submete ba ADN 
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uvip_out_1='True').all().order_by('inv__cont__project__id')
        elif stage == 'i':
            # ADN Prosesa
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uvip_out_1='True', is_adn_in='False').all().order_by('inv__cont__project__id')
        elif stage == 'j':
            # ADN Devolve
            objects = InvLetAdnBack.objects.filter(invlet__inv__cont__project__capital__code='CD', invlet__inv__cont__project__pcategory__code='FI', invlet__inv__cont__project__book_id__in=[2,3,6], invlet__inv__cont__status=1, invlet__inv__cont__is_complete='False', invlet__inv__cont__project__is_adn='True', is_return='True').all().order_by('invlet__inv__cont__project__id')
        elif stage == 'k':
            # ADN Rekomenda 
            objects = PayRecom.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='FI',inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True').all().order_by('inv__cont__project__id')
        elif stage == 'l':
            # Submete ba UIVP
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_adn_in='True').all().order_by('inv__cont__project__id')
        elif stage == 'm':  
            # Prosesu UIVP
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uivp_out2='False').all().order_by('inv__cont__project__id')
        elif stage == 'n':
            # UIVP Certifika Pagamentu
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uivp_out2='True').all().order_by('inv__cont__project__id')
        elif stage == 'o':
            # Submete ba Gabinete Ministro
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_gab_in='True').all().order_by('inv__cont__project__id')
        elif stage == 'p':
            # Gabinete Aprova
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_gab_app='True').all().order_by('inv__cont__project__id')
        elif stage == 'q':
            # Submete ba DGAF
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True').all().order_by('inv__cont__project__id')
        elif stage == 'r':
            # Prosesu DGAF
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True', is_dnof_back_out='False').all().order_by('inv__cont__project__id')
        elif stage == 's':
            # Pagamentu Final
            objects = InvTrack.objects.filter(inv__cont__project__capital__code='CD', inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True', is_dnof_back_out='True').all().order_by('inv__cont__project__id')
                  
    if pcat == 'cd' or pcat == 'lm' or pcat == 'bs':
        if stage == 'a' or stage == 'b' or stage == 'c':
            context = {'title': 'Lista Kontratu','legend': 'Lista Kontratu','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'contract/cont_list.html', context)
        elif  stage == 'd' or stage == 'h' or stage == 'i' or stage == 'l' or stage == 'm' or stage == 'n' or stage == 'o' or stage == 'p' or stage == 'q' or stage == 'r' or stage == 's':
            context = {'title': 'Lista Resibu','legend': 'Lista Resibu','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'track/inv_list.html', context)
        elif  stage == 'e':
            context = {'title': 'Lista Resibu ba Inpeksaun','legend': 'Lista Resibu ba Inpeksaun','objects': objects, 'pcat': pcat, 'stage': stage, 'invtrack':invtrack}
            return render(request, 'track/insp_list.html', context)
        elif  stage == 'f':
            context = {'title': 'Lista Resibu Devolve husi UIVP','legend': 'Lista Resibu Devolve husi UIVP','objects': objects, 'pcat': pcat, 'stage': stage, 'invtrack':invtrack}
            return render(request, 'track/insp_list.html', context)
        elif  stage == 'g':
            context = {'title': 'Lista Sertifikasaun Pagamentu UIVP','legend': 'Lista Sertifikasaun Pagamentu UIVP','objects': objects, 'pcat': pcat, 'stage': stage, 'invtrack':invtrack}
            return render(request, 'report_recap/cert_pay_list.html', context)
        
        elif  stage == 'j':
            context = {'title': 'Lista Dokumentu Devolve Husi ADN','legend': 'Lista Dokumentu Devolve Husi ADN','objects': objects, 'pcat': pcat, 'stage': stage, 'invtrack':invtrack}
            return render(request, 'report_recap/proj_inv_adn_list.html', context)
 
        elif  stage == 'k':
            context = {'title': 'Lista Sertifikasaun Pagamentu ADN','legend': 'Lista Sertifikasaun Pagamentu ADN','objects': objects, 'pcat': pcat, 'stage': stage, 'invtrack':invtrack}
            return render(request, 'report_recap/pay_recom_list.html', context)
 
@login_required   
@allowed_users(allowed_roles=['sigp_admin', 'sigp_dna', 'sigp_uivp', 'sigp_dnof', 'sigp_gabm', 'sigp_dgaf', 'sigp_min', 'sigp_op'])   
def rRecapInspProjList2(request, pcat, stage):
    objects = []
    
    if pcat == 'lm':
        if stage == 'a':
            objects=Contract.objects.filter(project__pcategory__code='LM', project__book_id__in=[2,3], status=1, is_complete='False',project__is_adn='False').all().order_by('-project__id')
        elif stage == 'b':
            objects=Contract.objects.filter(project__pcategory__code='LM', project__book_id__in=[6], status=1, is_complete='False',project__is_adn='False').all().order_by('-project__id')
        elif stage == 'c':
            objects=Contract.objects.filter(project__pcategory__code='LM', project__book_id__in=[2,3,6], status=1, is_complete='False',project__is_adn='False').all().order_by('-project__id')  
        elif stage == 'd':
            # invoice Husi Projetu
            objects = InvTrack.objects.filter(inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__project__is_adn='False', inv__cont__is_complete='False', inv__is_lock='True', inv__is_ready='True').select_related('inv__cont__project','inv__cont__status','inv__cont__type').prefetch_related('inv__cont__contractcomp__company').order_by('-inv__cont__project__id')
        elif stage == 'e':
            # Prsosesu Inspeksaun Husi UIVP
            objects = InspTracks.objects.filter(insp__cont__project__pcategory__code='LM', insp__cont__project__book_id__in=[2,3,6], insp__cont__status=1, insp__cont__project__is_adn='False', is_start='True', is_end='False').all().order_by('insp__cont__project__id')
        elif stage == 'f':
            # UIVP Devolve 
            pass
        elif stage == 'g':
            # UIVP Rekomenda pagamentu
            objects = CertPay.objects.filter(inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_lock='True').all().order_by('inv__cont__project__id')
        elif stage == 'h':
            # Submete ba Gabinete Ministro
            objects = InvTrack.objects.filter(inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_gab_in='True').all().order_by('inv__cont__project__id')
        elif stage == 'i':
            # Gabinete Ministro Aprova
            objects = InvTrack.objects.filter(inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_gap_app='True').all().order_by('inv__cont__project__id')
        elif stage == 'j':
            # Submete ba DGAF
            objects = InvTrack.objects.filter(inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_dgaf_in='True').all().order_by('inv__cont__project__id')
        elif stage == 'k':
            # Prosesu DGAF
            objects = InvTrack.objects.filter(inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_dgaf_in='True', is_dnof_back_out='False').all().order_by('inv__cont__project__id')
        elif stage == 'l':
            # Pagamentu Final
            objects = InvTrack.objects.filter(inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_dgaf_in='True', is_dnof_back_out='True').all().order_by('inv__cont__project__id')
            
    if pcat == 'cd' or pcat == 'cm' or pcat == 'bs':
        if stage == 'a':
            objects=Contract.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3], status=1, is_complete='False',project__is_adn='False').all().order_by('-project__id')
        elif stage == 'b':
            objects=Contract.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[6], status=1, is_complete='False',project__is_adn='False').all().order_by('-project__id')
        elif stage == 'c':
            objects=Contract.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3,6], status=1, is_complete='False',project__is_adn='False').all().order_by('-project__id')  
        elif stage == 'd':
            # invoice Husi Projetu
            objects = InvTrack.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__project__is_adn='False', inv__cont__is_complete='False', inv__is_lock='True', inv__is_ready='True').select_related('inv__cont__project','inv__cont__status','inv__cont__type').prefetch_related('inv__cont__contractcomp__company').order_by('-inv__cont__project__id')
        elif stage == 'e':
            # Prsosesu Inspeksaun Husi UIVP
            objects = InspTracks.objects.filter(insp__cont__project__capital__code__iexact=pcat,  insp__cont__project__pcategory__code='LM', insp__cont__project__book_id__in=[2,3,6], insp__cont__status=1, insp__cont__project__is_adn='False', is_start='True', is_end='False').all().order_by('insp__cont__project__id')
        elif stage == 'f':
            # UIVP Devolve 
            pass
        elif stage == 'g':
            # UIVP Rekomenda pagamentu
            objects = CertPay.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_lock='True').all().order_by('inv__cont__project__id')
        elif stage == 'h':
            # Submete ba Gabinete Ministro
            objects = InvTrack.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_gab_in='True').all().order_by('inv__cont__project__id')
        elif stage == 'i':
            # Gabinete Ministro Aprova
            objects = InvTrack.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_gap_app='True').all().order_by('inv__cont__project__id')
        elif stage == 'j':
            # Submete ba DGAF
            objects = InvTrack.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_dgaf_in='True').all().order_by('inv__cont__project__id')
        elif stage == 'k':
            # Prosesu DGAF
            objects = InvTrack.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_dgaf_in='True', is_dnof_back_out='False').all().order_by('inv__cont__project__id')
        elif stage == 'l':
            # Pagamentu Final
            objects = InvTrack.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_dgaf_in='True', is_dnof_back_out='True').all().order_by('inv__cont__project__id')
            
    if pcat == 'lm' or  pcat == 'cd' or pcat == 'cm' or pcat == 'bs':
        if stage == 'a' or stage == 'b' or stage == 'c':
            context = {'title': 'Lista Kontratu','legend': 'Lista Kontratu','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/cont_list2.html', context)
        
        elif  stage == 'd' or stage == 'h' or stage == 'i' or stage == 'j' or stage == 'k' or stage == 'l':
            context = {'title': 'Lista Resibu','legend': 'Lista Resibu','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/inv_list2.html', context)
        
        elif  stage == 'e':
            context = {'title': 'Lista Resibu ba Inpeksaun','legend': 'Lista Resibu ba Inpeksaun','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/insp_list2.html', context)
        
        elif  stage == 'f':
            context = {'title': 'Lista Resibu Devolve husi UIVP','legend': 'Lista Resibu Devolve husi UIVP','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/insp_list2.html', context)
        
        elif  stage == 'g':
            context = {'title': 'Lista Sertifikasaun Pagamentu UIVP','legend': 'Lista Sertifikasaun Pagamentu UIVP','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/cert_pay_list.html', context)
        
@login_required   
@allowed_users(allowed_roles=['sigp_admin', 'sigp_dna', 'sigp_uivp', 'sigp_dnof', 'sigp_gabm', 'sigp_dgaf', 'sigp_min', 'sigp_op'])   
def rRecapInspProjList3(request, pcat, stage):
    objects = []
    
                
    if pcat == 'cd':
        if stage == 'a':
            objects=Contract.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3], status=1, is_complete='False').all().order_by('-project__id')
        elif stage == 'b':
            objects=Contract.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[6], status=1, is_complete='False').all().order_by('-project__id')
        elif stage == 'c':
            objects=Contract.objects.filter(project__capital__code__iexact=pcat, project__pcategory__code='LM', project__book_id__in=[2,3,6], status=1, is_complete='False').all().order_by('-project__id')  
        elif stage == 'd':
            # invoice Husi Projetu
            objects = InvTrack.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__is_lock='True', inv__is_ready='True').select_related('inv__cont__project','inv__cont__status','inv__cont__type').prefetch_related('inv__cont__contractcomp__company').order_by('-inv__cont__project__id')
        elif stage == 'e':
            # Prsosesu Inspeksaun Husi UIVP
            objects = InspTracks.objects.filter(insp__cont__project__capital__code__iexact=pcat,  insp__cont__project__pcategory__code='LM', insp__cont__project__book_id__in=[2,3,6], insp__cont__status=1, is_start='True', is_end='False').all().order_by('insp__cont__project__id')
        elif stage == 'f':
            # UIVP Devolve 
            pass
        elif stage == 'g':
            # UIVP Rekomenda pagamentu
            objects = CertPay.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', is_lock='True').all().order_by('inv__cont__project__id')
        elif stage == 'h':
            # Submete ba Gabinete Ministro
            objects = InvTrack.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', is_gab_in='True').all().order_by('inv__cont__project__id')
        elif stage == 'i':
            # Gabinete Ministro Aprova
            objects = InvTrack.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', is_gap_app='True').all().order_by('inv__cont__project__id')
        elif stage == 'j':
            # Submete ba DGAF
            objects = InvTrack.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', is_dgaf_in='True').all().order_by('inv__cont__project__id')
        elif stage == 'k':
            # Prosesu DGAF
            objects = InvTrack.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', is_dgaf_in='True', is_dnof_back_out='False').all().order_by('inv__cont__project__id')
        elif stage == 'l':
            # Pagamentu Final
            objects = InvTrack.objects.filter(inv__cont__project__capital__code__iexact=pcat, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', is_dgaf_in='True', is_dnof_back_out='True').all().order_by('inv__cont__project__id')
            
    if  pcat == 'cd':
        if stage == 'a' or stage == 'b' or stage == 'c':
            context = {'title': 'Lista Kontratu','legend': 'Lista Kontratu','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/cont_list2.html', context)
        
        elif  stage == 'd' or stage == 'h' or stage == 'i' or stage == 'j' or stage == 'k' or stage == 'l':
            context = {'title': 'Lista Resibu','legend': 'Lista Resibu','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/inv_list2.html', context)
        
        elif  stage == 'e':
            context = {'title': 'Lista Resibu ba Inpeksaun','legend': 'Lista Resibu ba Inpeksaun','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/insp_list2.html', context)
        
        elif  stage == 'f':
            context = {'title': 'Lista Resibu Devolve husi UIVP','legend': 'Lista Resibu Devolve husi UIVP','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/insp_list2.html', context)
        
        elif  stage == 'g':
            context = {'title': 'Lista Sertifikasaun Pagamentu UIVP','legend': 'Lista Sertifikasaun Pagamentu UIVP','objects': objects, 'pcat': pcat, 'stage': stage}
            return render(request, 'report_recap/cert_pay_list.html', context)
        
@login_required
@allowed_users(allowed_roles=['sigp_admin', 'sigp_dna', 'sigp_uivp', 'sigp_dnof', 'sigp_gabm', 'sigp_dgaf', 'sigp_min', 'sigp_op'])
def rRecapPayPortDet(request, pcat):
    # Get all programs (you can filter if needed)
    prog = Program.objects.filter(project__pcategory__code=pcat.upper()).distinct().order_by("code")
    current_year = date.today().year

    objects = []

    for obj in prog:
        # Ongoing Project Counts
        a = Contract.objects.filter(project__program=obj, project__pcategory__code=pcat.upper(), status_id__in=[1]).values('project').distinct().count()
        # Allocated budget
        b = Contract.objects.filter(project__program=obj, project__pcategory__code=pcat.upper(), status_id__in=[1]).exclude(project__alocate_bd=0).aggregate(total=Coalesce(Sum('project__alocate_bd'), Decimal('0.00')))['total']
       
        # Distinct project counts in payments
        c1 = Payment.objects.filter(contract__project__program=obj, contract__project__pcategory__code=pcat.upper(),contract__status_id__in=[1]).values('contract__project').distinct().count()
        c2 = PaymentFiscal.objects.filter(contract__project__program=obj, contract__project__pcategory__code=pcat.upper(), contract__status_id__in=[1]).values('contract__project').distinct().count()
        c = c1 + c2
        
        d = Invoice.objects.filter(cont__project__program=obj, cont__project__pcategory__code=pcat.upper(), cont__status_id__in=[1], is_paid=True).count()
        
        e1 = CertPay.objects.filter(inv__cont__project__program=obj, inv__cont__project__pcategory__code=pcat.upper(), inv__cont__status_id__in=[1]).aggregate(total=Coalesce(Sum('total'), Decimal('0.00')))['total']
        e2 = PayRecom.objects.filter(inv__cont__project__program=obj, inv__cont__project__pcategory__code=pcat.upper(), inv__cont__status_id__in=[1]).aggregate(total=Coalesce(Sum('amount'), Decimal('0.00')))['total']
        
        #e1 = Payment.objects.filter(contract__project__program=obj, contract__status_id__in=[1]).aggregate(total=Coalesce(Sum('total'), Decimal('0.00')))['total']
        #e2 = PaymentFiscal.objects.filter(contract__project__program=obj, contract__status_id__in=[1]).aggregate(total=Coalesce(Sum('com_amount'), Decimal('0.00')))['total']
       
        e = e1 + e2
        # Payment portal aggregation
        f = PaymentPortal.objects.filter(program=obj, pcategory__code=pcat.upper(), year__year=current_year).aggregate(total_amount=Coalesce(Sum('amount'), Decimal('0.00')),total_percent=Coalesce(Sum('percent'), Decimal('0.00')))

        total_amount = f['total_amount']
        total_percent = f['total_percent']
        
        g = Contract.objects.filter(project__program=obj, project__pcategory__code=pcat.upper(), status_id__in=[1]).exclude(total=0).aggregate(total=Coalesce(Sum('total'), Decimal('0.00')))['total']

        h = 0
        if g > 0 and e > 0:
            val = (e / g) * 100
            h = round(val, 2)

        objects.append({
            "code": obj.code if obj.code else "",
            "name": obj.name if obj.name else "",
            "a": a or 0,
            "b": b or Decimal('0.00'),
            "c": c or 0,
            "d": d or 0,
            "e": e or Decimal('0.00'),
            "h": h or 0,
            "total_amount": total_amount or Decimal('0.00'),
            "total_percent": total_percent or Decimal('0.00'),
        })

    obj_tot = {
        "a": 0,
        "b": Decimal('0.00'),
        "c": 0,
        "d": 0,
        "e": Decimal('0.00'),
        "h": 0,
        "total_amount": Decimal('0.00'),
        "total_percent": Decimal('0.00'),
    }

    for obj in objects:
        for key in obj_tot.keys():
            obj_tot[key] += obj.get(key, 0) or 0

    context = {
        'title': 'REKAPITULASAUN',
        'legend': 'REKAPITULASAUN',
        'objects': objects,
        'obj_tot': obj_tot,
        'pcat': pcat.upper(),
    }

    return render(request, 'report_recap/proj_det.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin', 'sigp_dna', 'sigp_uivp', 'sigp_dnof', 'sigp_gabm', 'sigp_dgaf', 'sigp_min', 'sigp_op'])
def rRecapPayProjOngDet(request, pcat, pro):
    prog = Program.objects.filter(code=pro).first()
    contracts = Contract.objects.filter(project__program__code=pro,project__pcategory__code=pcat.upper(), status_id__in=[1]).all()
    objects = []

    for cont in contracts:
        proj = cont.project
        comp = ContractComp.objects.filter(contract=cont).all()
        amd = Amendment.objects.get(contract=cont)
        pay = Payment.objects.filter(contract=cont).last()
      
        objects.append({
            "con":cont,
            "alocate_bd": proj.alocate_bd,
            "contract_amount": cont.total,
            "company": comp,
            "amendment": amd,
            "payment": pay,
        })

    # ---------- TOTALS ----------
    obj_tot = {
        "alocate_bd": Decimal('0.00'),
        "contract_amount": Decimal('0.00'),
        "progress_percent": Decimal('0.00'),
        "payment_total": Decimal('0.00'),
        "payment_percent": Decimal('0.00'),
        "balance": Decimal('0.00'),
        "balance_percent": Decimal('0.00'),
    }

    for item in objects:
        obj_tot["alocate_bd"] += item.get("alocate_bd", Decimal('0.00')) or Decimal('0.00')
        obj_tot["contract_amount"] += item.get("contract_amount", Decimal('0.00')) or Decimal('0.00')
        obj_tot["progress_percent"] += item.get("payment").phys_prog if item.get("payment") and item.get("payment").phys_prog else Decimal('0.00')
        obj_tot["payment_total"] += item.get("payment").com_amount if item.get("payment") and item.get("payment").com_amount else Decimal('0.00')
        obj_tot["payment_percent"] += item.get("payment").com_percent if item.get("payment") and item.get("payment").com_percent else Decimal('0.00')
        obj_tot["balance"] += (item.get("contract_amount", Decimal('0.00')) - (item.get("payment").com_amount if item.get("payment") and item.get("payment").com_amount else Decimal('0.00')))
        obj_tot["balance_percent"] += 100 - (item.get("payment").com_percent if item.get("payment") and item.get("payment").com_percent else Decimal('0.00'))   

    # ---------- CONTEXT ----------
    context = {
        'title': 'REKAPITULASAUN',
        'legend': 'REKAPITULASAUN',
        'objects': objects,
        'obj_tot': obj_tot,
        'pcat': pcat.upper(),
        'prog': prog,
    }

    return render(request, 'report_recap/proj_ong_det.html', context)








# @login_required
# @allowed_users(allowed_roles=['admin','dna','dna_s','dnof','dnof_s','dgaf','dgaf_s','dg','min','min_s','vice','vice_s','op','gab','uivp'])
# def rRecapCompProjSum(request):
#     group = request.user.groups.all()[0].name
#     statuss = StatusPlan.objects.all()
#     today = datetime.date.today()
#     thisyear = today.year
#     lastyear = thisyear-1
#     years = [thisyear,lastyear]
#     comps = ContractComp.objects.exclude(company__isnull=True).distinct().values('company').all()
#     objects,objects2 = [],[]
#     for i in comps:
#         comp = Company.objects.filter(id=i['company']).first()
#         tot_i_a = Contract.objects.filter(contractcomp__company=comp).all().count()
#         obj1_1,obj1_2 = [],[]
#         for ii in statuss:
#             tot_ii_a = Contract.objects.filter(contractcomp__company=comp, project__status=ii).all().count()
#             obj1_1.append([ii,tot_ii_a])
          
#         for ij in years:
#             ij_a = Contract.objects.filter(contractcomp__company=comp, start_date__year=ij).all().count()
#             obj1_2.append([ij,ij_a])
#         objects.append([comp,tot_i_a,obj1_1])   
#         objects2.append([comp,obj1_2])
    
#     context = {
#         'group': group, 'statuss': statuss, 'years': years, 'objects': objects, 'objects2': objects2,
#         'title': 'Sumariu Projetu Baseia Compania', 'legend': 'Sumariu Projetu Baseia Compania'
#     }
#     return render(request, 'report_comp/proj_sum.html', context)

                
            
        
        
        
        
        
        
        
        
@login_required
@allowed_users(allowed_roles=['admin','dna','uivp','dnof','gab','dgaf','min','op','uivp'])
def rRecapCapAllDet(request):
    group = request.user.groups.all()[0].name
    objects,objects1, objects2, objects3,objects4,objects5 = [],[],[],[],[],[]
    capi= Capital.objects.filter().all()
    stat = StatusImp.objects.exclude(id__in=[2,3,4]).order_by('-id').all()
    dgs = DG.objects.filter().all().order_by("-name")
    dv = Division.objects.filter().all().order_by("-name")
    pkat = PCat.objects.filter().all()
    yr   =Year.objects.filter().all().order_by('-year')

    date = datetime.date.today()
    a,b,c,d,e,f,g,h,i,j,k = 0,0,0,0,0,0,0,0,0,0,0
    a2,b2,c2,d2,e2,f2,g2,h2,i2 = 0,0,0,0,0,0,0,0,0
    a3,b3,c3,d3,e3,f3,g3,h3,i3 = 0,0,0,0,0,0,0,0,0
    a4,b4,c4,d4,e4,f4,g4,h4,i4 = 0,0,0,0,0,0,0,0,0
    a5,b5,c5,d5,e5,f5,g5,h5,i5 = 0,0,0,0,0,0,0,0,0

    for cap in capi:
        #1. Capital Start
        a = Project.objects.filter(capital=cap, statusproj_id=2).all().count()
        b = Project.objects.filter(capital=cap, statusproj_id=1).all().count()
        c = a+b

        d = Contract.objects.filter(project__capital=cap).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
        e = Payment.objects.filter(contract__project__capital=cap).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
        i = Payment.objects.filter(contract__project__capital=cap, date__year=date.year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
        j = PaymentFiscal.objects.filter(contract__project__capital=cap, year=date.year).exclude(com_amount=0).aggregate(Sum('com_amount')).get('total__sum', 0.00)
        if i != None:
            if j != None:
                k = float(i)+ float(j)
        if e:
            val = 100*(e/d)
            f = round((val),2)
            g = d-e
            h = round((g/d)*100,2)
        objects.append([cap,c,d,e,f,g,h,k])

        for st in stat:
            a2 = Contract.objects.filter(project__capital=cap, status__name=st.name).all().count()
            b2 = Contract.objects.filter(project__capital=cap, status__name=st.name).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
            c2 = Payment.objects.filter(contract__project__capital=cap, contract__status__name=st.name).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
            g2 = Payment.objects.filter(contract__project__capital=cap, contract__status__name=st.name,date__year=date.year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
            h2 = PaymentFiscal.objects.filter(contract__project__capital=cap, year=date.year).exclude(com_amount=0).aggregate(Sum('com_amount')).get('total__sum', 0.00)
            if g2 != None:
                if h2 != None:
                    i2= float(g2) + float(h2)
            if c2:
                val = 100*(c2/b2)
                d2 = round((val),2)
                e2 = b2-c2
                f2 = round((e2/b2)*100,2)
            if a2 !=0:
                objects1.append([cap,st.name,a2,b2,c2,d2,e2,f2,i2])
            # Capital End

            #2. Donu Projetu Start
            for dg in dgs:
                a3 = Contract.objects.filter(project__capital=cap, status__name=st.name, project__owner__dg__name=dg).all().count()
                b3 = Contract.objects.filter(project__capital=cap, status__name=st.name, project__owner__dg__name=dg).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
                c3 = Payment.objects.filter(contract__project__capital=cap, contract__status__name=st.name, contract__project__owner__dg__name=dg).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
                g3 = Payment.objects.filter(contract__project__capital=cap, contract__status__name=st.name, contract__project__owner__dg__name=dg, date__year=date.year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
                h3 = PaymentFiscal.objects.filter(contract__project__capital=cap, contract__status__name=st.name, contract__project__owner__dg__name=dg, year=date.year).exclude(com_amount=0).aggregate(Sum('com_amount')).get('com_amount__sum', 0.00)

                if g3 != None:
                    if h3 != None:
                        i3= float(g3) + float(h3)
                if c3:
                    val = 100*(c3/b3)
                    d3 = round((val),2)
                    e3 = b3-c3
                    f3 = round((e3/b3)*100,2)

                if a3 != 0:
                    objects3.append([cap,st.name,dg.code,dg.name,a3,b3,c3,d3,e3,f3,i3])
                    #2. Donu Projetu End

                #3. Karegoria MOP Start
                for pka in pkat:
                    for y in yr:
                        a5 = Contract.objects.filter(project__capital=cap, status__name=st.name, project__owner__dg=dg, project__pcat__name=pka.name, start_date__year=y.year).all().count()
                        b5 = Contract.objects.filter(project__capital=cap, status__name=st.name, project__owner__dg=dg, project__pcat__name=pka.name, start_date__year=y.year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
                        c5 = Payment.objects.filter(contract__project__capital=cap, contract__status__name=st.name, contract__project__owner__dg__name=dg, contract__project__pcat__name=pka.name, contract__start_date__year=y.year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
                        g5 = Payment.objects.filter(contract__project__capital=cap, contract__status__name=st.name, contract__project__owner__dg__name=dg, contract__start_date__year=y.year, date__year=date.year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
                        h5 = PaymentFiscal.objects.filter(contract__project__capital=cap, contract__status__name=st.name, contract__project__owner__dg__name=dg, contract__start_date__year=y.year, year=date.year).exclude(com_amount=0).aggregate(Sum('com_amount')).get('com_amount__sum', 0.00)
                        if g5 != None:
                            if h5 != None:
                                i5= float(g5) + float(h5)
                        if c5:
                            val = 100*(c5/b5)
                            d5 = round((val),2)
                            e5 = b5-c5
                            f5 = round((e5/b5)*100,2)
                        if a5 !=0:
                            objects5.append([cap,st.name,dg.code,dg.name,pka.code,pka.name,y.year,a5,b5,c5,d5,e5,f5,i5])

    #1. Total Capital Start
    objects_1 = []
    if objects: objects_1 = np.array(objects)
    tota = Project.objects.filter(statusproj_id=2).all().count()
    totb = Project.objects.filter(statusproj_id=1).all().count()
    totc = tota+totb

    totd=sum(filter(None, objects_1[:,2]))
    tote=sum(filter(None, objects_1[:,3]))
    totf=sum(filter(None, objects_1[:,4]))
    totg=sum(filter(None, objects_1[:,5]))
    toth=sum(filter(None, objects_1[:,6]))
    obj_tot = [totc,totd,tote,totf,totg,toth]
    #1. Total Capital End



    years = Project.objects.distinct().values('year__year').all().order_by('-year__year')
    context = {
        'group': group, 'years': years, 'date':date,'objects':objects, 'obj_tot':obj_tot, 'objects1':objects1,
        'objects2':objects2, 'objects3':objects3,'objects4':objects4,'objects5':objects5,
        'capi':capi,'dv':dv,
        'title': 'SUMARIO PROJETU TO ' + str(date.year) + 'KONTRATU IHA ONA', 'legend': 'SUMARIO PROJETU TO ' + str(y) + ' - KONTRATU IHA ONA'
    }
    return render(request, 'report_recap/cap_all_det.html', context)

@login_required
@allowed_users(allowed_roles=['admin','dna','uivp','dnof','gab','dgaf','min','op','uivp'])
def rRecapCapEachDet(request,pk):
    group = request.user.groups.all()[0].name
    objects,objects1, objects2, objects3,objects4,objects5 = [],[],[],[],[],[]
    code=pk.upper()
    capi = Capital.objects.filter(code=code)
    capi2= Capital.objects.filter().all()
    stat = StatusImp.objects.exclude(id__in=[2,3,4]).order_by('-id').all()
    cp1=Capital.objects.filter(pk=1)
    cp2=Capital.objects.filter(pk=2)
    cp3=Capital.objects.filter(pk=3)
    dgs = DG.objects.filter().all().order_by("-name")
    dv = Division.objects.filter().all().order_by("-name")
    pkat = PCat.objects.filter().all()
    yr   =Year.objects.filter().all().order_by('-year')

    date = datetime.date.today()
    a,b,c,d,e,f,g,h,i,j,k = 0,0,0,0,0,0,0,0,0,0,0
    a2,b2,c2,d2,e2,f2,g2,h2,i2 = 0,0,0,0,0,0,0,0,0
    a3,b3,c3,d3,e3,f3,g3,h3,i3 = 0,0,0,0,0,0,0,0,0
    a4,b4,c4,d4,e4,f4,g4,h4,i4 = 0,0,0,0,0,0,0,0,0
    a5,b5,c5,d5,e5,f5,g5,h5,i5 = 0,0,0,0,0,0,0,0,0

    for cap in capi:
        #1. Capital Start
        a = Project.objects.filter(capital=cap, statusproj_id=2).all().count()
        b = Project.objects.filter(capital=cap, statusproj_id=1).all().count()
        c = a+b

        d = Contract.objects.filter(project__capital=cap).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
        e = Payment.objects.filter(contract__project__capital=cap).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
        i = Payment.objects.filter(contract__project__capital=cap, date__year=date.year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
        j = PaymentFiscal.objects.filter(contract__project__capital=cap, year=date.year).exclude(com_amount=0).aggregate(Sum('com_amount')).get('total__sum', 0.00)
        if i != None:
            if j != None:
                k = float(i)+ float(j)
        if e:
            val = 100*(e/d)
            f = round((val),2)
            g = d-e
            h = round((g/d)*100,2)
        objects.append([cap,c,d,e,f,g,h,k])

        for st in stat:
            a2 = Contract.objects.filter(project__capital=cap, status__name=st.name).all().count()
            b2 = Contract.objects.filter(project__capital=cap, status__name=st.name).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
            c2 = Payment.objects.filter(contract__project__capital=cap, contract__status__name=st.name).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
            g2 = Payment.objects.filter(contract__project__capital=cap, contract__status__name=st.name,date__year=date.year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
            h2 = PaymentFiscal.objects.filter(contract__project__capital=cap, year=date.year).exclude(com_amount=0).aggregate(Sum('com_amount')).get('total__sum', 0.00)
            if g2 != None:
                if h2 != None:
                    i2= float(g2) + float(h2)
            if c2:
                val = 100*(c2/b2)
                d2 = round((val),2)
                e2 = b2-c2
                f2 = round((e2/b2)*100,2)
            if a2 !=0:
                objects1.append([cap,st.name,a2,b2,c2,d2,e2,f2,i2])
            # Capital End

            #2. Donu Projetu Start
            for dg in dgs:
                a3 = Contract.objects.filter(project__capital=cap, status__name=st.name, project__owner__dg=dg).all().count()
                b3 = Contract.objects.filter(project__capital=cap, status__name=st.name, project__owner__dg=dg).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
                c3 = Payment.objects.filter(contract__project__capital=cap, contract__status__name=st.name, contract__project__owner__dg__name=dg).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
                g3 = Payment.objects.filter(contract__project__capital=cap, contract__status__name=st.name, contract__project__owner__dg__name=dg, date__year=date.year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
                h3 = PaymentFiscal.objects.filter(contract__project__capital=cap, contract__status__name=st.name, contract__project__owner__dg__name=dg, year=date.year).exclude(com_amount=0).aggregate(Sum('com_amount')).get('com_amount__sum', 0.00)

                if g3 != None:
                    if h3 != None:
                        i3= float(g3) + float(h3)
                if c3:
                    val = 100*(c3/b3)
                    d3 = round((val),2)
                    e3 = b3-c3
                    f3 = round((e3/b3)*100,2)

                if a3 != 0:
                    objects3.append([cap,st.name,dg.code,dg.name,a3,b3,c3,d3,e3,f3,i3])
                    #2. Donu Projetu End

                #3. Karegoria MOP Start
                for pka in pkat:
                    for y in yr:
                        a5 = Contract.objects.filter(project__capital=cap, status__name=st.name, project__owner__dg__name=dg, project__pcat__name=pka.name, start_date__year=y.year).all().count()
                        b5 = Contract.objects.filter(project__capital=cap, status__name=st.name, project__owner__dg__name=dg, project__pcat__name=pka.name, start_date__year=y.year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
                        c5 = Payment.objects.filter(contract__project__capital=cap, contract__status__name=st.name, contract__project__owner__dg__name=dg, contract__project__pcat__name=pka.name, contract__start_date__year=y.year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
                        g5 = Payment.objects.filter(contract__project__capital=cap, contract__status__name=st.name, contract__project__owner__dg__name=dg, contract__start_date__year=y.year, date__year=date.year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
                        h5 = PaymentFiscal.objects.filter(contract__project__capital=cap, contract__status__name=st.name, contract__project__owner__dg__name=dg, contract__start_date__year=y.year, year=date.year).exclude(com_amount=0).aggregate(Sum('com_amount')).get('com_amount__sum', 0.00)
                        if g5 != None:
                            if h5 != None:
                                i5= float(g5) + float(h5)
                        if c5:
                            val = 100*(c5/b5)
                            d5 = round((val),2)
                            e5 = b5-c5
                            f5 = round((e5/b5)*100,2)
                        if a5 !=0:
                            objects5.append([cap,st.name,dg.code,dg.name,pka.code,pka.name,y.year,a5,b5,c5,d5,e5,f5,i5])

    #1. Total Capital Start
    objects_1 = []
    if objects: objects_1 = np.array(objects)
    tota = Project.objects.filter(statusproj_id=2).all().count()
    totb = Project.objects.filter(statusproj_id=1).all().count()
    totc = tota+totb

    totd=sum(filter(None, objects_1[:,2]))
    tote=sum(filter(None, objects_1[:,3]))
    totf=sum(filter(None, objects_1[:,4]))
    totg=sum(filter(None, objects_1[:,5]))
    toth=sum(filter(None, objects_1[:,6]))
    obj_tot = [totc,totd,tote,totf,totg,toth]
    #1. Total Capital End



    years = Project.objects.distinct().values('year__year').all().order_by('-year__year')
    context = {
        'group': group, 'years': years, 'date':date,'objects':objects, 'obj_tot':obj_tot, 'objects1':objects1,
        'objects2':objects2, 'objects3':objects3,'objects4':objects4,'objects5':objects5,
        'capi':capi,'capi2':capi2,'cp1':cp1,'cp2':cp2, 'cp3':cp3,'dv':dv,
        'title': 'SUMARIO PROJETU TO ' + str(date.year) + 'KONTRATU IHA ONA', 'legend': 'SUMARIO PROJETU TO ' + str(date.year) + ' - KONTRATU IHA ONA'
    }
    return render(request, 'report_recap/cap_each_det.html', context)

@login_required
@allowed_users(allowed_roles=['admin','dna','uivp','dnof','gab','dgaf','min','op','uivp'])
def rRecapYear(request, year):
    group = request.user.groups.all()[0].name
    objects = []

    capi = Capital.objects.filter().all()
    aa,bb,cc,dd,ee,ff,gg,hh = 0,0,0,0,0,0,0,0

    for cap in capi:
        aa = Project.objects.filter(capital=cap, statusproj_id=2, year__year__lte=year).all().count()
        bb = Project.objects.filter(capital=cap, statusproj_id=1, year__year__lte=year).all().count()
        cc = aa+bb

        dd = Contract.objects.filter(project__capital=cap, status__id=1, project__year__year__lte=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
        ee = Payment.objects.filter(contract__project__capital=cap, contract__project__status__id=1, contract__project__year__year__lte=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
        if ee:
            a = 100*(ee/dd)
            ff = round((a),2)
            gg = dd-ee
            hh = round((gg/dd)*100,2)
        objects.append([cap.code.lower, cap,cc,dd,ee,ff,gg,hh])
    objects2 = []
    if objects: objects2 = np.array(objects)
    tota = Project.objects.filter(statusproj_id=2, year__year__lte=year).all().count()
    totb = Project.objects.filter(statusproj_id=1, year__year__lte=year).all().count()
    totc = tota+totb

    totd=sum(filter(None, objects2[:,2]))
    tote=sum(filter(None, objects2[:,3]))
    totf=sum(filter(None, objects2[:,4]))
    totg=sum(filter(None, objects2[:,5]))
    toth=sum(filter(None, objects2[:,6]))
    obj_tot = [totc,totd,tote,totf,totg,toth]

    years = Project.objects.distinct().values('year__year').all().order_by('-year__year')
    context = {
        'group': group, 'years': years, 'objects':objects, 'obj_tot':obj_tot,
        'title': 'Rekapitulasaun', 'legend': 'Rekapitulasaun'
    }
    return render(request, 'report_recap/dash.html', context)



