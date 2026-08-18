from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from invoice.models import InvLet, InvTrack
from conf.user_utils import c_user_sup
from contract.models import ContractComp

# #
# class notifSUPInv(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         mun = c_user_sup(request.user)
#         tot = InvLet.objects.filter(mun=mun, is_back=True).all().count()
#         return Response({'value':tot})
# ###
# # Inv
# @login_required
# @allowed_users(allowed_roles=['sup'])
# def notifSUPInvList(request):
#     group = request.user.groups.all()[0].name
#     mun = c_user_sup(request.user)
#     objects = InvLet.objects.filter(mun=mun, is_back=True).all().order_by("-date")
#     compcont = ContractComp.objects.all()
#     context = {
#         'group': group, 'objects':objects,'compcont':compcont,
#         'title': 'Invoice Tama', 'legend': 'Invoice Tama'
#     }
#     return render(request, 'notif_sup/inv_list.html', context)

SUP_ROLES = [
    "sigp_sup",
]


class notifSUPInv(APIView):

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

        if not any(role in group for role in SUP_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        # Municipality from SSO
        mun_id = getattr(portal_user, "mun_id", None)

        if not mun_id:
            return Response({
                "value": 0
            })

        total = InvLet.objects.filter(
            mun_id=mun_id,
            is_back=True
        ).count()

        return Response({
            "value": total
        })


# ============================================================
# SUPERVISOR INVOICE LIST
# ============================================================

def notifSUPInvList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in SUP_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    # Municipality from SSO
    mun_id = getattr(portal_user, "mun_id", None)

    if mun_id:
        objects = (
            InvLet.objects
            .filter(
                mun_id=mun_id,
                is_back=True
            )
            .order_by("-date")
        )
    else:
        objects = InvLet.objects.none()

    compcont = ContractComp.objects.all()

    context = {
        "group": group,
        "objects": objects,
        "compcont": compcont,
        "title": "Invoice Tama",
        "legend": "Invoice Tama",
    }

    return render(
        request,
        "notif_sup/inv_list.html",
        context
    )