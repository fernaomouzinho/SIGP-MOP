from django.shortcuts import get_object_or_404
from django.db.models import Sum
from requests import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from custom.models import Division, PCat, StatusPlan, StatusImp, PCategory, Sector, StatusProj, Year, Municipality, Capital
from project.models import Project, ProjectLoc
from contract.models import Contract
from company.models import Company
from payment.models import Payment
from conf.utils import f_monthname_tet
from django.utils.decorators import method_decorator
from users.decorators import allowed_users
from sigp.utils import get_roles

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIProjStatus(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        group = get_roles(request)
        objects = StatusProj.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(statusproj=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIProjStatusYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, year, format=None):
        group = get_roles(request)
        objects = StatusProj.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(statusproj=i, year__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPlanStatus(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        group = get_roles(request)
        objects = StatusPlan.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(status=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPlanStatusYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, year, format=None):
        group = get_roles(request)
        objects = StatusPlan.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(status=i, year__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIImpStatus(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        group = get_roles(request)
        objects = StatusImp.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Contract.objects.filter(status=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIImpStatusYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, year, format=None):
        group = get_roles(request)
        objects = StatusImp.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Contract.objects.filter(status=i, start_date__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPMopCat(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        group = get_roles(request)
        objects = PCat.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(pcat=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.code)
        data = { 'label': label, 'obj': obj, }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPMopCatYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, year, format=None):
        group = get_roles(request)
        objects = PCat.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(pcat=i, year__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.code)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPCat(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        group = get_roles(request)
        objects = PCategory.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(pcategory=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.code)
        data = { 'label': label, 'obj': obj, }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPCatYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, year, format=None):
        group = get_roles(request)
        objects = PCategory.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(pcategory=i, year__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.code)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPSec(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        group = get_roles(request)
        objects = Sector.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(sector=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPSecYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, year, format=None):
        group = get_roles(request)
        objects = Sector.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(sector=i, year__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPCap(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        group = get_roles(request)
        objects = Capital.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(capital=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.code)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPCapYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, year, format=None):
        group = get_roles(request)
        objects = Capital.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(capital=i, year__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.code)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPMun(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        group = get_roles(request)
        objects = Municipality.objects.all()
        label,obj,id = list(),list(),list()
        for i in objects:
            a = ProjectLoc.objects.filter(municipality=i).all().count()
            obj.append(a)
            label.append(i.name)
            id.append(i.id)
        data = { 'label': label, 'obj': obj, 'id': id, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPMunYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, year, format=None):
        group = get_roles(request)
        objects = Municipality.objects.all()
        label,obj = list(),list()
        for i in objects:
            a = ProjectLoc.objects.filter(municipality=i, project__year__year=year).all().count()
            obj.append(a)
            label.append(i.code)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        group = get_roles(request)
        objects = Year.objects.all().order_by('year')
        label,obj1,obj2 = list(),list(),list()
        for i in objects:
            a = Project.objects.filter(year=i, is_active=True).all().count()
            b = Contract.objects.filter(start_date__year=i.year).all().count()
            obj1.append(a)
            obj2.append(b)
            label.append(i.year)
        data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'group': group }
        return Response(data)
###
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPayMonthly(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        group = get_roles(request)
        label,obj = list(),list()
        for i in range(1,13):
            mname = f_monthname_tet(int(i))
            a = Payment.objects.filter(date__month=i).aggregate(Sum('total')).get('total__sum', 0.00)
            tot = 0
            if a: tot = a
            obj.append(tot)
            label.append(mname)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class APIPayMonthlyY(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, year, format=None):
        group = get_roles(request)
        label,obj = list(),list()
        for i in range(1,13):
            mname = f_monthname_tet(int(i))
            a = Payment.objects.filter(date__year=year, date__month=i).aggregate(Sum('total')).get('total__sum', 0.00)
            tot = 0
            if a: tot = a
            obj.append(tot)
            label.append(mname)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
######################################################
######################################################
######################################################
### DIV

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIProjStatus(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = StatusProj.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(owner=div, statusproj=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIProjStatusYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, year, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = StatusProj.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(owner=div, statusproj=i, year__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPlanStatus(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = StatusPlan.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(owner=div, status=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPlanStatusYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, year, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = StatusPlan.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(owner=div, status=i, year__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIImpStatus(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = StatusImp.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Contract.objects.filter(project__owner=div, status=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIImpStatusYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, year, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = StatusImp.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Contract.objects.filter(project__owner=div, status=i, start_date__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPMopCat(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk,format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = PCat.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(owner=div, pcat=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPMopCatYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, year, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = PCat.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(owner=div, pcat=i, year__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPCat(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk,format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = PCategory.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(owner=div, pcategory=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPCatYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, year, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = PCategory.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(owner=div, pcategory=i, year__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPSec(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = Sector.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(owner=div, sector=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPSecYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, year, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = Sector.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(owner=div, sector=i, year__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPCap(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = Capital.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(owner=div, capital=i, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPCapYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, year, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = Capital.objects.all().order_by('id')
        label,obj = list(),list()
        for i in objects:
            a = Project.objects.filter(owner=div, capital=i, year__year=year, is_active=True).all().count()
            obj.append(a)
            label.append(i.name)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPMun(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = Municipality.objects.all()
        label,obj = list(),list()
        for i in objects:
            a = ProjectLoc.objects.filter(project__owner=div, municipality=i).all().count()
            obj.append(a)
            label.append(i.code)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPMunYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, year, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = Municipality.objects.all()
        label,obj = list(),list()
        for i in objects:
            a = ProjectLoc.objects.filter(project__owner=div, municipality=i, project__year__year=year).all().count()
            obj.append(a)
            label.append(i.code)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
#
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPYear(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        objects = Year.objects.all().order_by('year')
        label,obj1,obj2 = list(),list(),list()
        for i in objects:
            a = Project.objects.filter(owner=div, year=i, is_active=True).all().count()
            b = Contract.objects.filter(project__owner=div, start_date__year=i.year).all().count()
            obj1.append(a)
            obj2.append(b)
            label.append(i.year)
        data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'group': group }
        return Response(data)
###
@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPayMonthly(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        label,obj = list(),list()
        for i in range(1,13):
            mname = f_monthname_tet(int(i))
            a = Payment.objects.filter(project__owner=div, date__month=i).aggregate(Sum('total')).get('total__sum', 0.00)
            tot = 0
            if a: tot = a
            obj.append(tot)
            label.append(mname)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)

@method_decorator(allowed_users(allowed_roles=['sigp_admin']),name='dispatch')
class divAPIPayMonthlyY(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, pk, year, format=None):
        group = get_roles(request)
        div = get_object_or_404(Division, pk=pk)
        label,obj = list(),list()
        for i in range(1,13):
            mname = f_monthname_tet(int(i))
            a = Payment.objects.filter(project__owner=div, date__year=year, date__month=i).aggregate(Sum('total')).get('total__sum', 0.00)
            tot = 0
            if a: tot = a
            obj.append(tot)
            label.append(mname)
        data = { 'label': label, 'obj': obj, 'group': group }
        return Response(data)
###
