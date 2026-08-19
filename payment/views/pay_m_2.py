import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from contract.models import ContPay, Contract, Amendment, ContractYear
from payment.models import Payment, PaymentFiscal
from payment.forms import customPayForm, customPayForm2
from payment.pay_utils import f_com_amount, f_com_percent, f_bal_amount, f_bal_percent, f_refresh
from conf.utils import getnewid
from users.decorators import allowed_users
from sigp.utils import get_roles


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def customPayAdd(request, hashid):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	contyear = ContractYear.objects.filter(contract=cont).first()
	paylast = Payment.objects.filter(contract=cont).last()
	if paylast: pay_com = paylast.com_amount
	else: pay_com = 0
	if request.method == 'POST':
		newid, new_hashid = getnewid(Payment)
		form = customPayForm(request.POST)
		if form.is_valid():
			total = form.cleaned_data.get('total')
			com_amount = f_com_amount(total,pay_com)
			com_percent = f_com_percent(com_amount,amend.total)
			bal_amount = f_bal_amount(amend.total,com_amount)
			bal_percent = f_bal_percent(bal_amount,amend.total)
			instance = form.save(commit=False)
			instance.id = newid
			instance.contract = cont
			instance.contyear = contyear
			instance.com_amount = com_amount
			instance.com_percent = com_percent
			instance.bal_amount = bal_amount
			instance.bal_percent = bal_percent
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta ona.')
			return redirect('custom-pay-list', hashid=hashid)
	else: form = customPayForm()
	context = {
		'cont': cont, 'amend':amend, 'form': form,
		'title': 'Aumenta Pagamentu', 'legend': 'Aumenta Pagamentu'
	}
	return render(request, 'payment/custom_form.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def customPayEdit(request, hashid, hashid2):
	cont = get_object_or_404(Contract, hashed=hashid)
	pay = get_object_or_404(Payment, hashed=hashid2)
	contyear = ContractYear.objects.filter(contract=cont).first()
	if request.method == 'POST':
		form = customPayForm2(request.POST, instance=pay)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.contyear = contyear
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera ona.')
			return redirect('custom-pay-list', hashid=hashid)
	else: form = customPayForm2(instance=pay)
	context = {
		'cont': cont, 'form': form,
		'title': 'Altera Pagamentu', 'legend': 'Altera Pagamentu'
	}
	return render(request, 'payment/custom_form.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def customPayRem(request, hashid, pk):
	objects = get_object_or_404(Payment, pk=pk)
	objects.delete()
	messages.success(request, f'Hapaga ona!')
	return redirect('custom-pay-list', hashid=hashid)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def customPayReady(request, hashid, pk):
	objects = get_object_or_404(Payment, pk=pk)
	objects.is_ready = True
	objects.save()
	messages.success(request, f'Pronto!')
	return redirect('custom-pay-list', hashid=hashid)
#

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def ContPayUpdate(request, hashid):
	cont = get_object_or_404(Contract, hashed=hashid)
	contpay = ContPay.objects.get(contract=cont)
	last_pay = Payment.objects.filter(contract=cont).last()
	contpay.com_amount = last_pay.com_amount
	contpay.com_percent = last_pay.com_percent
	contpay.bal_amount = last_pay.bal_amount
	contpay.bal_percent = last_pay.bal_percent
	if last_pay.phys_prog: contpay.phys_prog = last_pay.phys_prog
	contpay.save()
	messages.success(request, f'Atualiza ona.')
	return redirect('custom-pay-list', hashid=hashid)
#

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def customPayRefresh(request, hashid):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	pays = Payment.objects.filter(contract=cont).all()
	amend_amount = float(amend.total)

	payment2 = f_refresh(pays)
	zeros = np.array([np.zeros(payment2.shape[1])])
	new_payment = np.array(np.vstack((zeros,payment2)))
	new_result = []
	for i in range(1,new_payment.shape[0]):
		id = new_payment[i,0]
		amount = float(new_payment[i,1])
		pay_com = float(new_payment[i-1,2])
		com_amount = f_com_amount(amount,pay_com)
		com_percent = f_com_percent(com_amount,amend_amount)
		bal_amount = f_bal_amount(amend_amount,com_amount)
		bal_percent = f_bal_percent(bal_amount,amend_amount)
		new_result.append([id,com_amount,com_percent,bal_amount,bal_percent])
	for j in new_result:
		obj = Payment.objects.filter(id=j[0]).first()
		obj.com_amount = j[1]
		obj.com_percent = j[2]
		obj.bal_amount = j[3]
		obj.bal_percent = j[4]
		obj.save()
	messages.success(request, f'Altera ona.')
	return redirect('custom-pay-list', hashid=hashid)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def customPayDeducRefresh(request, hashid):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	pays = Payment.objects.filter(contract=cont).all()
	amend_amount = float(amend.total)
	payment2 = f_refresh(pays)
	zeros = np.array([np.zeros(payment2.shape[1])])
	new_payment = np.array(np.vstack((zeros,payment2)))
	new_result = []
	for i in range(1,new_payment.shape[0]):
		id = new_payment[i,0]
		amount = float(new_payment[i,1])
		pay_com = float(new_payment[i-1,2])
		com_amount = f_com_amount(amount,pay_com)
		com_percent = f_com_percent(com_amount,amend_amount)
		bal_amount = f_bal_amount(amend_amount,com_amount)
		bal_percent = f_bal_percent(bal_amount,amend_amount)
		new_result.append([id,com_amount,com_percent,bal_amount,bal_percent])
	for j in new_result:
		obj = Payment.objects.filter(id=j[0]).first()
		obj.com_amount = j[1]
		obj.com_percent = j[2]
		obj.bal_amount = j[3]
		obj.bal_percent = j[4]
		obj.save()
	messages.success(request, f'Altera ona.')
	return redirect('custom-pay-list', hashid=hashid)
### FISCAL

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def fiscalPayAdd(request, hashid, year):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	contyear = ContractYear.objects.filter(contract=cont, year=year).first()
	paylast = Payment.objects.filter(contyear=contyear).last()
	if paylast: pay_com = paylast.com_amount
	else: pay_com = 0
	fiscal = PaymentFiscal.objects.filter(contract=cont, year=year).first()
	if request.method == 'POST':
		newid, new_hashid = getnewid(Payment)
		form = customPayForm(request.POST)
		if form.is_valid():
			total = form.cleaned_data.get('total')
			com_amount = f_com_amount(total,pay_com)
			com_percent = f_com_percent(com_amount,contyear.total)
			bal_amount = f_bal_amount(contyear.total,com_amount)
			bal_percent = f_bal_percent(bal_amount,contyear.total)
			instance = form.save(commit=False)
			instance.id = newid
			instance.contract = cont
			instance.contyear = contyear
			instance.com_amount = com_amount
			instance.com_percent = com_percent
			instance.bal_amount = bal_amount
			instance.bal_percent = bal_percent
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()

			if not fiscal:
				newid2, _ = getnewid(PaymentFiscal)
				obj = PaymentFiscal(id=newid2, contract=cont, year=year, com_amount=com_amount, com_percent=com_percent,\
					bal_amount=bal_amount, bal_percent=bal_percent, user=request.user, datetime=datetime.datetime.now())
				obj.save()
			messages.success(request, f'Aumenta ona.')
			return redirect('fiscal-pay-list', hashid=hashid, year=year)
	else: form = customPayForm()
	context = {
		'cont': cont, 'amend': amend, 'form': form, 'year': year, 'page': 'fiscal',
		'title': 'Aumenta Pagamentu', 'legend': 'Aumenta Pagamentu'
	}
	return render(request, 'payment/custom_form.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def fiscalPayEdit(request, hashid, hashid2, year):
	cont = get_object_or_404(Contract, hashed=hashid)
	pay = get_object_or_404(Payment, hashed=hashid2)
	contyear = ContractYear.objects.filter(contract=cont, year=year).first()
	if request.method == 'POST':
		form = customPayForm2(request.POST, instance=pay)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.contyear = contyear
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera ona.')
			return redirect('fiscal-pay-list', hashid=hashid, year=year)
	else: form = customPayForm2(instance=pay)
	context = {
		'cont': cont, 'form': form, 'year': year, 'page': 'fiscal',
		'title': 'Altera Pagamentu', 'legend': 'Altera Pagamentu'
	}
	return render(request, 'payment/custom_form.html', context)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def fiscalPayRem(request, hashid, pk, year):
	objects = get_object_or_404(Payment, pk=pk)
	objects.delete()
	messages.success(request, f'Hapaga ona!')
	return redirect('fiscal-pay-list', hashid=hashid, year=year)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def fiscalPayReady(request, hashid, pk, year):
	objects = get_object_or_404(Payment, pk=pk)
	objects.is_ready = True
	objects.save()
	messages.success(request, f'Pronto!')
	return redirect('fiscal-pay-list', hashid=hashid, year=year)
#

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def PayFiscalUpdate(request, pk, year):
	contyear = get_object_or_404(ContractYear, pk=pk)
	cont = contyear.contract
	fiscal = PaymentFiscal.objects.filter(contract=cont, year=year).first()
	# last_pay = Payment.objects.filter(contyear=contyear, date__year=year).last()
	last_pay = Payment.objects.filter(contyear=contyear).last()
	fiscal.com_amount = last_pay.com_amount
	fiscal.com_percent = last_pay.com_percent
	fiscal.bal_amount = last_pay.bal_amount
	fiscal.bal_percent = last_pay.bal_percent
	fiscal.save()
	messages.success(request, f'Altera ona.')
	return redirect('fiscal-pay-list', hashid=cont.hashed, year=year)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def PayFiscalEna(request, hashid, pk):
	objects = get_object_or_404(PaymentFiscal, pk=pk)
	objects.is_active = True
	objects.save()
	objects2 = PaymentFiscal.objects.exclude(pk=pk).all()
	for i in objects2:
		i.is_active = False
		i.save()
	messages.success(request, f'Ativa!')
	return redirect('fiscal-year-list', hashid=hashid)


@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def PayFiscalEnd(request, hashid, year, pk):
	objects = get_object_or_404(ContractYear, pk=pk)
	objects.is_end = True
	objects.save()
	messages.success(request, f'Termina!')
	return redirect('fiscal-pay-list', hashid=hashid, year=year)
