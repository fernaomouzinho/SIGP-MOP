import numpy as np
import datetime
from django.shortcuts import render
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from conf.decorators import allowed_users
from django.db.models import Sum
from django.db.models.functions import Coalesce
from decimal import Decimal
from django.contrib.humanize.templatetags.humanize import intcomma
from project.models import Project,ProjectEst
from contract.models import Contract, ContractYear, ContractComp
from payment.models import Payment, PaymentFiscal,PaymentPortal
from custom.models import PCat, PCategory, StatusImp, StatusPlan, Capital, Division, Year, DG
from invoice.models import Invoice, CertPay,PayRecom, InvTrack, InvLet, InvLetAdnBack
from eval.models import Eval,EvalTrack,EvalFITrack,EvalLetAdnBack, EvalLetCNABack
from proc.models import Proc,ProcTrack,ProcReqTrack
from ver.models import VerTracks,Ver, VerSecEng, VerSecEngEmployee
from insp.models import InspTracks
from custom.models import Program
from company.models import Company

from datetime import date
from decimal import Decimal
import numpy as np
from django.db.models import Sum
from django.db.models.functions import Coalesce

   

def rRecapVericationADN(table):
    objects_1 = []
    objects_1_tot = []
    
    pcategory = table.objects.all()
    current_year = date.today().year

    for pcat in pcategory:
        a = ProjectEst.objects.filter(project__capital_id=3, project__pcategory=pcat, project__book_id__in=[2,3], project__statusproj_id=1, project__is_adn='True').values('project').distinct().count() 
        b = ProjectEst.objects.filter(project__capital_id=3, project__pcategory=pcat, project__book_id__in=[6], project__statusproj_id=1, project__is_adn='True').values('project').distinct().count()
        c = ProjectEst.objects.filter(project__capital_id=3, project__pcategory=pcat, project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True').values('project').distinct().count()
       
        if pcat.code == 'LM':
            # Total Dokumentu Submete ba UIVP
            d = VerTracks.objects.filter(ver__eval__proj__capital_id=3, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', is_start='True').values('ver__eval__proj').distinct().count()
            # Total Dokumentus Nebe Sei Iha Prosesu Verifikasaun UIVP
            e = VerTracks.objects.filter(ver__eval__proj__capital_id=3, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', ver__is_end='False', is_start='True', is_end='False').values('ver__eval__proj').distinct().count()
            # Total Dokumentus Devolve Husi UIVP
            # f = VerSecEng.objects.filter(ver__eval__proj__capital_id=3, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', ver__is_end='False', is_end='False', is_eng_back='True', is_eng_read='True', status='DEVOLVE').values('ver__eval__proj').distinct().count()
            # # Total Dokumentu Pasa iha Verifikasaun UIVP
            g = VerTracks.objects.filter(ver__eval__proj__capital_id=3, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', ver__is_end='True', is_start='True', is_end='True').values('ver__eval__proj').distinct().count()
            # Submisaun Dokumentu ba ADN
            h = EvalTrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='LM', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_uvip_out_1='True').values('eval__proj').distinct().count()
            # Projetu ne'ebe iha prosesu verifikaun ADN
            # i = EvalTrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='LM', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__is_adn='True', eval__is_end='False', is_ver_start='True', is_adn_in='False').values('eval__proj').distinct().count()
            # # Devolve Husi ADN
            j = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital_id=3, evallet__eval__proj__pcategory__code='LM',evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, is_result='False',is_return='True').values('evallet__eval__proj').distinct().count()
            # Rezultadu Verifikasaun ADN
            k = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital_id=3, evallet__eval__proj__pcategory__code='LM',evallet__eval__proj__book_id__in=[2,3,6],evallet__eval__proj__statusproj_id=1, is_result='True',is_return='False').values('evallet__eval__proj').distinct().count()
            # submete ba UIVP
            k1= EvalTrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='LM', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_adn_in='True').values('eval__proj').distinct().count()
            # Atualiza Estimatsaun ADN
            k2= EvalTrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_adn_in='True', eval__proj__projectest__adn__gt=0).values('eval__proj').distinct().count()
            # Submete ba GAbinete Ministro
            k3 = EvalTrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_gab_in='True', eval__proj__projectest__adn__gt=0).values('eval__proj').distinct().count()
            #Aprova TOR Husi GAB
            k4 = EvalTrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', eval__is_end='False', is_end='False', is_appr='True', eval__proj__projectest__adn__gt=0).values('eval__proj').distinct().count()
         
            
            l= int(0)
            m= int(0)
            # n= int(0)
            o= int(0)
            p= int(0)
            p1= int(0)
            p2= int(0)
            p3= int(0)
            
            
            # Submit ba DNA
            q = Proc.objects.filter(proj__capital_id=3, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='True', is_lock='True').values('proj').distinct().count()
            # Rekizasaun Tender DGAF
            r = Proc.objects.filter(proj__capital_id=3, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='True', is_req_start='True', is_req_end='False').values('proj').distinct().count()
            # Rezultadu tender DNA
            s = Proc.objects.filter(proj__capital_id=3, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='True', is_req_start='True', is_res_end='True').values('proj').distinct().count()   
            # Kontratu DNA
            t = Contract.objects.filter(project__capital_id=3, project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True', status_id__in=[7], is_complete='False').values('project').distinct().count()  
            
            # Montante Kontratu
            u =  Contract.objects.filter(project__capital_id=3, project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True', status_id__in=[7], total__lt=500000).values('project').distinct().count()  
            # Montante Kontratu Igual no mais 500,000
            v=  Contract.objects.filter(project__capital_id=3, project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True', status_id__in=[7], total__gte=500000).values('project').distinct().count()  
            
            
            
        elif pcat.code == 'FI': 
            # Total Dokumentu Submete ba UIVP
            d = VerTracks.objects.filter(ver__eval__proj__capital_id=3, ver__eval__proj__pcategory__code='FI', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', is_start='True').values('ver__eval__proj').distinct().count()
            # Total Dokumentus Nebe Sei Iha Prosesu Verifikasaun UIVP
            e = VerTracks.objects.filter(ver__eval__proj__capital_id=3, ver__eval__proj__pcategory__code='FI', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', ver__is_end='False', is_start='True', is_end='False').values('ver__eval__proj').distinct().count()
            # Total Dokumentus Devolve Husi UIVP
            # f = VerSecEng.objects.filter(ver__eval__proj__capital_id=3, ver__eval__proj__pcategory__code='FI', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', ver__is_end='False', is_end='False', is_eng_back='True', is_eng_read='True', status='DEVOLVE').values('ver__eval__proj').distinct().count()
            # # Total Dokumentu Pasa iha Verifikasaun UIVP
            g = VerTracks.objects.filter(ver__eval__proj__capital_id=3, ver__eval__proj__pcategory__code='FI', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='True', ver__is_end='True', is_start='True', is_end='True').values('ver__eval__proj').distinct().count()
            # Submisaun Dokumentu ba ADN
            h = EvalFITrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__is_adn='True', is_uvip_out_1='True').values('eval__proj').distinct().count()
            # Projetu ne'ebe iha prosesu verifikaun ADN
            # i = EvalFITrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__is_adn='True', eval__is_end='False', is_end='False', is_uvip_out_1='True', is_uvip_in_2='False').values('eval__proj').distinct().count()
            # # Devolve Husi ADN
            j = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital_id=3,evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, is_result='False',is_return='True').values('evallet__eval__proj').distinct().count() 
            # Rezultadu Verifikaun ADN
            k = EvalLetAdnBack.objects.filter(evallet__eval__proj__capital_id=3,evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, is_result='True',is_return='False').values('evallet__eval__proj').distinct().count()
            # submete ba UIVP
            k1= EvalFITrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_uvip_in_2='True').values('eval__proj').distinct().count()
            # Atualiza Estimatsaun ADN
            k2= EvalFITrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True',  is_uvip_in_2='True', eval__proj__projectest__adn__gt=0).values('eval__proj').distinct().count()
            #Submete ba Gabinete Ministro
            k3=EvalFITrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_gab_in_1='True', eval__proj__projectest__adn__gt=0).values('eval__proj').distinct().count()
            #Aprova Husi Gabinete Ministro
            k4=EvalFITrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_appr='True', eval__proj__projectest__adn__gt=0).values('eval__proj').distinct().count()
            # Submit ba KAFI
            l = EvalFITrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_appr='True', is_gab_out_1='True').values('eval__proj').distinct().count()
            # Submit ba cna
            m = EvalFITrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_appr='True',is_gab_out_3='True').values('eval__proj').distinct().count()
            # Process iha cna
            # n = EvalFITrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', eval__is_end='False', is_end='False', is_appr='True', is_gab_out_3='True', is_gab_in_4='False').values('eval__proj').distinct().count() 
            # # Kontratu devolve husi cna
            o = EvalLetCNABack.objects.filter(evallet__eval__proj__capital_id=3,evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1, is_result='False',is_return='True').values('evallet__eval__proj').distinct().count()
            # Kontratu produs husi cna
            p = EvalLetCNABack.objects.filter(evallet__eval__proj__capital_id=3,evallet__eval__proj__pcategory__code='FI', evallet__eval__proj__book_id__in=[2,3,6], evallet__eval__proj__statusproj_id=1,  is_result='True',is_return='False').values('evallet__eval__proj').distinct().count()
            
            # Submete ba GAB MINISTRO
            p1 = EvalFITrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_gab_in_4='True').values('eval__proj').distinct().count()
            
            # Aprova husi GAB MINISTRO
            p2 = EvalFITrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True', is_gab_sign='True').values('eval__proj').distinct().count()
            
            # UIVP Implementa
            p3 = EvalFITrack.objects.filter(eval__proj__capital_id=3, eval__proj__pcategory__code='FI', eval__proj__book_id__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='True',  is_uvip_out_5='True').values('eval__proj').distinct().count()
            
            
            q = int(0)
            r = int(0)
            s = int(0)
            t = int(0)
            # Montante Kontratu Menor 500,000
            u =  Contract.objects.filter(project__capital_id=3, project__pcategory__code='FI', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True', status_id__in=[7], total__lt=500000).values('project').distinct().count()  
            # Montante Kontratu Igual no mais 500,000
            v=  Contract.objects.filter(project__capital_id=3, project__pcategory__code='FI', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='True', status_id__in=[7], total__gte=500000).values('project').distinct().count()  
            
        
        objects_1.append({'pcat': pcat,'stages': {'a': a,'b': b,'c': c,'d': d,'e': e,'g': g,'h': h,'j': j,'k': k,'k1':k1,'k2':k2,'k3':k3,'k4':k4,'l': l,'m': m,'o': o,'p': p, 'p1':p1,'p2':p2,'p3':p3,'q': q,'r': r,'s': s,'t': t,'u': u,'v': v}})
   
        # Calculate totals for all stages without numpy
        stage_keys = ['a','b','c','d','e','g','h','j','k','k1','k2','k3','k4','l','m','o','p','p1','p2','p3','q','r','s','t','u','v']
        totals = {key: 0 for key in stage_keys}

        for obj in objects_1:
            for key, value in obj['stages'].items():
                totals[key] += value or 0  # safe in case value is None

        objects_1_tot = [ {'key': key, 'value': totals[key]} for key in stage_keys]
   
    

    return objects_1,objects_1_tot
def rRecapVericationINT(table):
    objects_2 = []
    objects_2_tot = []
    capital = table.objects.all().order_by('-id')
   
    #pcategory = table.objects.all()
    current_year = date.today().year

    for cap in capital:
        a = ProjectEst.objects.filter(project__capital=cap, project__pcategory__code='LM', project__book_id__in=[2,3], project__statusproj_id=1, project__is_adn='False').values('project').distinct().count()
        b = ProjectEst.objects.filter(project__capital=cap, project__pcategory__code='LM', project__book_id__in=[6], project__statusproj_id=1, project__is_adn='False').values('project').distinct().count()
        c = ProjectEst.objects.filter(project__capital=cap, project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='False').values('project').distinct().count()
        # Total Dokumentu Submete ba UIVP
        d = VerTracks.objects.filter(ver__eval__proj__capital_id=cap, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', is_start='True').values('ver__eval__proj').distinct().count()
        # Total Dokumentus Nebe Sei Iha Prosesu Verifikasaun UIVP
        e = VerSecEng.objects.filter(ver__eval__proj__capital_id=cap, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', ver__is_end='False',is_end='False').values('ver__eval__proj').distinct().count()
        # Total Dokumentus Devolve Husi UIVP
        # f = VerSecEng.objects.filter(ver__eval__proj__capital_id=cap, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', ver__is_end='False', is_end='False', is_eng_back='True', is_eng_read='True', status='DEVOLVE').values('ver__eval__proj').distinct().count()
        # # Total Dokumentu Pasa iha Verifikasaun UIVP
        g = VerSecEng.objects.filter(ver__eval__proj__capital_id=cap, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', ver__is_end='True', is_end='True', is_eng_back='True', is_eng_read='True', status='PASA').values('ver__eval__proj').distinct().count()
        # Total Dokumentus Submete Ba Gabinete Ministro
        h = EvalTrack.objects.filter(eval__proj__capital_id=cap, eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='False', eval__ver__is_end='True', is_gab_in='True').values('eval__proj').distinct().count()
        # Total Dokumentus Devolve Husi Gabinete Ministro
        i = EvalTrack.objects.filter(eval__proj__capital_id=cap, eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='False', eval__ver__is_end='True', is_gab_in='True', eval__is_appr='False', eval__is_return='True').values('eval__proj').distinct().count()
        # Total Dokumentus Aprovadu Husi Gabinete Ministro
        j = EvalTrack.objects.filter(eval__proj__capital_id=cap, eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__proj__is_adn='False', eval__ver__is_end='True', is_gab_in='True', eval__is_appr='True', eval__is_return='False').values('eval__proj').distinct().count()
        # Total Dokumentus Submete ba DNA
        k = Proc.objects.filter(proj__capital_id=cap, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='False',).values('proj').distinct().count()
        # Total Requisisaun iha prosesu ba DNA
        l = Proc.objects.filter(proj__capital_id=cap, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='False', is_req_start='True', is_req_end='False').values('proj').distinct().count()
        # Total Rezultadu Tender husi DNA
        m = Proc.objects.filter(proj__capital_id=cap, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, proj__is_adn='False', is_res_start='True', is_res_end='True').values('proj').distinct().count()
        # Total Kontratu Ba DNA ho status hein desizaun
        n = Contract.objects.filter(project__capital_id=cap, project__pcategory__code='LM', project__book_id__in=[2,3,6],  project__statusproj_id=1, project__is_adn='False', status_id__in=[7], is_complete='False').values('project').distinct().count()  
        # Montante Kontratu Menor 500,000
        o =  Contract.objects.filter(project__capital_id=cap, project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='False', status_id__in=[7], total__lt=500000).values('project').distinct().count()  
        # # Montante Kontratu Igual no mais 500,000 
        #p=  Contract.objects.filter(project__capital_id=cap, project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1, project__is_adn='False', status_id__in=[7], total__gte=500000).values('project').distinct().count()
       
        objects_2.append({'cap': cap,'stages': {'a': a,'b': b,'c': c,'d': d,'e': e,'g': g,'h': h,'i': i,'j': j,'k': k,'l': l,'m': m,'n': n,'o': o}})
        
        stage_keys = ['a','b','c','d','e','g','h','i','j','k','l','m','n','o']
        totals = {key: 0 for key in stage_keys}

        for obj in objects_2:
            for key, value in obj['stages'].items():
                totals[key] += value or 0  # safe in case value is None

        objects_2_tot = [ {'key': key, 'value': totals[key]} for key in stage_keys]
        
    return objects_2,objects_2_tot
def rRecapVericationADNINT(table):
    objects_22 = []
    objects_22_tot = []
    capital = table.objects.filter(code='CD').order_by('-id')
   
    #pcategory = table.objects.all()
    current_year = date.today().year

    for cap in capital:
        a = ProjectEst.objects.filter(project__capital=cap, project__pcategory__code='LM', project__book_id__in=[2,3], project__statusproj_id=1).values('project').distinct().count()
        b = ProjectEst.objects.filter(project__capital=cap, project__pcategory__code='LM', project__book_id__in=[6], project__statusproj_id=1).values('project').distinct().count()
        c = ProjectEst.objects.filter(project__capital=cap, project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1).values('project').distinct().count()
        # Total Dokumentu Submete ba UIVP
        d = VerTracks.objects.filter(ver__eval__proj__capital_id=cap, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, is_start='True').values('ver__eval__proj').distinct().count()
        # Total Dokumentus Nebe Sei Iha Prosesu Verifikasaun UIVP
        e = VerSecEng.objects.filter(ver__eval__proj__capital_id=cap, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__is_end='False',is_end='False').values('ver__eval__proj').distinct().count()
        # Total Dokumentus Devolve Husi UIVP
        # f = VerSecEng.objects.filter(ver__eval__proj__capital_id=cap, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1, ver__eval__proj__is_adn='False', ver__is_end='False', is_end='False', is_eng_back='True', is_eng_read='True', status='DEVOLVE').values('ver__eval__proj').distinct().count()
        # # Total Dokumentu Pasa iha Verifikasaun UIVP
        g = VerSecEng.objects.filter(ver__eval__proj__capital_id=cap, ver__eval__proj__pcategory__code='LM', ver__eval__proj__book__in=[2,3,6], ver__eval__proj__statusproj_id=1,  ver__is_end='True', is_end='True', is_eng_back='True', is_eng_read='True', status='PASA').values('ver__eval__proj').distinct().count()
        # Total Dokumentus Submete Ba Gabinete Ministro
        h = EvalTrack.objects.filter(eval__proj__capital_id=cap, eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__ver__is_end='True', is_gab_in='True').values('eval__proj').distinct().count()
        # Total Dokumentus Devolve Husi Gabinete Ministro
        i = EvalTrack.objects.filter(eval__proj__capital_id=cap, eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__ver__is_end='True', is_gab_in='True', eval__is_appr='False', eval__is_return='True').values('eval__proj').distinct().count()
        # Total Dokumentus Aprovadu Husi Gabinete Ministro
        j = EvalTrack.objects.filter(eval__proj__capital_id=cap, eval__proj__pcategory__code='LM', eval__proj__book__in=[2,3,6], eval__proj__statusproj_id=1, eval__ver__is_end='True', is_gab_in='True', eval__is_appr='True', eval__is_return='False').values('eval__proj').distinct().count()
        # Total Dokumentus Submete ba DNA
        k = Proc.objects.filter(proj__capital_id=cap, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1).values('proj').distinct().count()
        # Total Requisisaun iha prosesu ba DNA
        l = Proc.objects.filter(proj__capital_id=cap, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, is_req_start='True', is_req_end='False').values('proj').distinct().count()
        # Total Rezultadu Tender husi DNA
        m = Proc.objects.filter(proj__capital_id=cap, proj__pcategory__code='LM', proj__book_id__in=[2,3,6], proj__statusproj_id=1, is_res_start='True', is_res_end='True').values('proj').distinct().count()
        # Total Kontratu Ba DNA ho status hein desizaun
        n = Contract.objects.filter(project__capital_id=cap, project__pcategory__code='LM', project__book_id__in=[2,3,6],  project__statusproj_id=1, status_id__in=[7], is_complete='False').values('project').distinct().count()  
        # Montante Kontratu Menor 100,000
        o =  Contract.objects.filter(project__capital_id=cap, project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1, status_id__in=[7], total__lt=100000).values('project').distinct().count()  
        # # Montante Kontratu Igual no mais 100,000
        p=  Contract.objects.filter(project__capital_id=cap, project__pcategory__code='LM', project__book_id__in=[2,3,6], project__statusproj_id=1, status_id__in=[7], total__gte=100000).values('project').distinct().count()
       
        objects_22.append({'cap': cap,'stages': {'a': a,'b': b,'c': c,'d': d,'e': e,'g': g,'h': h,'i': i,'j': j,'k': k,'l': l,'m': m,'n': n,'o': o,'p': p}})
        
        stage_keys = ['a','b','c','d','e','g','h','i','j','k','l','m','n','o','p']
        totals = {key: 0 for key in stage_keys}

        for obj in objects_22:
            for key, value in obj['stages'].items():
                totals[key] += value or 0  # safe in case value is None

        objects_22_tot = [ {'key': key, 'value': totals[key]} for key in stage_keys]
        
    return objects_22,objects_22_tot



def rRecapInspectionADN(table):
    objects_3 = []
    objects_3_tot = []
   
    pcategory = table.objects.all()
    current_year = date.today().year

    for pcat in pcategory:
        a = Contract.objects.filter(project__capital_id=3, project__pcategory=pcat, project__book_id__in=[2,3], status=1, is_complete='False',project__is_adn='True').values('project').distinct().count()
        b = Contract.objects.filter(project__capital_id=3, project__pcategory=pcat, project__book_id__in=[6], status=1, is_complete='False',project__is_adn='True').values('project').distinct().count()
        c = Contract.objects.filter(project__capital_id=3, project__pcategory=pcat, project__book_id__in=[2,3,6], status=1, is_complete='False',project__is_adn='True').values('project').distinct().count()
      
        if pcat.code == 'LM':
            # Total Projetu husi Invoice
            d = InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', inv__is_lock='True', inv__is_ready='True').values('inv__cont__project').distinct().count()
            # Prosesu Inspeksaun UIVP
            e = InspTracks.objects.filter(insp__cont__project__capital_id=3, insp__cont__project__pcategory__code='LM', insp__cont__project__book_id__in=[2,3,6], insp__cont__status=1, insp__cont__is_complete='False', insp__cont__project__is_adn='True', is_start='True', is_end='False').values('insp__cont__project').distinct().count()
            # UIVP Devolve 
            f = 0
            #UIVP Rekomenda Pagamentu
            g = CertPay.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_lock='True').values('inv__cont__project').distinct().count()
            # Subemete ba ADN
            h = InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uvip_out_1='True').values('inv__cont__project').distinct().count()
            # Prosesu Inspeksaun ADN
            i = InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uvip_out_1='True', is_adn_in='False').values('inv__cont__project').distinct().count()
            # Devolve husi ADN
            j = InvLetAdnBack.objects.filter(invlet__inv__cont__project__capital_id=3, invlet__inv__cont__project__pcategory__code='LM', invlet__inv__cont__project__book_id__in=[2,3,6], invlet__inv__cont__status=1, invlet__inv__cont__is_complete='False', invlet__inv__cont__project__is_adn='True', is_return='True').values('invlet__inv__cont__project').distinct().count()
            # Rezultadu Inspeksaun ADN  
            k = PayRecom.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True').values('inv__cont__project').distinct().count()
            # Submete ba MOP-UIVP
            l = 0
            # Prosesu MOP-UIVP
            # m = 0
            # Certifika Pagamentu MOP-UIVP
            n = 0
            
            
            
            
            
            
            # Submite ba GAB Ministru
            o = InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_gab_in='True').values('inv__cont__project').distinct().count()
            # Gabinete Aprovadu
            p = InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_gap_app='True').values('inv__cont__project').distinct().count()
            # Submete ba DGAF
            q =InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True').values('inv__cont__project').distinct().count()
            # Prosesu DGAF
            r = InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True', is_dnof_back_out='False').values('inv__cont__project').distinct().count()
            # Pagamento Final
            s =InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True', is_dnof_back_out='True').values('inv__cont__project').distinct().count()
           
        elif pcat.code == 'FI':   
           # Total Projetu husi Invoice
            d = InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', inv__is_lock='True', inv__is_ready='True').values('inv__cont__project').distinct().count()
            # Prosesu Inspeksaun UIVP
            e = InspTracks.objects.filter(insp__cont__project__capital_id=3, insp__cont__project__pcategory__code='FI', insp__cont__project__book_id__in=[2,3,6], insp__cont__status=1, insp__cont__is_complete='False', insp__cont__project__is_adn='True', is_start='True', is_end='False').values('insp__cont__project').distinct().count()
            # UIVP Devolve 
            f = 0
            #UIVP Rekomenda Pagamentu
            g = CertPay.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_lock='True').values('inv__cont__project').distinct().count()
            # Subemete ba ADN
            h = InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uvip_out_1='True').values('inv__cont__project').distinct().count()
            # Prosesu Inspeksaun ADN
            i = InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_uvip_out_1='True', is_adn_in='False').values('inv__cont__project').distinct().count()
            # Devolve husi ADN
            j = InvLetAdnBack.objects.filter(invlet__inv__cont__project__capital_id=3, invlet__inv__cont__project__pcategory__code='FI', invlet__inv__cont__project__book_id__in=[2,3,6], invlet__inv__cont__status=1, invlet__inv__cont__is_complete='False', invlet__inv__cont__project__is_adn='True', is_return='True').values('invlet__inv__cont__project').distinct().count()
            # Rezultadu Inspeksaun ADN  
            k = PayRecom.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True').values('inv__cont__project').distinct().count()
            # Submete ba MOP-UIVP
            l = 0
            # Prosesu MOP-UIVP
            # m = 0
            # Certifika Pagamentu MOP-UIVP
            n = 0
            
            
            # Submite ba GAB Ministru
            o = InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_gab_in='True').values('inv__cont__project').distinct().count()
            # Gabinete Aprovadu
            p = InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_gap_app='True').values('inv__cont__project').distinct().count()
            # Submete ba DGAF
            q=InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True').values('inv__cont__project').distinct().count()
            # Prosesu DGAF
            r= InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True', is_dnof_back_out='False').values('inv__cont__project').distinct().count()
            # Pagamento Final
            s=InvTrack.objects.filter(inv__cont__project__capital_id=3, inv__cont__project__pcategory__code='FI', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='True', is_dgaf_in='True', is_dnof_back_out='True').values('inv__cont__project').distinct().count()
           
            
        objects_3.append({'cap': pcat,'stages': {'a': a,'b': b,'c': c, 'd':d, 'e':e,'f': f,'g': g,'h': h,'i': i,'j': j, 'k': k, 'l': l, 'n': n, 'o': o, 'p': p, 'p': p, 'q': q, 'r': r, 's': s}})   
        stage_keys = ['a','b','c','d','e','f','g','h','i','j','k','l','n','o','p','q','r','s']
        totals = {key: 0 for key in stage_keys}
        for obj in objects_3:
            for key, value in obj['stages'].items():
                totals[key] += value or 0  # safe in case value is None
        objects_3_tot = [ {'key': key, 'value': totals[key]} for key in stage_keys]
        
    return objects_3,objects_3_tot
