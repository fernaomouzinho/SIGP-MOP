import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from custom.models import Division, PCat, PCategory, Sector, Capital
from contract.models import ContractYear
from payment.models import Payment

class divAPIPayDash(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj = ['Kontratu','Pagamentu','Balansu'],list()
		tot_cont = ContractYear.objects.filter(contract__project__owner=div, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_bal = 0
		if tot_paid: tot_bal = tot_cont-tot_paid
		obj = [tot_cont,tot_paid,tot_bal]
		data = { 'label': label, 'obj': obj, }
		return Response(data)
#
class divAPIPayMopCat(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCat.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcat=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcat=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayCat(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCategory.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPaySec(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Sector.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__sector=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__sector=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.name)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayCap(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Capital.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__capital=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__capital=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)
#
class divAPIPayYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj = ['Kontratu','Pagamentu','Balansu'],list()
		tot_cont = ContractYear.objects.filter(contract__project__owner=div, year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contract__project__owner=div, contyear__year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_bal = 0
		if tot_paid: tot_bal = tot_cont-tot_paid
		obj = [tot_cont,tot_paid,tot_bal]
		data = { 'label': label, 'obj': obj, }
		return Response(data)

class divAPIPayMopCatYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCat.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcat=obj, year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcat=obj, contyear__year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayCatYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCategory.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, contyear__year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPaySecYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Sector.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__sector=obj, year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__sector=obj, contyear__year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.name)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayCapYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Capital.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__capital=obj, year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__capital=obj, contyear__year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)
### FISCAL
class divAPIPayFisDash(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj = ['Kontratu','Pagamentu','Balansu'],list()
		tot_cont = ContractYear.objects.filter(contract__project__owner=div, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contract__project__owner=div, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_bal = 0
		if tot_paid: tot_bal = tot_cont-tot_paid
		obj = [tot_cont,tot_paid,tot_bal]
		data = { 'label': label, 'obj': obj, }
		return Response(data)
#
class divAPIPayFisMopCat(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCat.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcat=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcat=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayFisCat(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCategory.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayFisSec(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Sector.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__sector=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__sector=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.name)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayFisCap(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Capital.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__capital=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__capital=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)
#
class divAPIPayFisYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj = ['Kontratu','Pagamentu','Balansu'],list()
		tot_cont = ContractYear.objects.filter(contract__project__owner=div, year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contract__project__owner=div, contyear__year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_bal = 0
		if tot_paid: tot_bal = tot_cont-tot_paid
		obj = [tot_cont,tot_paid,tot_bal]
		data = { 'label': label, 'obj': obj, }
		return Response(data)

class divAPIPayFisMopCatYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCat.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcat=obj, year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcat=obj, contyear__year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayFisCatYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCategory.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, contyear__year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayFisSecYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Sector.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__sector=obj, year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__sector=obj, contyear__year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.name)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayFisCapYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Capital.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__capital=obj, year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__capital=obj, contyear__year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)
### ANN
class divAPIPayAnnDash(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj = ['Kontratu','Pagamentu','Balansu'],list()
		tot_cont = ContractYear.objects.filter(contract__project__owner=div).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contract__project__owner=div).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_bal = 0
		if tot_paid: tot_bal = tot_cont-tot_paid
		obj = [tot_cont,tot_paid,tot_bal]
		data = { 'label': label, 'obj': obj, }
		return Response(data)
#
class divAPIPayAnnMopCat(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCat.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcat=obj).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcat=obj).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayAnnCat(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCategory.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcategory=obj).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcategory=obj).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayAnnSec(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Sector.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__sector=obj).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__sector=obj).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.name)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayAnnCap(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Capital.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__capital=obj).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__capital=obj).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)
#
class divAPIPayAnnYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj = ['Kontratu','Pagamentu','Balansu'],list()
		tot_cont = ContractYear.objects.filter(contract__project__owner=div, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contract__project__owner=div, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_bal = 0
		if tot_paid: tot_bal = tot_cont-tot_paid
		obj = [tot_cont,tot_paid,tot_bal]
		data = { 'label': label, 'obj': obj, }
		return Response(data)

class divAPIPayAnnMopCatYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCat.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcat=obj, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcat=obj, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayAnnCatYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCategory.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__pcategory=obj, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayAnnSecYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Sector.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__sector=obj, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__sector=obj, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.name)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class divAPIPayAnnCapYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, pk, year, format=None):
		div = get_object_or_404(Division, pk=pk)
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Capital.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__owner=div, contract__project__capital=obj, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__owner=div, contract__project__capital=obj, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)