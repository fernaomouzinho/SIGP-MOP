import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.contrib import messages
from contract.models import Amendment, AmendmentPeriod, AmendmentAmount, Contract, ContractYear, Deduction
from contract.forms import AmendPeriodForm, AmendAmountForm, DeductionForm
from project.models import Project
from payment.models import Payment, PaymentHist
from conf.utils import getnewid
from users.decorators import allowed_users
from sigp.utils import get_roles

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op'])
def AmendPerAdd(request, hashid):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	if request.method == 'POST':
		newid, new_hashid = getnewid(AmendmentPeriod)
		form = AmendPeriodForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.contract = cont
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta ona.')
			return redirect('amend-per-det', hashid)
	else: form = AmendPeriodForm()
	context = {
		'cont': cont, 'form': form, 'amend': amend, 'page': 'period',
		'title': 'Aumenta Tempu', 'legend': 'Aumenta Tempu',
	}
	return render(request, 'amendment/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op'])
def AmendPerEdit(request, hashid, pk):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	objects = get_object_or_404(AmendmentPeriod, pk=pk)
	if request.method == 'POST':
		form = AmendPeriodForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Altera ona.')
			return redirect('amend-per-det', hashid)
	else: form = AmendPeriodForm(instance=objects)
	context = {
		'cont': cont, 'form': form, 'page': 'period',
		'title': 'Altera Tempu', 'legend': 'Altera Tempu',
	}
	return render(request, 'amendment/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op'])
def AmendPerRem(request, hashid, pk):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	objects = get_object_or_404(AmendmentPeriod, pk=pk)
	objects.delete()
	amend.number = cont.number
	amend.end_date = cont.end_date
	amend.save()
	messages.success(request, f'Hapaga ona.')
	return redirect('amend-per-det', hashid)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op'])
def AmendPerConf(request, hashid, pk):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	objects = get_object_or_404(AmendmentPeriod, pk=pk)
	objects2 = AmendmentPeriod.objects.filter(contract=cont).exclude(id=pk).all()
	objects.is_confirm = True
	objects.is_active = True
	objects.save()
	for i in objects2:
		i.is_active = False
		i.save()
	amend.number = objects.number
	amend.end_date = objects.end_date
	amend.save()
	messages.success(request, f'Konfirma ona.')
	return redirect('amend-per-det', hashid)
###
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op'])
def AmendAmAdd(request, hashid):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	pays = Payment.objects.filter(contract=cont).all()
	amend_a = AmendmentAmount.objects.filter(contract=cont).first()
	if request.method == 'POST':
		newid, new_hashid = getnewid(AmendmentAmount)
		form = AmendAmountForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.contract = cont
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()

			if amend_a: info = form.cleaned_data.get('desc')
			else: info = "Original"
			
			for i in pays:
				obj2 = PaymentHist(user=request.user, contract=i.contract,\
					phys_prog=i.phys_prog, desc=i.desc,\
					total=i.total, com_amount=i.com_amount,\
					com_percent=i.com_percent, bal_amount=i.bal_amount,\
					bal_percent=i.bal_percent, date=i.date, info=info)
				obj2.save()
			messages.success(request, f'Aumenta ona.')
			return redirect('amend-am-det', hashid)
	else: form = AmendAmountForm()
	context = {
		'cont': cont, 'form': form, 'page': 'amount',
		'title': 'Aumenta Montante', 'legend': 'Aumenta Montante',
	}
	return render(request, 'amendment/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op'])
def AmendAmEdit(request, hashid, pk):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	objects = get_object_or_404(AmendmentAmount, pk=pk)
	if request.method == 'POST':
		form = AmendAmountForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Altera ona.')
			return redirect('amend-am-det', hashid)
	else: form = AmendAmountForm(instance=objects)
	context = {
		'cont': cont, 'form': form,  'page': 'amount',
		'title': 'Altera Montante', 'legend': 'Altera Montante',
	}
	return render(request, 'amendment/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op'])
def AmendAmRem(request, hashid, pk):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	objects = get_object_or_404(AmendmentAmount, pk=pk)
	objects.delete()
	amend.number = cont.number
	amend.total = cont.total
	amend.save()
	messages.success(request, f'Hapaga ona.')
	return redirect('amend-am-det', hashid)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op'])
def AmendAmConf(request, hashid, pk):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	objects = get_object_or_404(AmendmentAmount, pk=pk)
	objects.is_confirm = True
	objects.save()
	total = float(amend.total)+float(objects.total)
	amend.number = objects.number
	amend.total = total
	amend.save()
	contyears = ContractYear.objects.filter(contract=cont).all()
	for i in contyears:
		i.total = total
		i.save()
	messages.success(request, f'Konfirma ona.')
	return redirect('amend-am-det', hashid)
###
@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op'])
def DeducAdd(request, hashid):
	cont = get_object_or_404(Contract, hashed=hashid)
	if request.method == 'POST':
		newid, new_hashid = getnewid(Deduction)
		form = DeductionForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.contract = cont
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			messages.success(request, f'Aumenta ona.')
			return redirect('deduc-det', hashid)
	else: form = DeductionForm()
	context = {
		'cont': cont, 'form': form, 'page': 'deduc',
		'title': 'Aumenta Dedusaun', 'legend': 'Aumenta Dedusaun',
	}
	return render(request, 'amendment/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op'])
def DeducEdit(request, hashid, pk):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	objects = get_object_or_404(Deduction, pk=pk)
	if request.method == 'POST':
		form = DeductionForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Altera ona.')
			return redirect('deduc-det', hashid)
	else: form = DeductionForm(instance=objects)
	context = {
		'cont': cont, 'form': form,  'page': 'deduc',
		'title': 'Altera Dedusaun', 'legend': 'Altera Dedusaun',
	}
	return render(request, 'amendment/form.html', context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op'])
def DeducRem(request, hashid, pk):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	objects = get_object_or_404(Deduction, pk=pk)
	objects.delete()
	amend.number = cont.number
	amend.total = cont.total
	amend.save()
	messages.success(request, f'Hapaga ona.')
	return redirect('deduc-det', hashid)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_op'])
def DeducConf(request, hashid, pk):
	cont = get_object_or_404(Contract, hashed=hashid)
	amend = Amendment.objects.filter(contract=cont).first()
	objects = get_object_or_404(Deduction, pk=pk)
	objects.is_confirm = True
	objects.save()
	total = float(objects.total)
	amend.total = total
	amend.save()
	contyears = ContractYear.objects.filter(contract=cont).all()
	for i in contyears:
		i.total = total
		i.save()
	messages.success(request, f'Konfirma ona.')
	return redirect('deduc-det', hashid)