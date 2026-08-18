from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from conf.decorators import allowed_users
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from project.models import Project
from finance.models import CPVReq, CPV, PO,EV
from eval.models import EvalLet, Eval
from proc.models import ProcLet, ProcReqTrack, ProcResTrack
from invoice.models import InvLet
from ver.models import Ver, VerSecEng
from insp.models import Insp, InspSecEng
from conf.user_utils import c_user_sup, c_user_eng, c_user_sec,c_user_pos

# class notifbadgeDGAF(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot,tot1,tot2,tot3,tot4 = 0,0,0,0,0
#         tot1 = CPVReq.objects.filter(is_send=True, is_appr=False).all().count()
#         tot2 = CPV.objects.filter(is_dgaf=True, is_send=True, is_appr=False).all().count()
#         tot3 = PO.objects.filter(is_send=True, is_appr=False).all().count()
#         tot4 = ProcReqTrack.objects.filter(is_dna_out=True, is_dgaf_in_1=False).all().count()
#         tot5 = ProcResTrack.objects.filter(is_dna_out=True, is_dgaf_in_1=False).all().count()
#         tot6 = ProcLet.objects.filter((Q(is_back=True)|Q(to_id=2, is_send=True, is_read=False))).all().count()
#         tot7 = InvLet.objects.filter(to_id=3, is_send=True, is_read=False).all().count()
#         tot = tot1+tot2+tot3+tot4+tot5+tot6+tot7
#         return Response({'value':tot})

class notifbadgeDGAF(APIView):

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
        # 3. Allow DGAF roles only
        # ==========================================
        if not any(
            role in group
            for role in ["sigp_dgaf", "sigp_dgaf_s"]
        ):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        # ==========================================
        # 4. Count notifications
        # ==========================================
        tot1 = CPVReq.objects.filter(
            is_send=True,
            is_appr=False
        ).count()

        tot2 = CPV.objects.filter(
            is_dgaf=True,
            is_send=True,
            is_appr=False
        ).count()

        tot3 = PO.objects.filter(
            is_send=True,
            is_appr=False
        ).count()

        tot4 = ProcReqTrack.objects.filter(
            is_dna_out=True,
            is_dgaf_in_1=False
        ).count()

        tot5 = ProcResTrack.objects.filter(
            is_dna_out=True,
            is_dgaf_in_1=False
        ).count()

        tot6 = ProcLet.objects.filter(
            Q(is_back=True) |
            Q(
                to_id=2,
                is_send=True,
                is_read=False
            )
        ).count()

        tot7 = InvLet.objects.filter(
            to_id=3,
            is_send=True,
            is_read=False
        ).count()

        total = (
            tot1 +
            tot2 +
            tot3 +
            tot4 +
            tot5 +
            tot6 +
            tot7
        )

        return Response({
            "value": total
        })

# class notifbadgeDNOF(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = 0
#         tot1 = CPVReq.objects.filter((Q(is_back=True)|Q(is_appr=True, is_end=False))).all().count()
#         tot2 = CPV.objects.filter((Q(is_back=True)|Q(cpvtrack__is_dgaf_out=True, is_end=False))).all().count()
#         tot3 = InvLet.objects.filter(to_id=2, is_send=True, is_read=False).all().count()
#         tot4 = ProcLet.objects.filter(to_id=4, is_send=True, is_read=False).all().count()
#         tot = tot1+tot2+tot3+tot4
#         return Response({'value':tot})

class notifbadgeDNOF(APIView):

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
        # 3. Allow DNOF roles only
        # ==========================================
        if not any(
            role in group
            for role in ["sigp_dnof", "sigp_dnof_s"]
        ):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        # ==========================================
        # 4. Count DNOF notifications
        # ==========================================
        tot1 = CPVReq.objects.filter(
            Q(is_back=True) |
            Q(
                is_appr=True,
                is_end=False
            )
        ).count()

        tot2 = CPV.objects.filter(
            Q(is_back=True) |
            Q(
                cpvtrack__is_dgaf_out=True,
                is_end=False
            )
        ).count()

        tot3 = InvLet.objects.filter(
            to_id=2,
            is_send=True,
            is_read=False
        ).count()

        tot4 = ProcLet.objects.filter(
            to_id=4,
            is_send=True,
            is_read=False
        ).count()

        total = tot1 + tot2 + tot3 + tot4

        return Response({
            "value": total
        })

# class notifbadgeDNOFBO(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = 0
#         tot1 = EV.objects.filter(is_send=True, is_read=False).all().count()
#         tot = tot1
#         return Response({'value':tot})

class notifbadgeDNOFBO(APIView):

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
        # 3. Allow DNOF Back Office only
        # ==========================================
        if "sigp_dnof_bo" not in group:
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        # ==========================================
        # 4. Count notifications
        # ==========================================
        total = EV.objects.filter(
            is_send=True,
            is_read=False
        ).count()

        return Response({
            "value": total
        })

