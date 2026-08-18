import datetime
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.contrib import messages
from payment.forms import PaymentPortalForm
from conf.utils import getnewid
from payment.models import PaymentPortal
from users.decorators import allowed_users
from sigp.utils import get_roles

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def payPortalList(request):
    payments = PaymentPortal.objects.all().order_by('-year')  # latest first

    context = {
        "objects": payments,
        "title": "Lista Pagamentu Portal",
        "legend": "Lista Pagamentu Portal",
    }
    return render(request, "payment/port_pay_list.html", context)


@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def payPortalAdd(request, hashid=None):
   
    form = PaymentPortalForm(request.POST or None)
    if request.method == "POST":
        newid, new_hashid = getnewid(PaymentPortal)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = newid
            instance.datetime = datetime.datetime.now()
            instance.hashed = new_hashid
            instance.user = request.user
            instance.save()
            messages.success(request, "Aumenta Pagamentu Portal ho susesu ✅")
        return redirect("pay-portal-list")

    context = {
        "form": form,
        "title": "Aumenta Pagamentu Portal",
        "legend": "Aumenta Pagamentu Portal",
    }
    return render(request, "payment/portal_form.html", context)


@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def payPortalEdit(request, hashid):
    pay = get_object_or_404(PaymentPortal, hashed=hashid)
    form = PaymentPortalForm(request.POST or None, instance=pay)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Atualiza pagamentu portal ho susesu ✅")
        return redirect("pay-portal-list")

    context = {
        "form": form,
        "title": "Atualiza Pagamentu Portal",
        "legend": "Atualiza Pagamentu Portal",
        "object": pay,
    }
    return render(request, "payment/portal_form.html", context)

@login_required
@allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp'])
def payPortalDelete(request, hashid):
    pay = get_object_or_404(PaymentPortal, hashed=hashid)
    if request.method == "POST":
        pay.delete()
        messages.success(request, "Hamos pagamentu portal ho susesu ❌")
    return redirect("pay-portal-list")
