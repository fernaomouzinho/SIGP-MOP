from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from finance.models import CPVReq, CPV, PO, POLetter
from proc.models import ProcLet, ProcReqTrack, ProcResTrack
from invoice.models import InvLet, InvTrack
from contract.models import ContractComp

# #
# class notifDGAFCPVReq(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = CPVReq.objects.filter(is_send=True, is_appr=False).all().count()
#         return Response({'value':tot})

# class notifDGAFCPV(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = CPV.objects.filter(is_dgaf=True, is_send=True, is_appr=False).all().count()
#         return Response({'value':tot})

# class notifDGAFPO(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = PO.objects.filter(is_send=True, is_appr=False).all().count()
#         return Response({'value':tot})

# class notifDGAFProc(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot1 = ProcReqTrack.objects.filter(is_dna_out=True, is_dgaf_in_1=False).all().count()
#         tot2 = ProcResTrack.objects.filter(is_dna_out=True, is_dgaf_in_1=False).all().count()
#         tot3 = ProcLet.objects.filter((Q(is_back=True)|Q(to_id=2, is_send=True, is_read=False))).all().count()
#         tot = tot1+tot2+tot3
#         return Response({'value':tot})

# class notifDGAFInv(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = InvLet.objects.filter(to_id=3, is_send=True, is_read=False).all().count()
#         return Response({'value':tot})
# ###
# # CPV Req
# @login_required
# @allowed_users(allowed_roles=['dgaf'])
# def notifDGAFCPVReqList(request):
#     group = request.user.groups.all()[0].name
#     objects = CPVReq.objects.filter(is_send=True, is_appr=False).all().order_by('-date')
#     context = {
#         'group': group, 'objects': objects,
#         'title': 'Rekizasaun CPV', 'legend': 'Rekizasaun CPV'
#     }
#     return render(request, 'notif_dgaf/cpv_req_list.html', context)
# # CPV
# @login_required
# @allowed_users(allowed_roles=['dgaf'])
# def notifDGAFCPVList(request):
#     group = request.user.groups.all()[0].name
#     objects = CPV.objects.filter(is_dgaf=True, is_send=True, is_appr=False).all().order_by('-date')
#     context = {
#         'group': group, 'objects': objects,
#         'title': 'Lista CPV', 'legend': 'Lista CPV'
#     }
#     return render(request, 'notif_dgaf/cpv_list.html', context)
# # po
# @login_required
# @allowed_users(allowed_roles=['dgaf'])
# def notifDGAFPOList(request):
#     group = request.user.groups.all()[0].name
#     objects = PO.objects.filter(is_send=True, is_appr=False).all().order_by('-date')
#     context = {
#         'group': group, 'objects': objects,
#         'title': 'Lista PO', 'legend': 'Lista PO'
#     }
#     return render(request, 'notif_dgaf/po_list.html', context)

# @login_required
# @allowed_users(allowed_roles=['dgaf'])
# def notifDGAFPODet(request, hashid):
#     group = request.user.groups.all()[0].name
#     po = get_object_or_404(PO, hashed=hashid)
#     cont = po.cont
#     proj = cont.project
#     lett = POLetter.objects.filter(po=po).first()
#     context = {
#         'group':group, 'po':po, 'cont':cont, 'proj':proj, 'lett':lett,
#         'title':'Detallu PO', 'legend':'Detallu PO'
#     }
#     return render(request, 'notif_dgaf/po_det.html', context)
# # proc
# @login_required
# @allowed_users(allowed_roles=['dgaf'])
# def notifDGAFProcList(request):
#     group = request.user.groups.all()[0].name
#     objects1 = ProcReqTrack.objects.filter(is_dna_out=True, is_dgaf_in_1=False).all()
#     objects2 = ProcResTrack.objects.filter(is_dna_out=True, is_dgaf_in_1=False).all()
#     objects3 = ProcLet.objects.filter((Q(is_back=True)|Q(to_id=2, is_send=True, is_read=False)), is_req=True).all()
#     objects4 = ProcLet.objects.filter((Q(is_back=True)|Q(to_id=2, is_send=True, is_read=False)), is_req=False).all()
#     context = {
#         'group':group, 'objects1':objects1, 'objects2':objects2, 'objects3':objects3, 'objects4':objects4,
#         'title':'Tender', 'legend': 'Tender'
#     }
#     return render(request, 'notif_dgaf/proc_list.html', context)
# # INV
# @login_required
# @allowed_users(allowed_roles=['dgaf'])
# def notifDGAFInvList(request):
#     group = request.user.groups.all()[0].name
#     objects = InvLet.objects.filter(to_id=3, is_send=True, is_read=False).all().order_by('-id')
#     compcont = ContractComp.objects.all()
#     context = {
#         'group': group, 'objects': objects,'compcont':compcont,
#         'title': 'Resibu Foun', 'legend': 'Resibu Foun'
#     }
#     return render(request, 'notif_dgaf/inv_list.html', context)