# class notifbadgeGab(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot,tot1,tot2,tot3,tot4 = 0,0,0,0,0
#         tot1 = CPV.objects.filter(is_dgaf=False, is_send=True, is_appr=False).all().count()
#         tot2 = EvalLet.objects.filter(to_id=1, is_send=True, is_read=False).all().count()
#         tot3 = ProcLet.objects.filter(to_id=1, is_send=True, is_read=False).all().count()
#         tot4 = InvLet.objects.filter((Q(is_send=True, is_read=False)|Q(is_back=True)), to_id=5).all().count()
#         tot = tot1+tot2+tot3+tot4
#         return Response({'value':tot})

class notifbadgeGab(APIView):

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
        # 3. Allow GAB role only
        # ==========================================
        if "sigp_gab" not in group:
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        # ==========================================
        # 4. Count GAB notifications
        # ==========================================
        tot1 = CPV.objects.filter(
            is_dgaf=False,
            is_send=True,
            is_appr=False
        ).count()

        tot2 = EvalLet.objects.filter(
            to_id=1,
            is_send=True,
            is_read=False
        ).count()

        tot3 = ProcLet.objects.filter(
            to_id=1,
            is_send=True,
            is_read=False
        ).count()

        tot4 = InvLet.objects.filter(
            Q(is_send=True, is_read=False) |
            Q(is_back=True),
            to_id=5
        ).count()

        total = tot1 + tot2 + tot3 + tot4

        return Response({
            "value": total
        })

# class notifbadgeDNA(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = 0
#         tot1 = CPV.objects.filter(is_end=True, is_get_dna=False).all().count()
#         tot2 = PO.objects.filter((Q(is_back=True)|Q(potrack__is_dgaf_out=True, is_end=False))).all().count()
#         tot3 = Eval.objects.filter(is_appr=True, is_end=False).all().count()
#         tot4 = ProcLet.objects.filter(to_id=3, is_send=True, is_read=False).all().count()
#         tot5 = InvLet.objects.filter((Q(to_id=1, is_send=True, is_read=False)|Q(to_id=2, is_back=True))).all().count()
#         tot = tot1+tot2+tot3+tot4+tot5
#         return Response({'value':tot})

class notifbadgeDNA(APIView):

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
        # 3. Allow DNA roles only
        # ==========================================
        if not any(
            role in group
            for role in ["sigp_dna", "sigp_dna_s"]
        ):
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        # ==========================================
        # 4. Count DNA notifications
        # ==========================================
        tot1 = CPV.objects.filter(
            is_end=True,
            is_get_dna=False
        ).count()

        tot2 = PO.objects.filter(
            Q(is_back=True) |
            Q(
                potrack__is_dgaf_out=True,
                is_end=False
            )
        ).count()

        tot3 = Eval.objects.filter(
            is_appr=True,
            is_end=False
        ).count()

        tot4 = ProcLet.objects.filter(
            to_id=3,
            is_send=True,
            is_read=False
        ).count()

        tot5 = InvLet.objects.filter(
            Q(
                to_id=1,
                is_send=True,
                is_read=False
            ) |
            Q(
                to_id=2,
                is_back=True
            )
        ).count()

        # ==========================================
        # 5. Total
        # ==========================================
        total = (
            tot1 +
            tot2 +
            tot3 +
            tot4 +
            tot5
        )

        return Response({
            "value": total
        })

# class notifbadgeUVIP(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = 0
#         tot1 = Eval.objects.filter((\
#             Q(is_send=True, is_read=False)|\
#             Q(is_appr=True, is_let_appr=False, is_end=False)|\
#             Q(is_appr=True, is_let_appr=True, is_end=False))).all().count()
#         tot2 = EvalLet.objects.filter(is_back=True).all().count()
#         tot3 = InvLet.objects.filter((Q(to_id=4, is_send=True, is_read=False)|Q(to_id=5, is_back=True))).all().count()
#         tot4 = Ver.objects.filter(is_back=False).all().count()
#         tot5 = VerSecEng.objects.filter(is_back=True, is_back_read=False).all().count()
#         tot6 = InspSecEng.objects.filter(is_back=True, is_back_read=False).all().count()
#         tot = tot1+tot2+tot3+tot4+tot5+tot6
#         return Response({'value':tot})

