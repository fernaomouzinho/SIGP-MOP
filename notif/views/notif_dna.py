import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from finance.models import CPV, PO, POLetter
from invoice.models import InvLet, InvTrack
from eval.models import Eval
from proc.models import ProcLet
from contract.models import ContractComp

###
# class notifDNACPV(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = CPV.objects.filter(is_end=True, is_get_dna=False).all().count()
#         return Response({'value':tot})

# class notifDNAPO(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = PO.objects.filter((Q(is_back=True)|Q(potrack__is_dgaf_out=True, is_end=False))).all().count()
#         return Response({'value':tot})

# class notifDNAEval(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = Eval.objects.filter(is_appr=True, is_end=False).all().count()
#         return Response({'value':tot})

# class notifDNAProc(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = ProcLet.objects.filter(to_id=3, is_send=True, is_read=False).all().count()
#         return Response({'value':tot})

# class notifDNAInv(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = InvLet.objects.filter((Q(to_id=1, is_send=True, is_read=False)|Q(to_id=2, is_back=True))).all().count()
#         return Response({'value':tot})
# ###
# #cpv
# @login_required
# @allowed_users(allowed_roles=['dna'])
# def notifDNACPVList(request):
#     group = request.user.groups.all()[0].name
#     objects = CPV.objects.filter(is_end=True, is_get_dna=False).all().order_by('-date')
#     context = {
#         'group': group, 'objects':objects,
#         'title': 'CPV Aprovadu', 'legend': 'CPV Aprovadu'
#     }
#     return render(request, 'notif_dna/cpv_list.html', context)
# #po
# @login_required
# @allowed_users(allowed_roles=['dna'])
# def notifDNAPOList(request):
#     group = request.user.groups.all()[0].name
#     objects1 = PO.objects.filter(is_back=True).all().order_by('-date')
#     objects2 = POLetter.objects.filter(is_send=True, is_read=False).all().order_by('-date')
#     context = {
#         'group': group, 'objects1':objects1, 'objects2':objects2,
#         'title': 'PO Fila - Despaxu', 'legend': 'PO Fila - Despaxu'
#     }
#     return render(request, 'notif_dna/po_list.html', context)

# # EVAL
# @login_required
# @allowed_users(allowed_roles=['dna'])
# def notifDNAEvalList(request):
#     group = request.user.groups.all()[0].name
#     objects = Eval.objects.filter(is_appr=True, is_end=False).all().order_by('-id')
#     context = {
#         'group': group, 'objects': objects,
#         'title': 'Lista ToR Aprovadu', 'legend': 'Lista ToR Aprovadu'
#     }
#     return render(request, 'notif_dna/eval_list.html', context)

# # PROC
# @login_required
# @allowed_users(allowed_roles=['dna','dna_s'])
# def notifDNAProcList(request):
#     group = request.user.groups.all()[0].name
#     objects = ProcLet.objects.filter(to_id=3, is_send=True, is_read=False)
#     context = {
#         'group': group, 'objects':objects,
#         'title': 'Tender', 'legend': 'Tender'
#     }
#     return render(request, 'notif_dna/proc_list.html', context)
# # INV
# @login_required
# @allowed_users(allowed_roles=['dna'])
# def notifDNAInvList(request):
#     group = request.user.groups.all()[0].name
#     objects = InvLet.objects.filter((Q(to_id=1, is_send=True, is_read=False)|Q(to_id=2, is_back=True))).all().order_by('-id')
#     compcont = ContractComp.objects.all()
#     context = {
#         'group': group, 'objects': objects,'compcont':compcont,
#         'title': 'Resibu Foun', 'legend': 'Resibu Foun'
#     }
#     return render(request, 'notif_dna/inv_list.html', context)

# @login_required
# @allowed_users(allowed_roles=['dna'])
# def notifDNAInvDet(request, hashid):
#     group = request.user.groups.all()[0].name
#     obj = get_object_or_404(InvLet, hashed=hashid)
#     inv = obj.inv
#     cont = inv.cont
#     proj = cont.project
#     compcont = ContractComp.objects.filter(contract=cont).first()
#     track = InvTrack.objects.filter(inv=inv).first()
#     context = {
#         'group':group, 'obj':obj, 'inv':inv, 'cont':cont, 'proj':proj, 'track':track,'compcont':compcont,
#         'title':'Detallu Karta', 'legend':'Detallu Karta'
#     }
#     return render(request, 'notif_dna/inv_det.html', context)

# ============================================================
# DNA NOTIFICATION APIs
# ============================================================

DNA_ROLES = ["sigp_dna", "sigp_dna_s"]


