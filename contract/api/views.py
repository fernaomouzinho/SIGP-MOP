import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, Sum
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from project.models import Project, ProjectLoc, ProjectEst, ProjectEst,ProjectImg
from contract.models import Contract, ContractComp, Amendment
from company.models import CompUser
from payment.models import Payment, PaymentFiscal, PaymentHist, PhysicalProgress
from django.conf import settings
from users.decorators import allowed_users
from sigp.utils import get_roles

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


# class APIPortalContList(APIView):
#     authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         user = request.user
#         is_admin = user.is_superuser or user.groups.filter(name='admin').exists()
        

#         if is_admin:
#             conts = Contract.objects.filter(is_complete=False).order_by('-start_date')
#             print('All conts',conts)
#         else:
#             try:
#                 comp_user = CompUser.objects.get(user=user)
#                 company = comp_user.comp
#             except CompUser.DoesNotExist:
#                 return Response(
#                     {"error": "User has no company assigned"},
#                     status=400
#                 )

#             conts = (Contract.objects.filter(is_complete=False, contractcomp__company=company)
#                      .order_by('-start_date')
#                      .distinct())

#         objects = []
#         for i in conts:
#             proj = i.project
#             statusp = proj.statusproj.code if proj.statusproj else ""
#             pcategory = proj.pcategory.code if proj.pcategory else ""
#             cat = proj.pcat.code if proj.pcat else ""
#             status = proj.status.name if proj.status else ""
#             amend = Amendment.objects.filter(contract=i).first()
#             comps = ContractComp.objects.filter(contract=i).all()
#             physicalprog = PhysicalProgress.objects.filter(contract=i).order_by('-id').first()
#             if physicalprog:
#                 latest_prog_percent = physicalprog.prog_percent
#             else:
#                 latest_prog_percent = None

#             comp = []
#             if comps:
#                 for j in comps: 
#                     if j.company:
#                         comp.append([j.company.name])

#             projloc = ProjectLoc.objects.filter(project=proj).first()
#             if projloc and projloc.municipality:
#                 municipality_name = projloc.municipality.name
#                 startlat = projloc.start_lat
#                 startlng = projloc.start_lng
#                 endlat = projloc.end_lat
#                 endlng = projloc.end_lng
#             else:
#                 municipality_name = "N/A"
#                 startlat = ""
#                 startlng = ""
#                 endlat = ""
#                 endlng = ""

#             # 🔹 Load all images related to this project
#             proj_images = ProjectImg.objects.filter(project=proj).all()
#             image_urls = []
#             for img in proj_images:
#                 if img.image:
#                     image_urls.append(f"{settings.MEDIA_DOMAIN}{img.image.url}")

#             objects.append({
#                 "statusp": statusp,
#                 "code": proj.code,
#                 "name": proj.name,
#                 "cat": cat,
#                 "year": proj.year.year if proj.year else None,
#                 "status": status,
#                 "cont_number": amend.number if amend else None,
#                 "amount": amend.total if amend else None,
#                 "start_date": i.start_date,
#                 "end_date": amend.end_date if amend else None,
#                 "comp": comp,
#                 "pcategory": pcategory,
#                 "latest_prog_percent": latest_prog_percent,
#                 "municipality": municipality_name,
#                 "post": projloc.administrativepost.name if projloc and projloc.administrativepost else "N/A",
#                 "village": projloc.village.name if projloc and projloc.village else "N/A",
#                 "aldeia": projloc.aldeia.name if projloc and projloc.aldeia else "N/A",
#                 "start_lat": startlat,
#                 "start_lng": startlng,
#                 "end_lat": endlat,
#                 "end_lng": endlng,
#                 "owner": proj.owner.name if proj.owner else "N/A",
#                 "images": image_urls,   # 
#             })

#         return Response({"objects": objects})