class notifbadgeUVIP(APIView):

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
        # 4. Count UVIP notifications
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

        tot3 = InvLet.objects.filter(
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

        tot4 = Ver.objects.filter(
            is_back=False
        ).count()

        tot5 = VerSecEng.objects.filter(
            is_back=True,
            is_back_read=False
        ).count()

        tot6 = InspSecEng.objects.filter(
            is_back=True,
            is_back_read=False
        ).count()

        # ==========================================
        # 5. Total
        # ==========================================
        total = (
            tot1 +
            tot2 +
            tot3 +
            tot4 +
            tot5 +
            tot6
        )

        return Response({
            "value": total
        })

#
# class notifbadgeDIV(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         tot = Project.objects.filter(is_active=True, is_read=False).all().count()
#         return Response({'value':tot})

class notifbadgeDIV(APIView):

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
        # 3. Allow DIV roles only
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
        # 4. Count DIV notifications
        # ==========================================
        total = Project.objects.filter(
            is_active=True,
            is_read=False
        ).count()

        return Response({
            "value": total
        })
#
# class notifbadgeSUP(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         mun = c_user_sup(request.user)
#         tot = InvLet.objects.filter(mun=mun, is_back=True).all().count()
#         return Response({'value':tot})

class notifbadgeSUP(APIView):

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
        # 3. Allow Supervisor role only
        # ==========================================
        if "sigp_sup" not in group:
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        # ==========================================
        # 4. Get municipality from SSO user
        # ==========================================
        mun = getattr(portal_user, "municipality", None)

        if not mun:
            return Response({
                "value": 0
            })

        # ==========================================
        # 5. Count supervisor notifications
        # ==========================================
        total = InvLet.objects.filter(
            mun=mun,
            is_back=True
        ).count()

        return Response({
            "value": total
        })
#
# class notifbadgeSEC(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         sec = c_user_sec(request.user)
#         epos = c_user_pos(request.user)
#         print(epos)
#         print(sec)  
#         tot1 = Ver.objects.filter(sec=sec, epos__cat=epos, is_send=True, is_read=False).all().count()
#         tot2 = VerSecEng.objects.filter(sec=sec, ver__epos__cat=epos, is_eng_back=True, is_eng_read=False).all().count()
#         tot3 = Insp.objects.filter(epos__cat=epos,sec=sec, is_send=True, is_read=False).all().count()
#         tot4 = InspSecEng.objects.filter(sec=sec, insp__epos__cat=epos, is_eng_back=True, is_eng_read=False).all().count()
#         tot = tot1+tot2+tot3+tot4
#         return Response({'value':tot})

class notifbadgeSEC(APIView):

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
        # 3. Allow SEC role only
        # ==========================================
        if "sigp_sec" not in group:
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        # ==========================================
        # 4. Get section and position from SSO
        # ==========================================
        sec_id = getattr(portal_user, "sec_id", None)
        epos = getattr(portal_user, "epos_cat", None)

        if not sec_id or not epos:
            return Response({
                "value": 0
            })

        # ==========================================
        # 5. Count SEC notifications
        # ==========================================
        tot1 = Ver.objects.filter(
            sec_id=sec_id,
            epos__cat=epos,
            is_send=True,
            is_read=False
        ).count()

        tot2 = VerSecEng.objects.filter(
            sec_id=sec_id,
            ver__epos__cat=epos,
            is_eng_back=True,
            is_eng_read=False
        ).count()

        tot3 = Insp.objects.filter(
            sec_id=sec_id,
            epos__cat=epos,
            is_send=True,
            is_read=False
        ).count()

        tot4 = InspSecEng.objects.filter(
            sec_id=sec_id,
            insp__epos__cat=epos,
            is_eng_back=True,
            is_eng_read=False
        ).count()

        total = tot1 + tot2 + tot3 + tot4

        return Response({
            "value": total
        })
    
# class notifbadgeENG(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         eng = c_user_eng(request.user)
#         epos = c_user_pos(request.user)
#         print(epos)
#         print(eng)
#         tot1 = VerSecEng.objects.filter(to=eng, epos__cat=epos, is_send=True, is_send_read=False).all().count()
#         tot2 = InspSecEng.objects.filter(to=eng, insp__epos__cat=epos, is_send=True, is_send_read=False).all().count()
#         tot =tot1+tot2
#         return Response({'value':tot})

class notifbadgeENG(APIView):

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
        # 3. Allow Engineer role only
        # ==========================================
        if "sigp_eng" not in group:
            return Response(
                {"detail": "Permission denied."},
                status=403
            )

        # ==========================================
        # 4. Get engineer + position from SSO
        # ==========================================
        eng_id = getattr(portal_user, "eng_id", None)
        epos = getattr(portal_user, "epos_cat", None)

        if not eng_id or not epos:
            return Response({
                "value": 0
            })

        # ==========================================
        # 5. Count Engineer notifications
        # ==========================================
        tot1 = VerSecEng.objects.filter(
            to_id=eng_id,
            epos__cat=epos,
            is_send=True,
            is_send_read=False
        ).count()

        tot2 = InspSecEng.objects.filter(
            to_id=eng_id,
            insp__epos__cat=epos,
            is_send=True,
            is_send_read=False
        ).count()

        total = tot1 + tot2

        return Response({
            "value": total
        })
