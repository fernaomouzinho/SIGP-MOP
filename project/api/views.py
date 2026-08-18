import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from custom.models import PCat, Year, PCategory, Capital, Sector
from project.models import Project, ProjectLoc


# class APIProjList(APIView):
#     authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         projs = Project.objects.filter(is_adn=True, is_end=False).all().order_by('year')
#         project = []
#         for i in projs:
#             cap,cat,fund,book,type,sector,status="","","","","","",""
#             if i.capital: cap = i.capital.name
#             if i.pcategory: cat = i.pcategory.name
#             if i.fund: fund = i.fund.name
#             if i.book: book = i.book.name
#             if i.ptype: type = i.ptype.name
#             if i.sector: sector = i.sector.name
#             if i.statusproj: status = i.statusproj.name
#             loc = ProjectLoc.objects.filter(project=i).first()
#             mun,post,vil,s_lat,s_lng,e_lat,e_lng="","","","","","",""
#             if loc.municipality: mun = loc.municipality.name
#             if loc.administrativepost: post = loc.administrativepost.name
#             if loc.village: vil = loc.village.name
#             if loc.start_lat: s_lat = loc.start_lat
#             if loc.start_lng: s_lng = loc.start_lng
#             if loc.end_lat: e_lat = loc.end_lat
#             if loc.end_lng: e_lng = loc.end_lng
#             project.append({'code':i.code, 'name':i.name, 'capital':cap, 'category':cat, 'sector':sector,\
#            'type':type, 'fund':fund, 'book':book, 'owner':i.owner.name, 'year': i.year.year, 'status_proj':status,\
#            'status':i.status.name, 'mun':mun, 'post':post, 'post':post, 'vil':vil, 's_lat':s_lat, 's_lng':s_lng, 'e_lat':e_lat, 'e_lng':e_lng,
#             })
#         data = { 'project': project, }
#         return Response(data)

