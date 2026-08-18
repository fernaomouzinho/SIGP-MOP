import datetime
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from custom.models import PCat, PCategory, Sector, Capital
from contract.models import ContractYear
from payment.models import Payment

class APIPayDash(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		label,obj = ['Kontratu','Pagamentu','Balansu'],list()
		tot_cont = ContractYear.objects.filter(contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_bal = 0
		if tot_paid: tot_bal = tot_cont-tot_paid
		obj = [tot_cont,tot_paid,tot_bal]
		data = { 'label': label, 'obj': obj, }
		return Response(data)
#
class APIPayMopCat(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCat.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__pcat=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__pcat=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayCat(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCategory.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__pcategory=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__pcategory=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPaySec(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Sector.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__sector=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__sector=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.name)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayCap(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Capital.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__capital=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__capital=obj, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)
#
class APIPayYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj = ['Kontratu','Pagamentu','Balansu'],list()
		tot_cont = ContractYear.objects.filter(year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contyear__year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_bal = 0
		if tot_paid: tot_bal = tot_cont-tot_paid
		obj = [tot_cont,tot_paid,tot_bal]
		data = { 'label': label, 'obj': obj, }
		return Response(data)

class APIPayMopCatYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCat.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__pcat=obj, year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__pcat=obj, contyear__year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayCatYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCategory.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__pcategory=obj, year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__pcategory=obj, contyear__year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPaySecYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Sector.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__sector=obj, year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__sector=obj, contyear__year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.name)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayCapYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Capital.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__capital=obj, year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__capital=obj, contyear__year=year, contract__is_fiscal=False).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)
### FISCAL
class APIPayFisDash(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		label,obj = ['Kontratu','Pagamentu','Balansu'],list()
		tot_cont = ContractYear.objects.filter(contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_bal = 0
		if tot_paid: tot_bal = tot_cont-tot_paid
		obj = [tot_cont,tot_paid,tot_bal]
		data = { 'label': label, 'obj': obj, }
		return Response(data)
#
class APIPayFisMopCat(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCat.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__pcat=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__pcat=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayFisCat(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCategory.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__pcategory=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__pcategory=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayFisSec(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Sector.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__sector=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__sector=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.name)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayFisCap(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Capital.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__capital=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__capital=obj, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)
#
class APIPayFisYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj = ['Kontratu','Pagamentu','Balansu'],list()
		tot_cont = ContractYear.objects.filter(year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contyear__year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_bal = 0
		if tot_paid: tot_bal = tot_cont-tot_paid
		obj = [tot_cont,tot_paid,tot_bal]
		data = { 'label': label, 'obj': obj, }
		return Response(data)

class APIPayFisMopCatYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCat.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__pcat=obj, year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__pcat=obj, contyear__year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayFisCatYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCategory.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__pcategory=obj, year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__pcategory=obj, contyear__year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayFisSecYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Sector.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__sector=obj, year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__sector=obj, contyear__year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.name)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayFisCapYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Capital.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__capital=obj, year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__capital=obj, contyear__year=year, contract__is_fiscal=True).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)
### ANN
class APIPayAnnDash(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		this_year = datetime.date.today().year
		label,obj = ['Kontratu','Pagamentu','Balansu'],list()
		tot_cont = ContractYear.objects.filter(year=this_year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(date__year=this_year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_bal = 0
		if tot_paid: tot_bal = tot_cont-tot_paid
		obj = [tot_cont,tot_paid,tot_bal]
		data = { 'label': label, 'obj': obj, }
		return Response(data)
#
class APIPayAnnMopCat(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		this_year = datetime.date.today().year
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCat.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__pcat=obj, year=this_year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__pcat=obj, contyear__year=this_year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayAnnCat(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		this_year = datetime.date.today().year
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCategory.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__pcategory=obj, year=this_year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__pcategory=obj, contyear__year=this_year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayAnnSec(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		this_year = datetime.date.today().year
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Sector.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__sector=obj, year=this_year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__sector=obj, contyear__year=this_year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.name)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayAnnCap(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		this_year = datetime.date.today().year
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Capital.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__capital=obj, year=this_year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__capital=obj, contyear__year=this_year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)
#
class APIPayAnnYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj = ['Kontratu','Pagamentu','Balansu'],list()
		tot_cont = ContractYear.objects.filter(year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_paid = Payment.objects.filter(contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
		tot_bal = 0
		if tot_paid: tot_bal = tot_cont-tot_paid
		obj = [tot_cont,tot_paid,tot_bal]
		data = { 'label': label, 'obj': obj, }
		return Response(data)

class APIPayAnnMopCatYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCat.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__pcat=obj, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__pcat=obj, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayAnnCatYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = PCategory.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__pcategory=obj, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__pcategory=obj, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayAnnSecYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Sector.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__sector=obj, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__sector=obj, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.name)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)

class APIPayAnnCapYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, year, format=None):
		label,obj1,obj2,obj3 = list(),list(),list(),list()
		objs = Capital.objects.all()
		for obj in objs:
			obja, objb = 0,0
			obj_a = ContractYear.objects.filter(contract__project__capital=obj, year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_a: obja = obj_a
			obj_b = Payment.objects.filter(contract__project__capital=obj, contyear__year=year).exclude(total=0).aggregate(Sum('total')).get('total__sum', 0.00)
			if obj_b: objb = obj_b
			objc = obja-objb
			label.append(obj.code)
			obj1.append(obja)
			obj2.append(objb)
			obj3.append(objc)
		data = { 'label': label, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, }
		return Response(data)