def rRecapInspectionINT(table):
    objects_4 = []
    objects_4_tot = []
    capital = table.objects.all().order_by('-id')
   
    #pcategory = table.objects.all()
    current_year = date.today().year

    for cap in capital:
        a = Contract.objects.filter(project__capital=cap, project__pcategory__code='LM', project__book_id__in=[2,3], status=1, is_complete='False',project__is_adn='False').values('id').distinct().count()
        b = Contract.objects.filter(project__capital=cap, project__pcategory__code='LM', project__book_id__in=[6], status=1, is_complete='False',project__is_adn='False').values('id').distinct().count()
        c = Contract.objects.filter(project__capital=cap, project__pcategory__code='LM', project__book_id__in=[2,3,6], status=1, is_complete='False',project__is_adn='False').values('id').distinct().count()
        # Total Projetu husi Invoice
        d = InvTrack.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', inv__is_lock='True', inv__is_ready='True').values('inv__cont__project').distinct().count()
        # Prosesu Inspeksaun UIVP
        e = InspTracks.objects.filter(insp__cont__project__capital=cap, insp__cont__project__pcategory__code='LM', insp__cont__project__book_id__in=[2,3,6], insp__cont__status=1, insp__cont__is_complete='False', insp__cont__project__is_adn='False', is_start='True', is_end='False').values('insp__cont__project').distinct().count()
        # UIVP Devolve 
        f = 0
        #UIVP Rekomenda Pagamentu
        g = CertPay.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_lock='True').values('inv__cont__project').distinct().count()
        # Submite ba GAB Ministru
        h = InvTrack.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_gab_in='True').values('inv__cont__project').distinct().count()
        # Gabinete Aprovadu
        i = InvTrack.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_gap_app='True').values('inv__cont__project').distinct().count()
        # Submete ba DGAF
        j =InvTrack.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_dgaf_in='True').values('inv__cont__project').distinct().count()
        # Prosesu DGAF
        k = InvTrack.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_dgaf_in='True', is_dnof_back_out='False').values('inv__cont__project').distinct().count()
        # Pagamento Final
        l=InvTrack.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__cont__project__is_adn='False', is_dgaf_in='True', is_dnof_back_out='True').values('inv__cont__project').distinct().count()
        
    
        objects_4.append({'cap': cap,'stages': {'a': a,'b': b,'c': c, 'd':d,'e':e,'f': f,'g': g, 'h': h,'i': i,'j': j,'k': k,'l': l}})
        
        stage_keys = ['a','b','c','d','e','f','g','h','i','j','k','l']
        totals = {key: 0 for key in stage_keys}

        for obj in objects_4:
            for key, value in obj['stages'].items():
                totals[key] += value or 0  # safe in case value is None

        objects_4_tot = [ {'key': key, 'value': totals[key]} for key in stage_keys]
        
    
    return objects_4,objects_4_tot
