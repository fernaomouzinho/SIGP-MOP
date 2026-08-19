from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from contract.models import Contract, Amendment, AmendmentAmount, ContractYear
from payment.models import Invoice, Payment, PaymentHist, PhysicalProgress
from conf.user_utils import c_user_dna
from payment.forms import physicalProgressForm
from django.contrib import messages
from users.decorators import allowed_users
from sigp.utils import get_roles

@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_uivp'])
def PhysicalProgAdd(request, hashid):
    cont = get_object_or_404(Contract, hashed=hashid)
    dna = c_user_dna(request.user)
    pay = Payment.objects.filter(contract=cont).last()
    contyear = ContractYear.objects.filter(contract=cont).first()
   
    if request.method == 'POST':
        form = physicalProgressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.contract = cont
            instance.user = request.user
            instance.save()
            messages.success(request, f'Altera ona.')
            return redirect('phy-prog-list', hashid=hashid)
    else: form = physicalProgressForm()
    context = {
        'form': form, 'cont':cont,'pay': pay, 'contyear': contyear,
        'title': 'Hatama Progresu Fiziku', 'legend': 'Hatama Progresu Fiziku'
    }
    return render(request, 'progress/form.html', context)


@allowed_users(allowed_roles=['sigp_admin', 'sigp_dna', 'sigp_dna_s', 'sigp_uivp'])
def PhysicalProgEdit(request, pk):
    instance = get_object_or_404(PhysicalProgress, pk=pk)
    cont = instance.contract
    dna = c_user_dna(request.user)
    pay = Payment.objects.filter(contract=cont).last()
    contyear = ContractYear.objects.filter(contract=cont).first()

    if request.method == 'POST':
        form = physicalProgressForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user  # Optional: track the editor
            instance.save()
            messages.success(request, 'Progresu fiziku altera ona.')
            return redirect('phy-prog-list', hashid=cont.hashed)
    else:
        form = physicalProgressForm(instance=instance)

    context = {
        'form': form,
        'cont': cont,
        'pay': pay,
        'contyear': contyear,
        'title': 'Altera Progresu Fiziku',
        'legend': 'Altera Progresu Fiziku',
    }
    return render(request, 'progress/form.html', context)