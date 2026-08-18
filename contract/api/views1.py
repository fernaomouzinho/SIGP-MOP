import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, Sum
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from contract.models import Contract, ContractComp, Amendment
from company.models import CompUser

# class APIPortalContList(APIView):
#     authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         conts = Contract.objects.filter(is_complete=False).all().order_by('-start_date')
#         objects = []
#         for i in conts:
#             statusp,pcategory,cat,status,comp="","","","",""
#             proj = i.project
#             if proj.statusproj: statusp = proj.statusproj.code
#             if proj.pcategory: pcategory = proj.pcategory.code
#             if proj.pcat: cat = proj.pcat.code
#             if proj.status: status = proj.status.name

#             amend = Amendment.objects.filter(contract=i).first()
#             comps = ContractComp.objects.filter(contract=i).all()
#             comp = []
#             if comps:
#                 for j in comps: 
#                     if j.company: comp.append([j.company.name])
#             objects.append({'statusp':statusp, 'code':proj.code, 'name':proj.name, 'cat':cat, 'year': proj.year.year, 'status':status,\
#                    'cont_number':amend.number, 'amount':amend.total, 'start_date':i.start_date, 'end_date':amend.end_date, 'comp':comp, 'pcategory':pcategory,
#             })
#         data = { 'objects': objects, }
#         return Response(data)

class APIPortalContList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        is_admin = user.is_superuser or user.groups.filter(name='admin').exists()
       
        if is_admin:
            # Admin sees all incomplete contracts
            conts = Contract.objects.filter(is_complete=False).order_by('-start_date')
            return Response({"contracts": conts.values("id", "start_date")})
           
            
        else:
            # Normal user → filter by their company
            try:
                comp_user = CompUser.objects.get(user=user)
                company = comp_user.comp
            except CompUser.DoesNotExist:
                return Response(
                    {"error": "User has no company assigned"},
                    status=400
                )

            conts = (
                Contract.objects.filter(is_complete=False, contractcomp__company=company)
                .order_by('-start_date')
                .distinct()
            )

        objects = []
        for i in conts:
            proj = i.project

            # Safe attribute lookups
            statusp = proj.statusproj.code if proj.statusproj else ""
            pcategory = proj.pcategory.code if proj.pcategory else ""
            cat = proj.pcat.code if proj.pcat else ""
            status = proj.status.name if proj.status else ""

            amend = Amendment.objects.filter(contract=i).first()
            comps = list(ContractComp.objects.filter(contract=i).values_list("company__name", flat=True))

            objects.append({
                "statusp": statusp,
                "code": proj.code,
                "name": proj.name,
                "cat": cat,
                "year": proj.year.year if proj.year else None,
                "status": status,
                "cont_number": amend.number if amend else None,
                "amount": amend.total if amend else None,
                "start_date": i.start_date,
                "end_date": amend.end_date if amend else None,
                "comp": comps,   
                "pcategory": pcategory,
            })

        return Response({"objects": objects})

class APIPortalContHist(APIView):
    def get(self, request, format=None):
        conts = Contract.objects.filter(is_complete=True).all().order_by('-start_date')
        objects = []
        for i in conts:
            statusp,cat,status,comp="","","",""
            proj = i.project
            if proj.statusproj: statusp = proj.statusproj.code
            if proj.pcategory: cat = proj.pcategory.code
            if proj.status: status = proj.status.name

            amend = Amendment.objects.filter(contract=i).first()
            comps = ContractComp.objects.filter(contract=i).all()
            comp = []
            if comps:
                for j in comps:
                    if j.company: comp.append([j.company.name])
            objects.append({'statusp':statusp, 'code':proj.code, 'name':proj.name, 'cat':cat, 'year': proj.year.year, 'status':status,\
                   'cont_number':amend.number, 'amount':amend.total, 'start_date':i.start_date, 'end_date':amend.end_date, 'comp':comp, 
            })
        data = { 'objects': objects, }
        return Response(data)