def rRecapInspectionADNINT(table):
    objects_44 = []
    objects_44_tot = []
    capital = table.objects.filter(code="CD").order_by('-id')
   
    #pcategory = table.objects.all()
    current_year = date.today().year

    for cap in capital:
        a = Contract.objects.filter(project__capital=cap, project__pcategory__code='LM', project__book_id__in=[2,3], status=1, is_complete='False').values('id').distinct().count()
        b = Contract.objects.filter(project__capital=cap, project__pcategory__code='LM', project__book_id__in=[6], status=1, is_complete='False').values('id').distinct().count()
        c = Contract.objects.filter(project__capital=cap, project__pcategory__code='LM', project__book_id__in=[2,3,6], status=1, is_complete='False').values('id').distinct().count()
        # Total Projetu husi Invoice
        d = InvTrack.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', inv__is_lock='True', inv__is_ready='True').values('inv__cont__project').distinct().count()
        # Prosesu Inspeksaun UIVP
        e = InspTracks.objects.filter(insp__cont__project__capital=cap, insp__cont__project__pcategory__code='LM', insp__cont__project__book_id__in=[2,3,6], insp__cont__status=1, insp__cont__is_complete='False', is_start='True', is_end='False').values('insp__cont__project').distinct().count()
        # UIVP Devolve 
        f = 0
        #UIVP Rekomenda Pagamentu
        g = CertPay.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', is_lock='True').values('inv__cont__project').distinct().count()
        # Submite ba GAB Ministru
        h = InvTrack.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', is_gab_in='True').values('inv__cont__project').distinct().count()
        # Gabinete Aprovadu
        i = InvTrack.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', is_gap_app='True').values('inv__cont__project').distinct().count()
        # Submete ba DGAF
        j =InvTrack.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', is_dgaf_in='True').values('inv__cont__project').distinct().count()
        # Prosesu DGAF
        k = InvTrack.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', is_dgaf_in='True', is_dnof_back_out='False').values('inv__cont__project').distinct().count()
        # Pagamento Final
        l=InvTrack.objects.filter(inv__cont__project__capital=cap, inv__cont__project__pcategory__code='LM', inv__cont__project__book_id__in=[2,3,6], inv__cont__status=1, inv__cont__is_complete='False', is_dgaf_in='True', is_dnof_back_out='True').values('inv__cont__project').distinct().count()
        
    
        objects_44.append({'cap': cap,'stages': {'a': a,'b': b,'c': c, 'd':d,'e':e,'f': f,'g': g, 'h': h,'i': i,'j': j,'k': k,'l': l}})
        
        stage_keys = ['a','b','c','d','e','f','g','h','i','j','k','l']
        totals = {key: 0 for key in stage_keys}

        for obj in objects_44:
            for key, value in obj['stages'].items():
                totals[key] += value or 0  # safe in case value is None

        objects_44_tot = [ {'key': key, 'value': totals[key]} for key in stage_keys]
        
    
    return objects_44,objects_44_tot



