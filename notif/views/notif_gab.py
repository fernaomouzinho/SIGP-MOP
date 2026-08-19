from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from eval.models import EvalLet
from finance.models import CPV
from invoice.models import InvLet, InvTrack
from proc.models import ProcLet
from contract.models import ContractComp

# #
# class notifGabCPV(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = CPV.objects.filter(is_dgaf=False, is_send=True, is_appr=False).all().count()
#         return Response({'value':tot})

# class notifGabEval(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = EvalLet.objects.filter(to_id=1, is_send=True, is_read=False).all().count()
#         return Response({'value':tot})

# class notifGabProc(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = ProcLet.objects.filter(to_id=1, is_send=True, is_read=False).all().count()
#         return Response({'value':tot})

# class notifGabInv(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = InvLet.objects.filter((Q(is_send=True, is_read=False)|Q(is_back=True)), to_id=5).all().count()
#         return Response({'value':tot})
# ###
# # CPV
# @login_required
# @allowed_users(allowed_roles=['gab'])
# def notifGabCPVList(request):
#     group = request.user.groups.all()[0].name
#     objects = CPV.objects.filter(is_dgaf=False, is_send=True, is_appr=False).all().order_by("-date")
#     context = {
#         'group': group, 'objects': objects,
#         'title': 'Pedidu Aprovasaun CPV', 'legend': 'Pedidu Aprovasaun CPV'
#     }
#     return render(request, 'notif_gab/cpv_list.html', context)
# # EVAL
# @login_required
# @allowed_users(allowed_roles=['gab'])
# def notifGabEvalList(request):
#     group = request.user.groups.all()[0].name
#     objects = []
#     objects = EvalLet.objects.filter(to_id=1, is_send=True, is_read=False).all().order_by("-id")
#     context = {
#         'group': group, 'objects': objects,
#         'title': 'Pedidu Aprovasaun ToR', 'legend': 'Pedidu Aprovasaun ToR'
#     }
#     return render(request, 'notif_gab/eval_list.html', context)
# # PROC
# @login_required
# @allowed_users(allowed_roles=['gab'])
# def notifGabProcList(request):
#     group = request.user.groups.all()[0].name
#     objects1 = ProcLet.objects.filter(to_id=1, is_req=True, is_send=True, is_read=False).all().order_by("date","id")
#     objects2 = ProcLet.objects.filter(to_id=1, is_req=False, is_send=True, is_read=False).all().order_by("date","id")
#     context = {
#         'group': group, 'objects1':objects1, 'objects2':objects2,
#         'title': 'Karta Akompanhamentu Tender', 'legend': 'Karta Akompanhamentu Tender'
#     }
#     return render(request, 'notif_gab/proc_list.html', context)
# # INV
# @login_required
# @allowed_users(allowed_roles=['gab'])
# def notifGabInvList(request):
#     group = request.user.groups.all()[0].name
#     objects = InvLet.objects.filter((Q(is_send=True, is_read=False)|Q(is_back=True)), to_id=5).all().order_by('-id')
#     compcont = ContractComp.objects.all()
#     context = {
#         'group': group, 'objects': objects,'compcont':compcont,
#         'title': 'Invoice Foun', 'legend': 'Invoice Foun'
#     }
#     return render(request, 'notif_gab/inv_list.html', context)

# @login_required
# @allowed_users(allowed_roles=['gab'])
# def notifGabInvDet(request, hashid):
#     group = request.user.groups.all()[0].name
#     obj = get_object_or_404(InvLet, hashed=hashid)
#     inv = obj.inv
#     cont = inv.cont
#     proj = cont.project
#     compcont = ContractComp.objects.filter(contract=cont).first()
#     track = InvTrack.objects.filter(inv=inv).first()
#     context = {
#         'group': group, 'obj': obj, 'inv': inv, 'cont': cont, 'proj': proj, 'track': track,'compcont':compcont,
#         'title': 'Detalha Karta', 'legend': 'Detalha Karta'
#     }
#     return render(request, 'notif_gab/inv_det.html', context)
# ###

