from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from conf.decorators import allowed_users
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from finance.models import EV
from invoice.models import InvLet, InvTrack
from proc.models import ProcLet

# class notifDNOFBOEv(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = EV.objects.filter(is_send=True, is_read=False).all().count()
#         return Response({'value':tot})

# # EV
# @login_required
# @allowed_users(allowed_roles=['dnof-bo'])
# def notifDNOFBOEvList(request):
#     group = request.user.groups.all()[0].name
#     objects = EV.objects.filter(is_send=True, is_read=False).all().order_by('-id')
#     context = {
#         'group': group, 'objects': objects,
#         'title': 'Resibu Foun', 'legend': 'Resibu Foun'
#     }
#     return render(request, 'notif_dnof_bo/inv_list.html', context)

DNOF_BO_ROLES = [
    "sigp_dnof_bo",
]


class notifDNOFBOEv(APIView):

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

        if not any(role in group for role in DNOF_BO_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = EV.objects.filter(
            is_send=True,
            is_read=False
        ).count()

        return Response({
            "value": total
        })


# ============================================================
# DNOF BACK OFFICE EV LIST
# ============================================================

def notifDNOFBOEvList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in DNOF_BO_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = (
        EV.objects
        .filter(
            is_send=True,
            is_read=False
        )
        .order_by("-id")
    )

    context = {
        "group": group,
        "objects": objects,
        "title": "Resibu Foun",
        "legend": "Resibu Foun",
    }

    return render(
        request,
        "notif_dnof_bo/inv_list.html",
        context
    )