from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from insp.models import Insp, InspSecEng,InspSecEngEmployee
from conf.user_utils import c_user_eng, c_user_sec, c_user_pos

# ## UVIP
# class notifUVIPInsp(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot1 = Insp.objects.filter(is_back=True).all().count()
#         tot2 = InspSecEng.objects.filter(is_back=True, is_back_read=False).all().count()
#         tot = tot1+tot2
#         return Response({'value':tot})

# @login_required
# @allowed_users(allowed_roles=['uivp'])
# def notifUVIPInspList(request):
#     group = request.user.groups.all()[0].name
#     objects1 = Insp.objects.filter(is_back=True).all().order_by('-start_date')
#     objects2 = InspSecEng.objects.filter(is_back=True, is_back_read=False).all().order_by('-date')
#     context = {
#         'group': group, 'objects1': objects1, 'objects2': objects2,
#         'title': 'Notifikasaun', 'legend': 'Notifikasaun'
#     }
#     return render(request, 'notif_insp/uvip_insp_list.html', context)

# ### SEC
# class notifSECInsp(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         sec = c_user_sec(request.user)
#         epos=c_user_pos(request.user)
#         tot1 = Insp.objects.filter(epos__cat=epos, sec=sec, is_send=True, is_read=False).all().count()
#         tot2 = InspSecEng.objects.filter(sec=sec, is_eng_back=True, is_eng_read=False).all().count()
#         tot = tot1+tot2
#         return Response({'value':tot})

# @login_required
# @allowed_users(allowed_roles=['sec'])
# def notifSECInspList(request):
#     group = request.user.groups.all()[0].name
#     sec = c_user_sec(request.user)
#     print(sec)
#     epos=c_user_pos(request.user)
#     print(epos)
#     objects1 = Insp.objects.filter(epos__cat=epos, sec=sec,is_send=True, is_read=False).all().order_by('-start_date')
#     print("aa",objects1)
#     objects2 = InspSecEng.objects.filter(sec=sec, is_eng_back=True, is_eng_read=False).all().order_by('-date')
#     print(objects2)
#     objects3 = InspSecEngEmployee.objects.all()
#     context = {
#         'group': group, 'objects1': objects1, 'objects2': objects2,'objects3':objects3,
#         'title': 'Despaxu Foun - Inspeksaun', 'legend': 'Despaxu Foun - Inspeksaun'
#     }
#     return render(request, 'notif_insp/sec_insp_list.html', context)
# ### ENG
# class notifENGInsp(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         eng = c_user_eng(request.user)
#         epos=c_user_pos(request.user)
#         tot = InspSecEng.objects.filter(to=eng, insp__epos__cat=epos, is_send=True, is_send_read=False).all().count()
#         return Response({'value':tot})

# @login_required
# @allowed_users(allowed_roles=['eng'])
# def notifENGInspList(request):
#     group = request.user.groups.all()[0].name
#     eng = c_user_eng(request.user)
#     epos=c_user_pos(request.user)
#     objects = InspSecEng.objects.filter(to=eng, insp__epos__cat=epos, is_send=True, is_send_read=False).all().order_by('-date')
#     context = {
#         'group': group, 'objects': objects,
#         'title': 'Despaxu Foun - Inspeksaun', 'legend': 'Despaxu Foun - Inspeksaun'
#     }
#     return render(request, 'notif_insp/eng_insp_list.html', context)

# ============================================================
# ROLE SETS
# ============================================================

UVIP_ROLES = ["sigp_uvip"]
SEC_ROLES = ["sigp_sec"]
ENG_ROLES = ["sigp_eng"]


# ============================================================
# UVIP
# ============================================================

class notifUVIPInsp(APIView):

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

        tot1 = Insp.objects.filter(
            is_back=True
        ).count()

        tot2 = InspSecEng.objects.filter(
            is_back=True,
            is_back_read=False
        ).count()

        total = tot1 + tot2

        return Response({
            "value": total
        })


def notifUVIPInspList(request):

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
        Insp.objects
        .filter(is_back=True)
        .order_by("-start_date")
    )

    objects2 = (
        InspSecEng.objects
        .filter(
            is_back=True,
            is_back_read=False
        )
        .order_by("-date")
    )

    context = {
        "group": group,
        "objects1": objects1,
        "objects2": objects2,
        "title": "Notifikasaun",
        "legend": "Notifikasaun",
    }

    return render(
        request,
        "notif_insp/uvip_insp_list.html",
        context
    )


# ============================================================
# SEC
# ============================================================

class notifSECInsp(APIView):

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

        if not any(role in group for role in SEC_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        sec_id = getattr(portal_user, "sec_id", None)
        epos = getattr(portal_user, "epos_cat", None)

        if not sec_id or not epos:
            return Response({
                "value": 0
            })

        tot1 = Insp.objects.filter(
            epos__cat=epos,
            sec_id=sec_id,
            is_send=True,
            is_read=False
        ).count()

        tot2 = InspSecEng.objects.filter(
            sec_id=sec_id,
            is_eng_back=True,
            is_eng_read=False
        ).count()

        total = tot1 + tot2

        return Response({
            "value": total
        })


def notifSECInspList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in SEC_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    sec_id = getattr(portal_user, "sec_id", None)
    epos = getattr(portal_user, "epos_cat", None)

    if sec_id and epos:

        objects1 = (
            Insp.objects
            .filter(
                epos__cat=epos,
                sec_id=sec_id,
                is_send=True,
                is_read=False
            )
            .order_by("-start_date")
        )

        objects2 = (
            InspSecEng.objects
            .filter(
                sec_id=sec_id,
                is_eng_back=True,
                is_eng_read=False
            )
            .order_by("-date")
        )

    else:
        objects1 = Insp.objects.none()
        objects2 = InspSecEng.objects.none()

    objects3 = InspSecEngEmployee.objects.all()

    context = {
        "group": group,
        "objects1": objects1,
        "objects2": objects2,
        "objects3": objects3,
        "title": "Despaxu Foun - Inspeksaun",
        "legend": "Despaxu Foun - Inspeksaun",
    }

    return render(
        request,
        "notif_insp/sec_insp_list.html",
        context
    )


# ============================================================
# ENG
# ============================================================

class notifENGInsp(APIView):

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

        if not any(role in group for role in ENG_ROLES):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        eng_id = getattr(portal_user, "eng_id", None)
        epos = getattr(portal_user, "epos_cat", None)

        if not eng_id or not epos:
            return Response({
                "value": 0
            })

        total = InspSecEng.objects.filter(
            to_id=eng_id,
            insp__epos__cat=epos,
            is_send=True,
            is_send_read=False
        ).count()

        return Response({
            "value": total
        })


def notifENGInspList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(role in group for role in ENG_ROLES):
        return render(
            request,
            "403.html",
            status=403
        )

    eng_id = getattr(portal_user, "eng_id", None)
    epos = getattr(portal_user, "epos_cat", None)

    if eng_id and epos:

        objects = (
            InspSecEng.objects
            .filter(
                to_id=eng_id,
                insp__epos__cat=epos,
                is_send=True,
                is_send_read=False
            )
            .order_by("-date")
        )

    else:
        objects = InspSecEng.objects.none()

    context = {
        "group": group,
        "objects": objects,
        "title": "Despaxu Foun - Inspeksaun",
        "legend": "Despaxu Foun - Inspeksaun",
    }

    return render(
        request,
        "notif_insp/eng_insp_list.html",
        context
    )