# ============================================================
# GAB ROLES
# ============================================================

GAB_ROLES = [
    "sigp_gab",
    "sigp_gab_s",
]


# ============================================================
# GAB CPV API
# ============================================================

class notifGabCPV(APIView):

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

        if not any(role in group for role in GAB_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = CPV.objects.filter(
            is_dgaf=False,
            is_send=True,
            is_appr=False
        ).count()

        return Response({
            "value": total
        })


# ============================================================
# GAB EVAL API
# ============================================================

class notifGabEval(APIView):

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

        if not any(role in group for role in GAB_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = EvalLet.objects.filter(
            to_id=1,
            is_send=True,
            is_read=False
        ).count()

        return Response({
            "value": total
        })


# ============================================================
# GAB PROCUREMENT API
# ============================================================

class notifGabProc(APIView):

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

        if not any(role in group for role in GAB_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = ProcLet.objects.filter(
            to_id=1,
            is_send=True,
            is_read=False
        ).count()

        return Response({
            "value": total
        })


# ============================================================
# GAB INVOICE API
# ============================================================

class notifGabInv(APIView):

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

        if not any(role in group for role in GAB_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = InvLet.objects.filter(
            Q(
                is_send=True,
                is_read=False
            ) |
            Q(is_back=True),
            to_id=5
        ).count()

        return Response({
            "value": total
        })


# ============================================================
# GAB CPV LIST
# ============================================================

def notifGabCPVList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in GAB_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = (
        CPV.objects
        .filter(
            is_dgaf=False,
            is_send=True,
            is_appr=False
        )
        .order_by("-date")
    )

    context = {
        "group": group,
        "objects": objects,
        "title": "Pedidu Aprovasaun CPV",
        "legend": "Pedidu Aprovasaun CPV",
    }

    return render(
        request,
        "notif_gab/cpv_list.html",
        context
    )


# ============================================================
# GAB EVAL LIST
# ============================================================

def notifGabEvalList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in GAB_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = (
        EvalLet.objects
        .filter(
            to_id=1,
            is_send=True,
            is_read=False
        )
        .order_by("-id")
    )

    context = {
        "group": group,
        "objects": objects,
        "title": "Pedidu Aprovasaun ToR",
        "legend": "Pedidu Aprovasaun ToR",
    }

    return render(
        request,
        "notif_gab/eval_list.html",
        context
    )


# ============================================================
# GAB PROCUREMENT LIST
# ============================================================

def notifGabProcList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in GAB_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects1 = (
        ProcLet.objects
        .filter(
            to_id=1,
            is_req=True,
            is_send=True,
            is_read=False
        )
        .order_by("date", "id")
    )

    objects2 = (
        ProcLet.objects
        .filter(
            to_id=1,
            is_req=False,
            is_send=True,
            is_read=False
        )
        .order_by("date", "id")
    )

    context = {
        "group": group,
        "objects1": objects1,
        "objects2": objects2,
        "title": "Karta Akompanhamentu Tender",
        "legend": "Karta Akompanhamentu Tender",
    }

    return render(
        request,
        "notif_gab/proc_list.html",
        context
    )


# ============================================================
# GAB INVOICE LIST
# ============================================================

def notifGabInvList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in GAB_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = (
        InvLet.objects
        .filter(
            Q(
                is_send=True,
                is_read=False
            ) |
            Q(is_back=True),
            to_id=5
        )
        .order_by("-id")
    )

    compcont = ContractComp.objects.all()

    context = {
        "group": group,
        "objects": objects,
        "compcont": compcont,
        "title": "Invoice Foun",
        "legend": "Invoice Foun",
    }

    return render(
        request,
        "notif_gab/inv_list.html",
        context
    )


# ============================================================
# GAB INVOICE DETAIL
# ============================================================

def notifGabInvDet(request, hashid):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in GAB_ROLES):
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
        "title": "Detalha Karta",
        "legend": "Detalha Karta",
    }

    return render(
        request,
        "notif_gab/inv_det.html",
        context
    )