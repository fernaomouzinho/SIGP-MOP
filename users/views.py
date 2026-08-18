import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from employee.models import EmployeeUser, EmployeeDiv, EmployeePos
from users.forms import UserUpdateForm
from company.models import Company, CompUser

@login_required
def Profile(request):
    group = request.user.groups.all()[0].name
    user = EmployeeUser.objects.get(user=request.user)
    emp = user.employee
    empdiv = EmployeeDiv.objects.filter(employee=emp).first()
    emppos = EmployeePos.objects.filter(employee=emp).first()
    context = {
        'group': group, 'emp': emp, 'empdiv': empdiv, 'emppos': emppos,
        'title': 'Informasaun Perfil', 'legend': 'Informasaun Perfil',
    }
    return render(request, 'auth/profile.html', context)

@login_required
def AccountUpdate(request):
    
    ob = EmployeeUser.objects.values('user')
    oc = CompUser.objects.values('user')
    for a in ob:
        if a['user'] == request.user.id:
            objects = EmployeeUser.objects.get(user=request.user)
    
    for a in oc:
        if a['user'] == request.user.id:
            objects = CompUser.objects.get(user=request.user)
            
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Ita nia konta atualiza ona!')
            return redirect('user-account')
    else: u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
        'title': 'Konta', 'legend': 'Konta',
    }
    return render(request, 'auth/account.html', context)

class UserPasswordChangeView(PasswordChangeView):
    template_name = 'auth/change_password.html'
    success_url = reverse_lazy('user-change-password-done')

class UserPasswordChangeDoneView(PasswordResetDoneView):
    template_name = 'auth/change_password_done.html'