class notifDNACPV(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        portal_user = getattr(request, "portal_user", None)

        if not portal_user:
            return Response(
                {"detail": "Authentication required."},
                status=401
            )

        group = getattr(request, "portal_roles", [])

        if not group:
            group = request.session.get("portal_roles", [])

        if not any(role in group for role in DNA_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = CPV.objects.filter(
            is_end=True,
            is_get_dna=False
        ).count()

        return Response({
            "value": total
        })


class notifDNAPO(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        portal_user = getattr(request, "portal_user", None)

        if not portal_user:
            return Response(
                {"detail": "Authentication required."},
                status=401
            )

        group = getattr(request, "portal_roles", [])

        if not group:
            group = request.session.get("portal_roles", [])

        if not any(role in group for role in DNA_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = PO.objects.filter(
            Q(is_back=True) |
            Q(
                potrack__is_dgaf_out=True,
                is_end=False
            )
        ).count()

        return Response({
            "value": total
        })


class notifDNAEval(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        portal_user = getattr(request, "portal_user", None)

        if not portal_user:
            return Response(
                {"detail": "Authentication required."},
                status=401
            )

        group = getattr(request, "portal_roles", [])

        if not group:
            group = request.session.get("portal_roles", [])

        if not any(role in group for role in DNA_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = Eval.objects.filter(
            is_appr=True,
            is_end=False
        ).count()

        return Response({
            "value": total
        })


class notifDNAProc(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        portal_user = getattr(request, "portal_user", None)

        if not portal_user:
            return Response(
                {"detail": "Authentication required."},
                status=401
            )

        group = getattr(request, "portal_roles", [])

        if not group:
            group = request.session.get("portal_roles", [])

        if not any(role in group for role in DNA_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = ProcLet.objects.filter(
            to_id=3,
            is_send=True,
            is_read=False
        ).count()

        return Response({
            "value": total
        })


class notifDNAInv(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        portal_user = getattr(request, "portal_user", None)

        if not portal_user:
            return Response(
                {"detail": "Authentication required."},
                status=401
            )

        group = getattr(request, "portal_roles", [])

        if not group:
            group = request.session.get("portal_roles", [])

        if not any(role in group for role in DNA_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = InvLet.objects.filter(
            Q(
                to_id=1,
                is_send=True,
                is_read=False
            ) |
            Q(
                to_id=2,
                is_back=True
            )
        ).count()

        return Response({
            "value": total
        })


# ============================================================
# DNA CPV LIST
# ============================================================

def notifDNACPVList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in DNA_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = (
        CPV.objects
        .filter(
            is_end=True,
            is_get_dna=False
        )
        .order_by("-date")
    )

    context = {
        "group": group,
        "objects": objects,
        "title": "CPV Aprovadu",
        "legend": "CPV Aprovadu",
    }

    return render(
        request,
        "notif_dna/cpv_list.html",
        context
    )


# ============================================================
# DNA PO LIST
# ============================================================

def notifDNAPOList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in DNA_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects1 = (
        PO.objects
        .filter(is_back=True)
        .order_by("-date")
    )

    objects2 = (
        POLetter.objects
        .filter(
            is_send=True,
            is_read=False
        )
        .order_by("-date")
    )

    context = {
        "group": group,
        "objects1": objects1,
        "objects2": objects2,
        "title": "PO Fila - Despaxu",
        "legend": "PO Fila - Despaxu",
    }

    return render(
        request,
        "notif_dna/po_list.html",
        context
    )


# ============================================================
# DNA EVALUATION LIST
# ============================================================

def notifDNAEvalList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in DNA_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = (
        Eval.objects
        .filter(
            is_appr=True,
            is_end=False
        )
        .order_by("-id")
    )

    context = {
        "group": group,
        "objects": objects,
        "title": "Lista ToR Aprovadu",
        "legend": "Lista ToR Aprovadu",
    }

    return render(
        request,
        "notif_dna/eval_list.html",
        context
    )


# ============================================================
# DNA PROCUREMENT LIST
# ============================================================

def notifDNAProcList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in DNA_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = ProcLet.objects.filter(
        to_id=3,
        is_send=True,
        is_read=False
    )

    context = {
        "group": group,
        "objects": objects,
        "title": "Tender",
        "legend": "Tender",
    }

    return render(
        request,
        "notif_dna/proc_list.html",
        context
    )


# ============================================================
# DNA INVOICE LIST
# ============================================================

def notifDNAInvList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in DNA_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = (
        InvLet.objects
        .filter(
            Q(
                to_id=1,
                is_send=True,
                is_read=False
            ) |
            Q(
                to_id=2,
                is_back=True
            )
        )
        .order_by("-id")
    )

    compcont = ContractComp.objects.all()

    context = {
        "group": group,
        "objects": objects,
        "compcont": compcont,
        "title": "Resibu Foun",
        "legend": "Resibu Foun",
    }

    return render(
        request,
        "notif_dna/inv_list.html",
        context
    )


# ============================================================
# DNA INVOICE DETAIL
# ============================================================

def notifDNAInvDet(request, hashid):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in DNA_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    obj = get_object_or_404(
        InvLet,
        hashed=hashid
    )

    inv = obj.inv
    cont = inv.cont
    proj = cont.project

    compcont = (
        ContractComp.objects
        .filter(contract=cont)
        .first()
    )

    track = (
        InvTrack.objects
        .filter(inv=inv)
        .first()
    )

    context = {
        "group": group,
        "obj": obj,
        "inv": inv,
        "cont": cont,
        "proj": proj,
        "track": track,
        "compcont": compcont,
        "title": "Detallu Karta",
        "legend": "Detallu Karta",
    }

    return render(
        request,
        "notif_dna/inv_det.html",
        context
    )