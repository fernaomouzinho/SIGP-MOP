from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from employee.models import Employee, EmployeeDiv, EmployeePos
from conf.decorators import allowed_users

@login_required
@allowed_users(allowed_roles=['admin'])
def EmpList(request):
	group = request.user.groups.all()[0].name
	objects = Employee.objects.all().prefetch_related('employeepos','employeediv').order_by("name")
	context = {
		'group': group, 'objects': objects,
		'title': 'Utilizadores', 'legend': 'Utilizadores'
	}
	return render(request, 'employee/list.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def EmpDetail(request, hashid):
	group = request.user.groups.all()[0].name
	emp = get_object_or_404(Employee, hashed=hashid)
	empdiv = EmployeeDiv.objects.filter(employee=emp).first()
	emppos = EmployeePos.objects.filter(employee=emp).first()
	context = {
		'group': group, 'emp': emp, 'empdiv': empdiv, 'emppos': emppos,
		'title': 'Detalha Utilizador', 'legend': 'Detalha Utilizador',
	}
	return render(request, 'employee/detail.html', context)
