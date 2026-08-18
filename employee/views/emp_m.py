import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from employee.models import Employee, EmployeeUser
from employee.forms import *
from conf.utils import getnewid, split_string

@login_required
@allowed_users(allowed_roles=['admin'])
def EmpAdd(request):
	group = Group.objects.get(name='user')
	if request.method == 'POST':
		newid, new_hashid = getnewid(Employee)
		newid2, _ = getnewid(User)
		newid3, _ = getnewid(EmployeeUser)
		form = EmpForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.id = newid
			instance.datetime = datetime.datetime.now()
			instance.user = request.user
			instance.hashed = new_hashid
			instance.save()
			username = split_string(form.cleaned_data.get('name')).lower()+str(newid)
			password = make_password('mopSigP_23')
			obj = User(id=newid2, username=username, password=password)
			obj.save()
			obj2 = EmployeeUser(id=newid3, user_id=newid2, employee_id=newid)
			obj2.save()
			user = User.objects.get(pk=newid2)
			user.groups.add(group)
			messages.success(request, f'Aumenta ona.')
			return redirect('emp-list')
	else: form = EmpForm()
	context = {
		'form': form, 'user': request.user, 'page': 'plist',
		'title': 'Aumenta Utilizador', 'legend': 'Aumenta Utilizador'
	}
	return render(request, 'employee/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def EmpEdit(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	if request.method == 'POST':
		form = EmpForm(request.POST, instance=emp)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera ona.')
			return redirect('emp-det', hashid=hashid)
	else: form = EmpForm(instance=emp)
	context = {
		'emp': emp, 'form': form,
		'title': 'Altera Utilizador', 'legend': 'Altera Utilizador'
	}
	return render(request, 'employee/form.html', context)
#
@login_required
@allowed_users(allowed_roles=['admin'])
def EmpDivEdit(request, hashid, pk):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = get_object_or_404(EmployeeDiv, pk=pk)
	if request.method == 'POST':
		form = EmpDivForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Aumenta ona.')
			return redirect('emp-det', hashid=hashid)
	else: form = EmpDivForm(instance=objects)
	context = {
		'emp': emp, 'form': form, 'page': 'pdet',
		'title': 'Kolokasaun', 'legend': 'Kolokasaun'
	}
	return render(request, 'employee/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def EmpDivRem(request, hashid, pk):
	objects = get_object_or_404(EmployeeDiv, pk=pk)
	objects.delete()
	messages.success(request, f'Hapaga ona.')
	return redirect('emp-det', hashid=hashid)
#
@login_required
@allowed_users(allowed_roles=['admin'])
def EmpPosEdit(request, hashid, pk):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = get_object_or_404(EmployeePos, pk=pk)
	if request.method == 'POST':
		form = EmpPosForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Aumenta ona.')
			return redirect('emp-det', hashid=hashid)
	else: form = EmpPosForm(instance=objects)
	context = {
		'emp': emp, 'form': form, 'page': 'pdet',
		'title': 'Aumenta Pojisaun', 'legend': 'Aumenta Pojisaun'
	}
	return render(request, 'employee/form.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def EmpPosRem(request, hashid, pk):
	objects = get_object_or_404(EmployeePos, pk=pk)
	objects.position = None
	objects.start_date = None
	objects.save()
	messages.success(request, f'Hapaga ona.')
	return redirect('emp-det', hashid=hashid)