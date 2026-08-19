from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from finance.models import CPVLetter, CPVReq, CPV
from invoice.models import InvLet, InvTrack
from proc.models import ProcLet
from contract.models import ContractComp

# class notifDNOFCPVReq(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot1 = CPVReq.objects.filter((Q(is_back=True)|Q(is_appr=True, is_end=False))).all().count()
#         tot2 = ProcLet.objects.filter(to_id=4, is_send=True, is_read=False).all().count()
#         tot = tot1+tot2
#         return Response({'value':tot})

# class notifDNOFCPV(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = CPV.objects.filter((Q(is_back=True)|Q(cpvtrack__is_dgaf_out=True, is_end=False))).all().count()
#         return Response({'value':tot})

# class notifDNOFInv(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = InvLet.objects.filter(to_id=2, is_send=True, is_read=False).all().count()
#         return Response({'value':tot})
# ### CPV Req
# @login_required
# @allowed_users(allowed_roles=['dnof'])
# def notifDNOFCPVReqList(request):
#     group = request.user.groups.all()[0].name
#     objects1 = CPVReq.objects.filter((Q(is_back=True)|Q(is_appr=True, is_end=False))).all().order_by('-date')
#     objects2 = ProcLet.objects.filter(to_id=4, is_send=True, is_read=False).all().order_by('-id')
#     context = {
#         'group': group, 'objects1': objects1, 'objects2':objects2,
#         'title': 'Rekizasaun CPV - Fila', 'legend': 'Rekizasaun CPV - Fila'
#     }
#     return render(request, 'notif_dnof/cpv_req_list.html', context)
# # CPV
# @login_required
# @allowed_users(allowed_roles=['dnof'])
# def notifDNOFCPVList(request):
#     group = request.user.groups.all()[0].name
#     objects1 = CPV.objects.filter(is_back=True).all().order_by('-date')
#     objects2 = CPVLetter.objects.filter(is_send=True, is_read=False).all().order_by('-date')
#     context = {
#         'group': group, 'objects1': objects1, 'objects2': objects2,
#         'title': 'CPV Fila - Despaxu', 'legend': 'CPV Fila - Despaxu'
#     }
#     return render(request, 'notif_dnof/cpv_list.html', context)
# # INV
# @login_required
# @allowed_users(allowed_roles=['dnof'])
# def notifDNOFInvList(request):
#     group = request.user.groups.all()[0].name
#     objects = InvLet.objects.filter(to_id=2, is_send=True, is_read=False).all().order_by('-id')
#     compcont = ContractComp.objects.all()
#     context = {
#         'group': group, 'objects': objects,'compcont':compcont,
#         'title': 'Recibu Foun', 'legend': 'Recibu Foun'
#     }
#     return render(request, 'notif_dnof/inv_list.html', context)

# @login_required
# @allowed_users(allowed_roles=['dnof'])
# def notifDNOFInvDet(request, hashid):
#     group = request.user.groups.all()[0].name
#     obj = get_object_or_404(InvLet, hashed=hashid)
#     inv = obj.inv
#     cont = inv.cont
#     proj = cont.project
#     compcont = ContractComp.objects.filter(contract=cont).first()
#     track = InvTrack.objects.filter(inv=inv).first()
#     context = {
#         'group':group, 'obj':obj, 'inv':inv, 'cont':cont, 'proj':proj, 'track':track, 'compcont':compcont,
#         'title': 'Detallu Karta', 'legend': 'Detallu Karta'
#     }
#     return render(request, 'notif_dnof/inv_det.html', context)

DNOF_ROLES = ["sigp_dnof", "sigp_dnof_s"]
# ============================================================
# DNOF ROLES
# ============================================================

DNOF_ROLES = [
    "sigp_dnof",
    "sigp_dnof_s",
]


# ============================================================
# DNOF CPV REQUEST API
# ============================================================

class notifDNOFCPVReq(APIView):

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

        if not any(role in group for role in DNOF_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        tot1 = CPVReq.objects.filter(
            Q(is_back=True) |
            Q(
                is_appr=True,
                is_end=False
            )
        ).count()

        tot2 = ProcLet.objects.filter(
            to_id=4,
            is_send=True,
            is_read=False
        ).count()

        total = tot1 + tot2

        return Response({
            "value": total
        })


# ============================================================
# DNOF CPV API
# ============================================================

class notifDNOFCPV(APIView):

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

        if not any(role in group for role in DNOF_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = CPV.objects.filter(
            Q(is_back=True) |
            Q(
                cpvtrack__is_dgaf_out=True,
                is_end=False
            )
        ).count()

        return Response({
            "value": total
        })


# ============================================================
# DNOF INVOICE API
# ============================================================

class notifDNOFInv(APIView):

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

        if not any(role in group for role in DNOF_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = InvLet.objects.filter(
            to_id=2,
            is_send=True,
            is_read=False
        ).count()

        return Response({
            "value": total
        })


# ============================================================
# DNOF CPV REQUEST LIST
# ============================================================

def notifDNOFCPVReqList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in DNOF_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects1 = (
        CPVReq.objects
        .filter(
            Q(is_back=True) |
            Q(
                is_appr=True,
                is_end=False
            )
        )
        .order_by("-date")
    )

    objects2 = (
        ProcLet.objects
        .filter(
            to_id=4,
            is_send=True,
            is_read=False
        )
        .order_by("-id")
    )

    context = {
        "group": group,
        "objects1": objects1,
        "objects2": objects2,
        "title": "Rekizasaun CPV - Fila",
        "legend": "Rekizasaun CPV - Fila",
    }

    return render(
        request,
        "notif_dnof/cpv_req_list.html",
        context
    )


# ============================================================
# DNOF CPV LIST
# ============================================================

def notifDNOFCPVList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in DNOF_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects1 = (
        CPV.objects
        .filter(is_back=True)
        .order_by("-date")
    )

    objects2 = (
        CPVLetter.objects
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
        "title": "CPV Fila - Despaxu",
        "legend": "CPV Fila - Despaxu",
    }

    return render(
        request,
        "notif_dnof/cpv_list.html",
        context
    )


# ============================================================
# DNOF INVOICE LIST
# ============================================================

def notifDNOFInvList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in DNOF_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = (
        InvLet.objects
        .filter(
            to_id=2,
            is_send=True,
            is_read=False
        )
        .order_by("-id")
    )

    compcont = ContractComp.objects.all()

    context = {
        "group": group,
        "objects": objects,
        "compcont": compcont,
        "title": "Recibu Foun",
        "legend": "Recibu Foun",
    }

    return render(
        request,
        "notif_dnof/inv_list.html",
        context
    )


# ============================================================
# DNOF INVOICE DETAIL
# ============================================================

def notifDNOFInvDet(request, hashid):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in DNOF_ROLES):
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
        "notif_dnof/inv_det.html",
        context
    )