class APIProjList(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        # ==========================================
        # 1. Check SSO authentication
        # ==========================================
        portal_user = getattr(request, "portal_user", None)

        if not portal_user:
            return Response(
                {"detail": "Authentication required."},
                status=401
            )

        # ==========================================
        # 2. Get projects
        # ==========================================
        projs = (
            Project.objects
            .filter(
                is_adn=True,
                is_end=False
            )
            .select_related(
                "capital",
                "pcategory",
                "fund",
                "book",
                "ptype",
                "sector",
                "statusproj",
                "status",
                "owner",
                "year",
            )
            .order_by("year")
        )

        projects = []

        # ==========================================
        # 3. Build project data
        # ==========================================
        for i in projs:

            loc = (
                ProjectLoc.objects
                .filter(project=i)
                .select_related(
                    "municipality",
                    "administrativepost",
                    "village",
                )
                .first()
            )

            projects.append({
                "code": i.code,
                "name": i.name,

                "capital": (
                    i.capital.name
                    if i.capital
                    else None
                ),

                "category": (
                    i.pcategory.name
                    if i.pcategory
                    else None
                ),

                "sector": (
                    i.sector.name
                    if i.sector
                    else None
                ),

                "type": (
                    i.ptype.name
                    if i.ptype
                    else None
                ),

                "fund": (
                    i.fund.name
                    if i.fund
                    else None
                ),

                "book": (
                    i.book.name
                    if i.book
                    else None
                ),

                "owner": (
                    i.owner.name
                    if i.owner
                    else None
                ),

                "year": (
                    i.year.year
                    if i.year
                    else None
                ),

                "status_proj": (
                    i.statusproj.name
                    if i.statusproj
                    else None
                ),

                "status": (
                    i.status.name
                    if i.status
                    else None
                ),

                # Location
                "mun": (
                    loc.municipality.name
                    if loc and loc.municipality
                    else None
                ),

                "post": (
                    loc.administrativepost.name
                    if loc and loc.administrativepost
                    else None
                ),

                "vil": (
                    loc.village.name
                    if loc and loc.village
                    else None
                ),

                "s_lat": (
                    loc.start_lat
                    if loc
                    else None
                ),

                "s_lng": (
                    loc.start_lng
                    if loc
                    else None
                ),

                "e_lat": (
                    loc.end_lat
                    if loc
                    else None
                ),

                "e_lng": (
                    loc.end_lng
                    if loc
                    else None
                ),
            })

        return Response({
            "project": projects
        })
        
        
# class APIProjYears(APIView):
#     authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, year, format=None):
#         projs = Project.objects.filter(is_adn=True, is_end=False, year__year=year).all().order_by('year')
#         project = []
#         for i in projs:
#             cap,cat,fund,book,type,sector,status="","","","","","",""
#             if i.capital: cap = i.capital.name
#             if i.pcategory: cat = i.pcategory.name
#             if i.fund: fund = i.fund.name
#             if i.book: book = i.book.name
#             if i.ptype: type = i.ptype.name
#             if i.sector: sector = i.sector.name
#             if i.statusproj: status = i.statusproj.name
#             loc = ProjectLoc.objects.filter(project=i).first()
#             mun,post,vil,s_lat,s_lng,e_lat,e_lng="","","","","","",""
#             if loc.municipality: mun = loc.municipality.name
#             if loc.administrativepost: post = loc.administrativepost.name
#             if loc.village: vil = loc.village.name
#             if loc.start_lat: s_lat = loc.start_lat
#             if loc.start_lng: s_lng = loc.start_lng
#             if loc.end_lat: e_lat = loc.end_lat
#             if loc.end_lng: e_lng = loc.end_lng
#             project.append({'code':i.code, 'name':i.name, 'capital':cap, 'category':cat, 'sector':sector,\
#            'type':type, 'fund':fund, 'book':book, 'owner':i.owner.name, 'year': i.year.year, 'status_proj':status,\
#            'status':i.status.name, 'mun':mun, 'post':post, 'post':post, 'vil':vil, 's_lat':s_lat, 's_lng':s_lng, 'e_lat':e_lat, 'e_lng':e_lng,
#             })
#         data = { 'project': project, }
#         return Response(data)

class APIProjYears(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, year, format=None):

        # ==========================================
        # 1. Check SSO authentication
        # ==========================================
        portal_user = getattr(request, "portal_user", None)

        if not portal_user:
            return Response(
                {"detail": "Authentication required."},
                status=401
            )

        # ==========================================
        # 2. Get projects by year
        # ==========================================
        projs = (
            Project.objects
            .filter(
                is_adn=True,
                is_end=False,
                year__year=year
            )
            .select_related(
                "capital",
                "pcategory",
                "fund",
                "book",
                "ptype",
                "sector",
                "statusproj",
                "status",
                "owner",
                "year",
            )
            .order_by("year")
        )

        projects = []

        # ==========================================
        # 3. Build project response
        # ==========================================
        for i in projs:

            loc = (
                ProjectLoc.objects
                .filter(project=i)
                .select_related(
                    "municipality",
                    "administrativepost",
                    "village"
                )
                .first()
            )

            projects.append({

                "code": i.code,

                "name": i.name,

                "capital": (
                    i.capital.name
                    if i.capital
                    else None
                ),

                "category": (
                    i.pcategory.name
                    if i.pcategory
                    else None
                ),

                "sector": (
                    i.sector.name
                    if i.sector
                    else None
                ),

                "type": (
                    i.ptype.name
                    if i.ptype
                    else None
                ),

                "fund": (
                    i.fund.name
                    if i.fund
                    else None
                ),

                "book": (
                    i.book.name
                    if i.book
                    else None
                ),

                "owner": (
                    i.owner.name
                    if i.owner
                    else None
                ),

                "year": (
                    i.year.year
                    if i.year
                    else None
                ),

                "status_proj": (
                    i.statusproj.name
                    if i.statusproj
                    else None
                ),

                "status": (
                    i.status.name
                    if i.status
                    else None
                ),

                # ==================================
                # Location
                # ==================================
                "mun": (
                    loc.municipality.name
                    if loc and loc.municipality
                    else None
                ),

                "post": (
                    loc.administrativepost.name
                    if loc and loc.administrativepost
                    else None
                ),

                "vil": (
                    loc.village.name
                    if loc and loc.village
                    else None
                ),

                "s_lat": (
                    loc.start_lat
                    if loc
                    else None
                ),

                "s_lng": (
                    loc.start_lng
                    if loc
                    else None
                ),

                "e_lat": (
                    loc.end_lat
                    if loc
                    else None
                ),

                "e_lng": (
                    loc.end_lng
                    if loc
                    else None
                ),
            })

        return Response({
            "project": projects
        })
###
class APIPortalHome(APIView):
    def get(self, request, format=None):
        year = datetime.datetime.today().year
        obj = []
        obj1 = Project.objects.filter(statusproj_id=1, year__year=year).all().count()
        obj2 = Project.objects.filter(statusproj_id=2).all().count()
        obj3 = Project.objects.filter(status_id=2).all().count()
        obj4 = Project.objects.filter(status_id=4).all().count()
        obj5 = Project.objects.filter(status_id=1).all().count()
        obj = [obj1,obj2,obj3,obj4,obj5]
        data = { 'year': year, 'obj': obj, }
        return Response(data)

class APIPPortalMOpCat(APIView):
    def get(self, request, format=None):
        objects = PCat.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(pcat=i).all().count()
            obj.append(a)
            label.append(i.code)
        data = { 'label': label, 'obj': obj, }
        return Response(data)

class APIPPortalProjCat(APIView):
    def get(self, request, format=None):
        objects = PCategory.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(pcategory=i).all().count()
            obj.append(a)
            label.append(i.code)
        data = { 'label': label, 'obj': obj, }
        return Response(data)

class APIPPortalProjCap(APIView):
    def get(self, request, format=None):
        objects = Capital.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(capital=i).all().count()
            obj.append(a)
            label.append(i.code)
        data = { 'label': label, 'obj': obj, }
        return Response(data)

class APIPPortalProjSec(APIView):
    def get(self, request, format=None):
        objects = Sector.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(sector=i).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, }
        return Response(data)