@method_decorator(
    allowed_users(
        allowed_roles=[
            'sigp_admin',
            'sigp_dna',
            'sigp_dna_s',
            'sigp_op',
            'sigp_uivp',
        ]
    ),
    name='dispatch'
)
class APIPortalContList(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        # ==========================================
        # 1. SSO USER / ROLES
        # ==========================================
        roles = get_roles(request)

        user_id = request.user.id
        username = request.user.username

        is_admin = 'sigp_admin' in roles

        # ==========================================
        # 2. ADMIN: SEE ALL CONTRACTS
        # ==========================================
        if is_admin:

            conts = (
                Contract.objects
                .filter(is_complete=False)
                .order_by('-start_date')
            )

        # ==========================================
        # 3. NON ADMIN: SEE COMPANY CONTRACTS ONLY
        # ==========================================
        else:

            comp_user = (
                CompUser.objects
                .select_related('comp')
                .filter(user_id=user_id)
                .first()
            )

            if not comp_user:
                return Response(
                    {
                        "error": "User has no company assigned",
                        "username": username,
                    },
                    status=400
                )

            company = comp_user.comp

            conts = (
                Contract.objects
                .filter(
                    is_complete=False,
                    contractcomp__company=company
                )
                .order_by('-start_date')
                .distinct()
            )

        # ==========================================
        # 4. BUILD API RESPONSE
        # ==========================================
        objects = []

        for i in conts:

            proj = i.project

            statusp = (
                proj.statusproj.code
                if proj.statusproj else ""
            )

            pcategory = (
                proj.pcategory.code
                if proj.pcategory else ""
            )

            cat = (
                proj.pcat.code
                if proj.pcat else ""
            )

            status_name = (
                proj.status.name
                if proj.status else ""
            )

            # Amendment
            amend = (
                Amendment.objects
                .filter(contract=i)
                .first()
            )

            # Companies
            comps = (
                ContractComp.objects
                .filter(contract=i)
            )

            comp = []

            for j in comps:
                if j.company:
                    comp.append([j.company.name])

            # Physical progress
            physicalprog = (
                PhysicalProgress.objects
                .filter(contract=i)
                .order_by('-id')
                .first()
            )

            latest_prog_percent = (
                physicalprog.prog_percent
                if physicalprog else None
            )

            # ======================================
            # Location
            # ======================================
            projloc = (
                ProjectLoc.objects
                .filter(project=proj)
                .first()
            )

            if projloc:
                municipality_name = (
                    projloc.municipality.name
                    if projloc.municipality else "N/A"
                )

                post_name = (
                    projloc.administrativepost.name
                    if projloc.administrativepost else "N/A"
                )

                village_name = (
                    projloc.village.name
                    if projloc.village else "N/A"
                )

                aldeia_name = (
                    projloc.aldeia.name
                    if projloc.aldeia else "N/A"
                )

                startlat = projloc.start_lat or ""
                startlng = projloc.start_lng or ""
                endlat = projloc.end_lat or ""
                endlng = projloc.end_lng or ""

            else:
                municipality_name = "N/A"
                post_name = "N/A"
                village_name = "N/A"
                aldeia_name = "N/A"

                startlat = ""
                startlng = ""
                endlat = ""
                endlng = ""

            # ======================================
            # Project images
            # ======================================
            proj_images = ProjectImg.objects.filter(
                project=proj
            )

            image_urls = []

            for img in proj_images:
                if img.image:
                    image_urls.append(
                        f"{settings.MEDIA_DOMAIN}{img.image.url}"
                    )

            # ======================================
            # Response object
            # ======================================
            objects.append({
                "statusp": statusp,
                "code": proj.code,
                "name": proj.name,
                "cat": cat,

                "year": (
                    proj.year.year
                    if proj.year else None
                ),

                "status": status_name,

                "cont_number": (
                    amend.number
                    if amend else None
                ),

                "amount": (
                    amend.total
                    if amend else None
                ),

                "start_date": i.start_date,

                "end_date": (
                    amend.end_date
                    if amend else None
                ),

                "comp": comp,

                "pcategory": pcategory,

                "latest_prog_percent":
                    latest_prog_percent,

                "municipality":
                    municipality_name,

                "post":
                    post_name,

                "village":
                    village_name,

                "aldeia":
                    aldeia_name,

                "start_lat":
                    startlat,

                "start_lng":
                    startlng,

                "end_lat":
                    endlat,

                "end_lng":
                    endlng,

                "owner": (
                    proj.owner.name
                    if proj.owner else "N/A"
                ),

                "images":
                    image_urls,
            })

        return Response({
            "objects": objects
        })


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
