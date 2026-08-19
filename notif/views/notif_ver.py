from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from ver.models import Ver, VerSecEng,VerSecEngEmployee
from conf.user_utils import c_user_eng, c_user_sec,c_user_pos
from contract.models import ContractComp

# ## UVIP
# class notifUVIPVer(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         #tot1 = Ver.objects.filter(is_back=False).all().count()
#         tot2 = VerSecEng.objects.filter(is_back=True, is_back_read=False).all().count()
#         tot = tot2
#         return Response({'value':tot})

# @login_required
# @allowed_users(allowed_roles=['uivp'])
# def notifUVIPVerList(request):
#     group = request.user.groups.all()[0].name
#     objects1 = Ver.objects.filter(is_back=False).all().order_by('-start_date')
#     objects2 = VerSecEng.objects.filter(is_back=True, is_back_read=False).all().order_by('-date')
#     context = {
#         'group': group, 'objects1': objects1, 'objects2': objects2,
#         'title': 'Notifikasaun', 'legend': 'Notifikasaun'
#     }
#     return render(request, 'notif_ver/uvip_ver_list.html', context)
# ### SEC
# class notifSECVer(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         sec = c_user_sec(request.user)
#         epos=c_user_pos(request.user)
#         tot1 = Ver.objects.filter(sec=sec, epos__cat=epos, is_send=True, is_read=False).all().count()
#         tot2 = VerSecEng.objects.filter(sec=sec, epos__cat=epos, is_eng_back=True, is_eng_read=False).all().count()
#         tot = tot1+tot2
#         return Response({'value':tot})

# @login_required
# @allowed_users(allowed_roles=['sec'])
# def notifSECVerList(request):
#     group = request.user.groups.all()[0].name
#     sec = c_user_sec(request.user)
#     epos=c_user_pos(request.user)
#     objects1 = Ver.objects.filter(sec=sec, epos__cat=epos,is_send=True, is_read=False).all().order_by('-start_date')
#     objects2 = VerSecEng.objects.filter(sec=sec, epos__cat=epos,is_eng_back=True, is_eng_read=False).all().order_by('-date')
#     objects3 = VerSecEngEmployee.objects.all()
#     context = {
#         'group': group, 'objects1': objects1, 'objects2': objects2,'objects3':objects3,
#         'title': 'Despaxu Foun - Verifikasaun', 'legend': 'Despaxu Foun - Verifikasaun'
#     }
#     return render(request, 'notif_ver/sec_ver_list.html', context)
# ### ENG
# class notifENGVer(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         eng = c_user_eng(request.user)
#         tot = VerSecEng.objects.filter(to=eng, is_send=True, is_send_read=False).all().count()
#         return Response({'value':tot})

# @login_required
# @allowed_users(allowed_roles=['eng'])
# def notifENGVerList(request):
#     group = request.user.groups.all()[0].name
#     eng = c_user_eng(request.user)
#     objects = VerSecEng.objects.filter(to=eng, is_send=True, is_send_read=False).all().order_by('-date')
#     object1 = VerSecEngEmployee.objects.all()
#     objects3 = ContractComp.objects.all()
#     context = {
#         'group': group, 'objects': objects, 'object1':object1, 'objects3':objects3,
#         'title': 'Despaxu Foun - Verifikasaun', 'legend': 'Despaxu Foun - Verifikasaun'
#     }
#     return render(request, 'notif_ver/eng_ver_list.html', context)


UVIP_ROLES = ["sigp_uvip", "sigp_uvip_s"]
SEC_ROLES = ["sigp_sec"]
ENG_ROLES = ["sigp_eng"]


# ============================================================
# UVIP VERIFICATION
# ============================================================

class notifUVIPVer(APIView):

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

        total = VerSecEng.objects.filter(
            is_back=True,
            is_back_read=False
        ).count()

        return Response({
            "value": total
        })


def notifUVIPVerList(request):

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
        Ver.objects
        .filter(is_back=False)
        .order_by("-start_date")
    )

    objects2 = (
        VerSecEng.objects
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
        "notif_ver/uvip_ver_list.html",
        context
    )


# ============================================================
# SEC VERIFICATION
# ============================================================

class notifSECVer(APIView):

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

        tot1 = Ver.objects.filter(
            sec_id=sec_id,
            epos__cat=epos,
            is_send=True,
            is_read=False
        ).count()

        tot2 = VerSecEng.objects.filter(
            sec_id=sec_id,
            epos__cat=epos,
            is_eng_back=True,
            is_eng_read=False
        ).count()

        total = tot1 + tot2

        return Response({
            "value": total
        })


def notifSECVerList(request):

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
            Ver.objects
            .filter(
                sec_id=sec_id,
                epos__cat=epos,
                is_send=True,
                is_read=False
            )
            .order_by("-start_date")
        )

        objects2 = (
            VerSecEng.objects
            .filter(
                sec_id=sec_id,
                epos__cat=epos,
                is_eng_back=True,
                is_eng_read=False
            )
            .order_by("-date")
        )

    else:
        objects1 = Ver.objects.none()
        objects2 = VerSecEng.objects.none()

    objects3 = VerSecEngEmployee.objects.all()

    context = {
        "group": group,
        "objects1": objects1,
        "objects2": objects2,
        "objects3": objects3,
        "title": "Despaxu Foun - Verifikasaun",
        "legend": "Despaxu Foun - Verifikasaun",
    }

    return render(
        request,
        "notif_ver/sec_ver_list.html",
        context
    )


# ============================================================
# ENG VERIFICATION
# ============================================================

class notifENGVer(APIView):

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

        if not eng_id:
            return Response({
                "value": 0
            })

        total = VerSecEng.objects.filter(
            to_id=eng_id,
            is_send=True,
            is_send_read=False
        ).count()

        return Response({
            "value": total
        })


def notifENGVerList(request):

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

    if eng_id:
        objects = (
            VerSecEng.objects
            .filter(
                to_id=eng_id,
                is_send=True,
                is_send_read=False
            )
            .order_by("-date")
        )
    else:
        objects = VerSecEng.objects.none()

    object1 = VerSecEngEmployee.objects.all()
    objects3 = ContractComp.objects.all()

    context = {
        "group": group,
        "objects": objects,
        "object1": object1,
        "objects3": objects3,
        "title": "Despaxu Foun - Verifikasaun",
        "legend": "Despaxu Foun - Verifikasaun",
    }

    return render(
        request,
        "notif_ver/eng_ver_list.html",
        context
    )