# @login_required
# @allowed_users(allowed_roles=['dgaf'])
# def notifDGAFInvDet(request, hashid):
#     group = request.user.groups.all()[0].name
#     obj = get_object_or_404(InvLet, hashed=hashid)
#     inv = obj.inv
#     cont = inv.cont
#     proj = cont.project
#     compcont = ContractComp.objects.filter(contract=cont).first()
#     track = InvTrack.objects.filter(inv=inv).first()
#     context = {
#         'group': group, 'obj': obj, 'inv': inv, 'cont': cont, 'proj': proj, 'track': track,'compcont':compcont,
#         'title': 'Detallu Karta', 'legend': 'Detallu Karta'
#     }
#     return render(request, 'notif_dgaf/inv_det.html', context)


# ============================================================
# DGAF NOTIFICATION API
# ============================================================

class notifDGAFCPVReq(APIView):

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

        if not any(
            role in group
            for role in ["sigp_dgaf", "sigp_dgaf_s"]
        ):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = CPVReq.objects.filter(
            is_send=True,
            is_appr=False
        ).count()

        return Response({
            "value": total
        })


class notifDGAFCPV(APIView):

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

        if not any(
            role in group
            for role in ["sigp_dgaf", "sigp_dgaf_s"]
        ):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = CPV.objects.filter(
            is_dgaf=True,
            is_send=True,
            is_appr=False
        ).count()

        return Response({
            "value": total
        })


class notifDGAFPO(APIView):

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

        if not any(
            role in group
            for role in ["sigp_dgaf", "sigp_dgaf_s"]
        ):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = PO.objects.filter(
            is_send=True,
            is_appr=False
        ).count()

        return Response({
            "value": total
        })


class notifDGAFProc(APIView):

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

        if not any(
            role in group
            for role in ["sigp_dgaf", "sigp_dgaf_s"]
        ):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        tot1 = ProcReqTrack.objects.filter(
            is_dna_out=True,
            is_dgaf_in_1=False
        ).count()

        tot2 = ProcResTrack.objects.filter(
            is_dna_out=True,
            is_dgaf_in_1=False
        ).count()

        tot3 = ProcLet.objects.filter(
            Q(is_back=True) |
            Q(
                to_id=2,
                is_send=True,
                is_read=False
            )
        ).count()

        total = tot1 + tot2 + tot3

        return Response({
            "value": total
        })


class notifDGAFInv(APIView):

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

        if not any(
            role in group
            for role in ["sigp_dgaf", "sigp_dgaf_s"]
        ):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = InvLet.objects.filter(
            to_id=3,
            is_send=True,
            is_read=False
        ).count()

        return Response({
            "value": total
        })


# ============================================================
# DGAF CPV REQUEST LIST
# ============================================================

def notifDGAFCPVReqList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(
        role in group
        for role in ["sigp_dgaf", "sigp_dgaf_s"]
    ):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = (
        CPVReq.objects
        .filter(
            is_send=True,
            is_appr=False
        )
        .order_by("-date")
    )

    context = {
        "group": group,
        "objects": objects,
        "title": "Rekizasaun CPV",
        "legend": "Rekizasaun CPV",
    }

    return render(
        request,
        "notif_dgaf/cpv_req_list.html",
        context
    )


