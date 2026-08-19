from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from eval.models import Eval, EvalLet
from invoice.models import InvLet, InvTrack
from contract.models import ContractComp

# #
# class notifUVIPEval(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot1 = Eval.objects.filter((\
#             Q(is_send=True, is_read=False)|\
#             Q(is_appr=True, is_let_appr=False, is_end=False)|\
#             Q(is_appr=True, is_let_appr=True, is_end=False))).all().count()
#         tot2 = EvalLet.objects.filter(is_back=True).all().count()
#         tot = tot1+tot2
#         return Response({'value':tot})

# class notifUVIPInv(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = InvLet.objects.filter((Q(to_id=4, is_send=True, is_read=False)|Q(to_id=5, is_back=True))).all().count()
#         return Response({'value':tot})
# ###
# # Eval
# @login_required
# @allowed_users(allowed_roles=['uivp'])
# def notifUVIPEvalList(request):
#     group = request.user.groups.all()[0].name
#     objects1 = Eval.objects.filter((Q(is_send=True, is_read=False)|\
#                 Q(is_appr=True, is_let_appr=False, is_end=False)|\
#                 Q(is_appr=True, is_let_appr=True, is_end=False))).all().order_by("-date")
#     objects2 = EvalLet.objects.filter(is_back=True).all().order_by("-date")
    
    
#     context = {
#         'group': group, 'objects1':objects1, 'objects2':objects2, 
#         'title': 'Avaliasaun ToR', 'legend': 'Avaliasaun ToR'
#     }
#     return render(request, 'notif_uvip/eval_list.html', context)

# # Inv
# @login_required
# @allowed_users(allowed_roles=['uivp'])
# def notifUVIPInvList(request):
#     group = request.user.groups.all()[0].name
#     objects = InvLet.objects.filter((Q(to_id=4, is_send=True, is_read=False)|Q(to_id=5, is_back=True))).all().order_by("-date")
#     compcont = ContractComp.objects.all()
#     context = {
#         'group': group, 'objects':objects,'compcont':compcont,
#         'title': 'Resibu Tama', 'legend': 'Resibu Tama'
#     }
#     return render(request, 'notif_uvip/inv_list.html', context)

# @login_required
# @allowed_users(allowed_roles=['uivp'])
# def notifUVIPInvDet(request, hashid):
#     group = request.user.groups.all()[0].name
#     obj = get_object_or_404(InvLet, hashed=hashid)
#     inv = obj.inv
#     cont = inv.cont
#     proj = cont.project
#     compcont = ContractComp.objects.filter(contract=cont).first()
#     track = InvTrack.objects.filter(inv=inv).first()
#     context = {
#         'group': group, 'obj': obj, 'inv': inv, 'cont': cont, 'proj': proj, 'track': track,'compcont':compcont,
#         'title': 'Detalha Karta', 'legend': 'Detallu Karta'
#     }
#     return render(request, 'notif_uvip/inv_det.html', context)

UVIP_ROLES = [
    "sigp_uvip",
    "sigp_uvip_s",
]


class notifUVIPEval(APIView):

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

        if not any(role in group for role in UVIP_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        tot1 = Eval.objects.filter(
            Q(is_send=True, is_read=False) |
            Q(
                is_appr=True,
                is_let_appr=False,
                is_end=False
            ) |
            Q(
                is_appr=True,
                is_let_appr=True,
                is_end=False
            )
        ).count()

        tot2 = EvalLet.objects.filter(
            is_back=True
        ).count()

        total = tot1 + tot2

        return Response({
            "value": total
        })


class notifUVIPInv(APIView):

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

        if not any(role in group for role in UVIP_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = InvLet.objects.filter(
            Q(
                to_id=4,
                is_send=True,
                is_read=False
            ) |
            Q(
                to_id=5,
                is_back=True
            )
        ).count()

        return Response({
            "value": total
        })


# ============================================================
# UVIP EVAL LIST
# ============================================================

def notifUVIPEvalList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in UVIP_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects1 = (
        Eval.objects
        .filter(
            Q(is_send=True, is_read=False) |
            Q(
                is_appr=True,
                is_let_appr=False,
                is_end=False
            ) |
            Q(
                is_appr=True,
                is_let_appr=True,
                is_end=False
            )
        )
        .order_by("-date")
    )

    objects2 = (
        EvalLet.objects
        .filter(is_back=True)
        .order_by("-date")
    )

    context = {
        "group": group,
        "objects1": objects1,
        "objects2": objects2,
        "title": "Avaliasaun ToR",
        "legend": "Avaliasaun ToR",
    }

    return render(
        request,
        "notif_uvip/eval_list.html",
        context
    )


# ============================================================
# UVIP INVOICE LIST
# ============================================================

def notifUVIPInvList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in UVIP_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = (
        InvLet.objects
        .filter(
            Q(
                to_id=4,
                is_send=True,
                is_read=False
            ) |
            Q(
                to_id=5,
                is_back=True
            )
        )
        .order_by("-date")
    )

    compcont = ContractComp.objects.all()

    context = {
        "group": group,
        "objects": objects,
        "compcont": compcont,
        "title": "Resibu Tama",
        "legend": "Resibu Tama",
    }

    return render(
        request,
        "notif_uvip/inv_list.html",
        context
    )


# ============================================================
# UVIP INVOICE DETAIL
# ============================================================

def notifUVIPInvDet(request, hashid):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in UVIP_ROLES):
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
        "legend": "Detallu Karta",
    }

    return render(
        request,
        "notif_uvip/inv_det.html",
        context
    )