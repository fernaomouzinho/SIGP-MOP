from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from eval.models import Eval, EvalLet
from invoice.models import InvLet, InvTrack
from contract.models import ContractComp

#
# class notifBDEval(APIView):
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

class notifBDEval(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        # ==========================================
        # 1. Check SSO authentication
        # ==========================================
        portal_user = getattr(request, "portal_user", None)

        if not portal_user:
            return Response(
                {"detail": "Authentication required."},
                status=401
            )

        # ==========================================
        # 2. Get SSO roles
        # ==========================================
        group = getattr(request, "portal_roles", [])

        if not group:
            group = request.session.get("portal_roles", [])

        # ==========================================
        # 3. Allow related role only
        # ==========================================
        if "sigp_uvip" not in group:
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        # ==========================================
        # 4. Count evaluation notifications
        # ==========================================
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

# class notifBDInv(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = InvLet.objects.filter((Q(to_id=4, is_send=True, is_read=False)|Q(to_id=5, is_back=True))).all().count()
#         return Response({'value':tot})

class notifBDInv(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        # ==========================================
        # 1. Check SSO authentication
        # ==========================================
        portal_user = getattr(request, "portal_user", None)

        if not portal_user:
            return Response(
                {"detail": "Authentication required."},
                status=401
            )

        # ==========================================
        # 2. Get SSO roles
        # ==========================================
        group = getattr(request, "portal_roles", [])

        if not group:
            group = request.session.get("portal_roles", [])

        # ==========================================
        # 3. Allow UVIP role only
        # ==========================================
        if "sigp_uvip" not in group:
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        # ==========================================
        # 4. Count invoice notifications
        # ==========================================
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
###
# # Eval
# @login_required
# @allowed_users(allowed_roles=['uivp'])
# def notifBDEvalList(request):
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

def notifBDEvalList(request):

    # ==========================================
    # 1. Check SSO authentication
    # ==========================================
    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")  # change to your SSO/login URL if needed

    # ==========================================
    # 2. Get SSO roles
    # ==========================================
    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    # ==========================================
    # 3. Allow UVIP only
    # ==========================================
    if "sigp_uvip" not in group:
        return render(
            request,
            "403.html",
            status=403
        )

    # ==========================================
    # 4. Get evaluation notifications
    # ==========================================
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

    # ==========================================
    # 5. Context
    # ==========================================
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

# Inv
# @login_required
# @allowed_users(allowed_roles=['uivp'])
# def notifBDInvList(request):
#     group = request.user.groups.all()[0].name
#     objects = InvLet.objects.filter((Q(to_id=4, is_send=True, is_read=False)|Q(to_id=5, is_back=True))).all().order_by("-date")
#     compcont = ContractComp.objects.all()
#     context = {
#         'group': group, 'objects':objects,'compcont':compcont,
#         'title': 'Resibu Tama', 'legend': 'Resibu Tama'
#     }
#     return render(request, 'notif_uvip/inv_list.html', context)

def notifBDInvList(request):

    # ==========================================
    # 1. Check SSO authentication
    # ==========================================
    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")  # or your central SSO login URL

    # ==========================================
    # 2. Get SSO roles
    # ==========================================
    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    # ==========================================
    # 3. Allow UVIP role only
    # ==========================================
    if "sigp_uvip" not in group:
        return render(
            request,
            "403.html",
            status=403
        )

    # ==========================================
    # 4. Get invoice notifications
    # ==========================================
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

    # ==========================================
    # 5. Context
    # ==========================================
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

# @login_required
# @allowed_users(allowed_roles=['uivp'])
# def notifBDInvDet(request, hashid):
#     group = request.user.groups.all()[0].name
#     obj = get_object_or_404(InvLet, hashed=hashid)
#     inv = obj.inv
#     cont = inv.cont
#     proj = cont.project
#     compcont = ContractComp.objects.filter(contract=cont).first()
#     track = InvTrack.objects.filter(inv=inv).first()
#     context = {
#         'group': group, 'obj': obj, 'inv': inv, 'cont': cont, 'proj': proj, 'track': track,
#         'title': 'Detalha Karta', 'legend': 'Detallu Karta'
#     }
#     return render(request, 'notif_uvip/inv_det.html', context)

def notifBDInvDet(request, hashid):

    # ==========================================
    # 1. Check SSO authentication
    # ==========================================
    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")  # replace with your SSO login if needed

    # ==========================================
    # 2. Get SSO roles
    # ==========================================
    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    # ==========================================
    # 3. Allow UVIP only
    # ==========================================
    if "sigp_uvip" not in group:
        return render(
            request,
            "403.html",
            status=403
        )

    # ==========================================
    # 4. Get invoice letter
    # ==========================================
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

    # ==========================================
    # 5. Context
    # ==========================================
    context = {
        "group": group,
        "obj": obj,
        "inv": inv,
        "cont": cont,
        "proj": proj,
        "compcont": compcont,
        "track": track,
        "title": "Detalha Karta",
        "legend": "Detallu Karta",
    }

    return render(
        request,
        "notif_uvip/inv_det.html",
        context
    )