# ============================================================
# DGAF CPV LIST
# ============================================================

def notifDGAFCPVList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(
        role in group
        for role in ["sigp_dgaf", "sigp_dgaf_s"]
    ):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = (
        CPV.objects
        .filter(
            is_dgaf=True,
            is_send=True,
            is_appr=False
        )
        .order_by("-date")
    )

    context = {
        "group": group,
        "objects": objects,
        "title": "Lista CPV",
        "legend": "Lista CPV",
    }

    return render(
        request,
        "notif_dgaf/cpv_list.html",
        context
    )


# ============================================================
# DGAF PO LIST
# ============================================================

def notifDGAFPOList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(
        role in group
        for role in ["sigp_dgaf", "sigp_dgaf_s"]
    ):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = (
        PO.objects
        .filter(
            is_send=True,
            is_appr=False
        )
        .order_by("-date")
    )

    context = {
        "group": group,
        "objects": objects,
        "title": "Lista PO",
        "legend": "Lista PO",
    }

    return render(
        request,
        "notif_dgaf/po_list.html",
        context
    )


# ============================================================
# DGAF PO DETAIL
# ============================================================

def notifDGAFPODet(request, hashid):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(
        role in group
        for role in ["sigp_dgaf", "sigp_dgaf_s"]
    ):
        return render(
            request,
            "403.html",
            status=403
        )

    po = get_object_or_404(
        PO,
        hashed=hashid
    )

    cont = po.cont
    proj = cont.project

    lett = (
        POLetter.objects
        .filter(po=po)
        .first()
    )

    context = {
        "group": group,
        "po": po,
        "cont": cont,
        "proj": proj,
        "lett": lett,
        "title": "Detallu PO",
        "legend": "Detallu PO",
    }

    return render(
        request,
        "notif_dgaf/po_det.html",
        context
    )


# ============================================================
# DGAF PROCUREMENT LIST
# ============================================================

def notifDGAFProcList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(
        role in group
        for role in ["sigp_dgaf", "sigp_dgaf_s"]
    ):
        return render(
            request,
            "403.html",
            status=403
        )

    objects1 = ProcReqTrack.objects.filter(
        is_dna_out=True,
        is_dgaf_in_1=False
    )

    objects2 = ProcResTrack.objects.filter(
        is_dna_out=True,
        is_dgaf_in_1=False
    )

    objects3 = ProcLet.objects.filter(
        Q(is_back=True) |
        Q(
            to_id=2,
            is_send=True,
            is_read=False
        ),
        is_req=True
    )

    objects4 = ProcLet.objects.filter(
        Q(is_back=True) |
        Q(
            to_id=2,
            is_send=True,
            is_read=False
        ),
        is_req=False
    )

    context = {
        "group": group,
        "objects1": objects1,
        "objects2": objects2,
        "objects3": objects3,
        "objects4": objects4,
        "title": "Tender",
        "legend": "Tender",
    }

    return render(
        request,
        "notif_dgaf/proc_list.html",
        context
    )


# ============================================================
# DGAF INVOICE LIST
# ============================================================

def notifDGAFInvList(request):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(
        role in group
        for role in ["sigp_dgaf", "sigp_dgaf_s"]
    ):
        return render(
            request,
            "403.html",
            status=403
        )

    objects = (
        InvLet.objects
        .filter(
            to_id=3,
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
        "title": "Resibu Foun",
        "legend": "Resibu Foun",
    }

    return render(
        request,
        "notif_dgaf/inv_list.html",
        context
    )


# ============================================================
# DGAF INVOICE DETAIL
# ============================================================

def notifDGAFInvDet(request, hashid):

    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    if not any(
        role in group
        for role in ["sigp_dgaf", "sigp_dgaf_s"]
    ):
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
        "notif_dgaf/inv_det.html",
        context
    )