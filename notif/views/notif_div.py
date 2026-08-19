from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from project.models import Project
from eval.models import Eval
from conf.user_utils import c_user_div
		
# #
# class notifDIVEval(APIView):
# 	authentication_classes = [SessionAuthentication, BasicAuthentication]
# 	permission_classes = [IsAuthenticated]
# 	def get(self, request, format=None):
# 		div = c_user_div(request.user)
# 		tot = Eval.objects.filter(div=div, is_appr=True, is_end=True).all().count()
# 		return Response({'value':tot})
# ###
# @login_required
# @allowed_users(allowed_roles=['div'])
# def notifDIVEvalList(request):
# 	group = request.user.groups.all()[0].name
# 	div = c_user_div(request.user)
# 	objects = Eval.objects.filter(div=div, is_appr=True, is_end=True).all().order_by('-date')
# 	context = {
# 		'group': group, 'objects': objects,
# 		'title': 'Lista ToR Aprovadu', 'legend': 'Lista ToR Aprovadu'
# 	}
# 	return render(request, 'notif_div/eval_list.html', context)

# class notifDIVpp(APIView):
# 	authentication_classes = [SessionAuthentication, BasicAuthentication]
# 	permission_classes = [IsAuthenticated]
# 	def get(self, request, format=None):
# 		tot = Project.objects.filter(is_active=True, is_read=False).all().count()
# 		return Response({'value':tot})

# ###
# @login_required
# @allowed_users(allowed_roles=['div'])
# def notifDIVProjList(request):
# 	group = request.user.groups.all()[0].name
# 	objects = Project.objects.filter(is_active=True, is_read=False).all().order_by('-datetime')
# 	context = {
# 		'group': group, 'objects': objects,
# 		'title': 'Lista Projetu', 'legend': 'Lista Projetu'
# 	}
# 	return render(request, 'notif_div/proj_list.html', context)


class notifDIVEval(APIView):

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
        # 3. Allow DIV roles
        # ==========================================
        if not any(
            role in group
            for role in ["sigp_div", "sigp_div_s"]
        ):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        # ==========================================
        # 4. Get division from SSO
        # ==========================================
        div_id = getattr(portal_user, "div_id", None)

        if not div_id:
            return Response({
                "value": 0
            })

        # ==========================================
        # 5. Count approved evaluations
        # ==========================================
        total = Eval.objects.filter(
            div_id=div_id,
            is_appr=True,
            is_end=True
        ).count()

        return Response({
            "value": total
        })
        
def notifDIVEvalList(request):

    # ==========================================
    # 1. Check SSO authentication
    # ==========================================
    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    # ==========================================
    # 2. Get SSO roles
    # ==========================================
    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    # ==========================================
    # 3. Allow DIV roles
    # ==========================================
    if not any(
        role in group
        for role in ["sigp_div", "sigp_div_s"]
    ):
        return render(
            request,
            "403.html",
            status=403
        )

    # ==========================================
    # 4. Get division from SSO
    # ==========================================
    div_id = getattr(portal_user, "div_id", None)

    if div_id:
        objects = (
            Eval.objects
            .filter(
                div_id=div_id,
                is_appr=True,
                is_end=True
            )
            .order_by("-date")
        )
    else:
        objects = Eval.objects.none()

    # ==========================================
    # 5. Context
    # ==========================================
    context = {
        "group": group,
        "objects": objects,
        "title": "Lista ToR Aprovadu",
        "legend": "Lista ToR Aprovadu",
    }

    return render(
        request,
        "notif_div/eval_list.html",
        context
    )
    
class notifDIVpp(APIView):

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
            for role in ["sigp_div", "sigp_div_s"]
        ):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        total = Project.objects.filter(
            is_active=True,
            is_read=False
        ).count()

        return Response({
            "value": total
        })
        
def notifDIVProjList(request):

    # ==========================================
    # 1. Check SSO authentication
    # ==========================================
    portal_user = getattr(request, "portal_user", None)

    if not portal_user:
        return redirect("/login/")

    # ==========================================
    # 2. Get SSO roles
    # ==========================================
    group = getattr(request, "portal_roles", [])

    if not group:
        group = request.session.get("portal_roles", [])

    # ==========================================
    # 3. Allow DIV roles
    # ==========================================
    if not any(
        role in group
        for role in ["sigp_div", "sigp_div_s"]
    ):
        return render(
            request,
            "403.html",
            status=403
        )

    # ==========================================
    # 4. Get projects
    # ==========================================
    objects = (
        Project.objects
        .filter(
            is_active=True,
            is_read=False
        )
        .order_by("-datetime")
    )

    # ==========================================
    # 5. Context
    # ==========================================
    context = {
        "group": group,
        "objects": objects,
        "title": "Lista Projetu",
        "legend": "Lista Projetu",
    }

    return render(
        request,
        "notif_div/proj_list.html",
        context
    )