def rRecapPortalPay(table):
    objects = []
    pcategory = table.objects.all()
    current_year = date.today().year

    for pcate in pcategory:
        prog = Program.objects.filter(project__pcategory=pcate).distinct().order_by("code")
    
        # Project counts
        a = Contract.objects.filter(project__pcategory=pcate, status_id__in=[1]).values('project').distinct().count()
        # Allocated budget
        b = Contract.objects.filter(project__pcategory=pcate, status_id__in=[1]).exclude(project__alocate_bd=0).aggregate(total=Coalesce(Sum('project__alocate_bd'), Decimal('0.00')))['total']
       
        # Distinct project counts in payments
        c1 = Payment.objects.filter(contract__project__pcategory=pcate,contract__status_id__in=[1]).values('contract__project').distinct().count()
        c2 = PaymentFiscal.objects.filter(contract__project__pcategory=pcate, contract__status_id__in=[1]).values('contract__project').distinct().count()
        c = c1 + c2
        
        
        
        d = Invoice.objects.filter(cont__project__pcategory=pcate, cont__status_id__in=[1], is_paid=True).count()
        
        e1 = CertPay.objects.filter(inv__cont__project__pcategory=pcate, inv__cont__status_id__in=[1]).aggregate(total=Coalesce(Sum('total'), Decimal('0.00')))['total']
        e2 = PayRecom.objects.filter(inv__cont__project__pcategory=pcate, inv__cont__status_id__in=[1]).aggregate(total=Coalesce(Sum('amount'), Decimal('0.00')))['total']
        #e1 = Payment.objects.filter(contract__project__pcategory=pcate, contract__status_id__in=[1]).aggregate(total=Coalesce(Sum('total'), Decimal('0.00')))['total']
        #e2 = PaymentFiscal.objects.filter(contract__project__pcategory=pcate, contract__status_id__in=[1]).aggregate(total=Coalesce(Sum('com_amount'), Decimal('0.00')))['total']
       
        e = e1 + e2
        
        # Payment portal aggregation
        total_amount = Decimal('0.00')
        total_percent = Decimal('0.00')
        for pr in prog:
            f = PaymentPortal.objects.filter(pcategory=pcate, program__code=pr.code,  year__year=current_year).aggregate(total_amount=Coalesce(Sum('amount'), Decimal('0.00')),total_percent=Coalesce(Sum('percent'), Decimal('0.00')))
        
            total_amount += f['total_amount']
            total_percent += f['total_percent']

        g = Contract.objects.filter(project__pcategory=pcate, status_id__in=[1]).exclude(total=0).aggregate(total=Coalesce(Sum('total'), Decimal('0.00')))['total']
        
        h = 0
        if g > 0 and e > 0:
            val = (e / g) * 100
            h = round(val, 2)

        objects.append({
            "code": pcate.code.lower() if pcate.code else "",
            "pcate": pcate,
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

    return objects, obj_tot

def rRecapCompImpProj(table):
    statuss = StatusPlan.objects.all()
    today = datetime.date.today()
    thisyear = today.year
    lastyear = thisyear-1
    years = [thisyear,lastyear]
    comps = table.objects.exclude(company__isnull=True).distinct().values('company').all()
    objects_5,objects_6 = [],[]
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
        objects_5.append([comp,tot_i_a,obj1_1])   
        objects_6.append([comp,obj1_2])            

    return objects_5, objects_6


