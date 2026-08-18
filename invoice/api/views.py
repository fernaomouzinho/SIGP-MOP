from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from invoice.models import Invoice, InvTrack


def format_date(date_obj):
    """Convert date to DD-MM-YYYY format, return None if empty."""
    if date_obj:
        return date_obj.strftime("%d-%m-%Y")
    return None


# class APIInvoiceList(APIView):
#     authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         user = request.user
#         is_admin = user.groups.filter(name='admin').exists()

#         if is_admin:
#             invoices = Invoice.objects.all().order_by('-date')
#         else:
#             invoices = Invoice.objects.filter(user=user).order_by('-date')

#         objects = []
#         for inv in invoices:
#             objects.append({
#                 "invoice_number": inv.number,
#                 "contract": inv.cont.number if inv.cont else None,
#                 "municipality": inv.mun.name if inv.mun else None,
#                 "date": format_date(inv.date),
#                 "phys_prog": inv.phys_prog,
#                 "total": float(inv.total) if inv.total is not None else None,
#                 "desc": inv.desc,
#                 "is_paid": inv.is_paid,
#                 "is_end": inv.is_end,
#             })

#         return Response({"objects": objects})

class APIInvoiceList(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        # ==========================================
        # 1. Get SSO identity
        # ==========================================
        portal_user = getattr(request, "portal_user", None)

        if not portal_user:
            return Response(
                {"detail": "Authentication required."},
                status=401
            )

        # ==========================================
        # 2. Get roles from SSO
        # ==========================================
        roles = getattr(request, "portal_roles", [])

        if not roles:
            roles = request.session.get("portal_roles", [])

        # Adjust these roles to your real system
        admin_roles = [
            "pmis_admin",
            "pmis_finance",
            "admin",
        ]

        is_admin = any(role in roles for role in admin_roles)

        # ==========================================
        # 3. Get external employee/user identity
        # ==========================================
        emp_id = getattr(portal_user, "emp_id", None)

        if not emp_id:
            return Response(
                {"detail": "Employee identity not found."},
                status=403
            )

        # ==========================================
        # 4. Filter invoices
        # ==========================================
        if is_admin:
            invoices = Invoice.objects.all()
        else:
            invoices = Invoice.objects.filter(
                employee_id=emp_id
            )

        invoices = invoices.order_by("-date")

        # ==========================================
        # 5. Build response
        # ==========================================
        objects = []

        for inv in invoices:
            objects.append({
                "invoice_number": inv.number,
                "contract": inv.cont.number if inv.cont else None,
                "municipality": inv.mun.name if inv.mun else None,
                "date": format_date(inv.date),
                "phys_prog": inv.phys_prog,
                "total": (
                    float(inv.total)
                    if inv.total is not None
                    else None
                ),
                "desc": inv.desc,
                "is_paid": inv.is_paid,
                "is_end": inv.is_end,
            })

        return Response({
            "objects": objects
        })
    
# class APIInvoiceTracking(APIView):
#     """
#     API to list invoices with their tracking status and stage percentage.
#     Dates will be returned in DD-MM-YYYY format.
#     """
#     authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         user = request.user
#         is_admin = user.groups.filter(name='admin').exists()

#         if is_admin:
#             invoices = Invoice.objects.all().order_by('-date')
#         else:
#             invoices = Invoice.objects.filter(user=user).order_by('-date')

#         objects = []

#         for inv in invoices:
#             invtrack = InvTrack.objects.filter(inv=inv).first()  # One track per invoice
#             track_data = {}

#             if invtrack:
#                 track_data = {
#                     "stages": invtrack.stages,
#                     "percent": invtrack.percent,
#                     "is_sup_out": invtrack.is_sup_out,
#                     "date_sup_out": format_date(invtrack.date_sup_out),
#                     "is_uvip_in": invtrack.is_uvip_in,
#                     "date_uvip_in": format_date(invtrack.date_uvip_in),
#                     "is_insp_start": invtrack.is_insp_start,
#                     "date_insp_start": format_date(invtrack.date_insp_start),
#                     "is_insp_end": invtrack.is_insp_end,
#                     "date_insp_end": format_date(invtrack.date_insp_end),
#                     "is_uvip_out_1": invtrack.is_uvip_out_1,
#                     "date_uvip_out_1": format_date(invtrack.date_uvip_out_1),
#                     "is_adn_in": invtrack.is_adn_in,
#                     "date_adn_in": format_date(invtrack.date_adn_in),
#                     "is_uvip_out_2": invtrack.is_uvip_out_2,
#                     "date_uvip_out_2": format_date(invtrack.date_uvip_out_2),
#                     "is_gab_in": invtrack.is_gab_in,
#                     "date_gab_in": format_date(invtrack.date_gab_in),
#                     "is_gap_app": invtrack.is_gap_app,
#                     "date_gab_app": format_date(invtrack.date_gab_app),
#                     "is_gab_out": invtrack.is_gab_out,
#                     "date_gab_out": format_date(invtrack.date_gab_out),
#                     "is_dgaf_in": invtrack.is_dgaf_in,
#                     "date_dgaf_in": format_date(invtrack.date_dgaf_in),
#                     "is_dgaf_out": invtrack.is_dgaf_out,
#                     "date_dgaf_out": format_date(invtrack.date_dgaf_out),
#                     "is_dna_in": invtrack.is_dna_in,
#                     "date_dna_in": format_date(invtrack.date_dna_in),
#                     "is_dna_out": invtrack.is_dna_out,
#                     "date_dna_out": format_date(invtrack.date_dna_out),
#                     "is_dnof_in": invtrack.is_dnof_in,
#                     "date_dnof_in": format_date(invtrack.date_dnof_in),
#                     "is_dnof_out": invtrack.is_dnof_out,
#                     "date_dnof_out": format_date(invtrack.date_dnof_out),
#                     "is_dnof_middle_out": invtrack.is_dnof_middle_out,
#                     "date_dnof_middle_out": format_date(invtrack.date_dnof_middle_out),
#                     "is_dnof_back_in": invtrack.is_dnof_back_in,
#                     "date_dnof_back_in": format_date(invtrack.date_dnof_back_in),
#                     "is_dnof_back_insp_start": invtrack.is_dnof_back_insp_start,
#                     "date_dnof_back_insp_start": format_date(invtrack.date_dnof_back_insp_start),
#                     "is_dnof_back_insp_end": invtrack.is_dnof_back_insp_end,
#                     "date_dnof_back_insp_end": format_date(invtrack.date_dnof_back_insp_end),
#                     "is_dnof_back_cre_start": invtrack.is_dnof_back_cre_start,
#                     "date_dnof_back_cre_start": format_date(invtrack.date_dnof_back_cre_start),
#                     "is_dnof_back_cre_end": invtrack.is_dnof_back_cre_end,
#                     "date_dnof_back_cre_end": format_date(invtrack.date_dnof_back_cre_end),
#                     "is_dnof_back_apr_start": invtrack.is_dnof_back_apr_start,
#                     "date_dnof_back_apr_start": format_date(invtrack.date_dnof_back_apr_start),
#                     "is_dnof_back_apr_end": invtrack.is_dnof_back_apr_end,
#                     "date_dnof_back_apr_end": format_date(invtrack.date_dnof_back_apr_end),
#                     "is_dnof_back_out": invtrack.is_dnof_back_out,
#                     "date_dnof_back_out": format_date(invtrack.date_dnof_back_out),
#                 }

#             objects.append({
#                 "invoice_number": inv.number,
#                 "contract": inv.cont.number if inv.cont else None,
#                 "municipality": inv.mun.name if inv.mun else None,
#                 "date": format_date(inv.date),
#                 "phys_prog": inv.phys_prog,
#                 "total": inv.total,
#                 "desc": inv.desc,
#                 "is_paid": inv.is_paid,
#                 "is_end": inv.is_end,
#                 "tracking": track_data
#             })

#         return Response({"objects": objects})


class APIInvoiceTracking(APIView):
    """
    API to list invoices with their tracking status and stage percentage.

    Authentication and authorization are based on SSO/JWT.
    Dates are returned in DD-MM-YYYY format.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        # ==========================================
        # 1. Get authenticated SSO user
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
        roles = getattr(request, "portal_roles", [])

        if not roles:
            roles = request.session.get("portal_roles", [])

        # Change according to your actual roles
        admin_roles = [
            "pmis_admin",
            "pmis_finance",
            "admin",
        ]

        is_admin = any(
            role in roles
            for role in admin_roles
        )

        # ==========================================
        # 3. Get employee identity from SSO
        # ==========================================
        emp_id = getattr(portal_user, "emp_id", None)

        if not emp_id:
            return Response(
                {"detail": "Employee identity not found."},
                status=403
            )

        # ==========================================
        # 4. Filter invoices
        # ==========================================
        if is_admin:
            invoices = Invoice.objects.all()
        else:
            invoices = Invoice.objects.filter(
                employee_id=emp_id
            )

        invoices = invoices.order_by("-date")

        objects = []

        # ==========================================
        # 5. Build invoice tracking response
        # ==========================================
        for inv in invoices:

            invtrack = InvTrack.objects.filter(
                inv=inv
            ).first()

            track_data = {}

            if invtrack:
                track_data = {

                    "stages": invtrack.stages,
                    "percent": invtrack.percent,

                    # Supervisor
                    "is_sup_out": invtrack.is_sup_out,
                    "date_sup_out": format_date(
                        invtrack.date_sup_out
                    ),

                    # UVIP
                    "is_uvip_in": invtrack.is_uvip_in,
                    "date_uvip_in": format_date(
                        invtrack.date_uvip_in
                    ),

                    # Inspection
                    "is_insp_start": invtrack.is_insp_start,
                    "date_insp_start": format_date(
                        invtrack.date_insp_start
                    ),

                    "is_insp_end": invtrack.is_insp_end,
                    "date_insp_end": format_date(
                        invtrack.date_insp_end
                    ),

                    # UVIP OUT 1
                    "is_uvip_out_1": invtrack.is_uvip_out_1,
                    "date_uvip_out_1": format_date(
                        invtrack.date_uvip_out_1
                    ),

                    # ADN
                    "is_adn_in": invtrack.is_adn_in,
                    "date_adn_in": format_date(
                        invtrack.date_adn_in
                    ),

                    # UVIP OUT 2
                    "is_uvip_out_2": invtrack.is_uvip_out_2,
                    "date_uvip_out_2": format_date(
                        invtrack.date_uvip_out_2
                    ),

                    # GAB
                    "is_gab_in": invtrack.is_gab_in,
                    "date_gab_in": format_date(
                        invtrack.date_gab_in
                    ),

                    "is_gap_app": invtrack.is_gap_app,
                    "date_gab_app": format_date(
                        invtrack.date_gab_app
                    ),

                    "is_gab_out": invtrack.is_gab_out,
                    "date_gab_out": format_date(
                        invtrack.date_gab_out
                    ),

                    # DGAF
                    "is_dgaf_in": invtrack.is_dgaf_in,
                    "date_dgaf_in": format_date(
                        invtrack.date_dgaf_in
                    ),

                    "is_dgaf_out": invtrack.is_dgaf_out,
                    "date_dgaf_out": format_date(
                        invtrack.date_dgaf_out
                    ),

                    # DNA
                    "is_dna_in": invtrack.is_dna_in,
                    "date_dna_in": format_date(
                        invtrack.date_dna_in
                    ),

                    "is_dna_out": invtrack.is_dna_out,
                    "date_dna_out": format_date(
                        invtrack.date_dna_out
                    ),

                    # DNOF
                    "is_dnof_in": invtrack.is_dnof_in,
                    "date_dnof_in": format_date(
                        invtrack.date_dnof_in
                    ),

                    "is_dnof_out": invtrack.is_dnof_out,
                    "date_dnof_out": format_date(
                        invtrack.date_dnof_out
                    ),

                    "is_dnof_middle_out": (
                        invtrack.is_dnof_middle_out
                    ),
                    "date_dnof_middle_out": format_date(
                        invtrack.date_dnof_middle_out
                    ),

                    # DNOF back
                    "is_dnof_back_in": (
                        invtrack.is_dnof_back_in
                    ),
                    "date_dnof_back_in": format_date(
                        invtrack.date_dnof_back_in
                    ),

                    # Back inspection
                    "is_dnof_back_insp_start": (
                        invtrack.is_dnof_back_insp_start
                    ),
                    "date_dnof_back_insp_start": format_date(
                        invtrack.date_dnof_back_insp_start
                    ),

                    "is_dnof_back_insp_end": (
                        invtrack.is_dnof_back_insp_end
                    ),
                    "date_dnof_back_insp_end": format_date(
                        invtrack.date_dnof_back_insp_end
                    ),

                    # CRE
                    "is_dnof_back_cre_start": (
                        invtrack.is_dnof_back_cre_start
                    ),
                    "date_dnof_back_cre_start": format_date(
                        invtrack.date_dnof_back_cre_start
                    ),

                    "is_dnof_back_cre_end": (
                        invtrack.is_dnof_back_cre_end
                    ),
                    "date_dnof_back_cre_end": format_date(
                        invtrack.date_dnof_back_cre_end
                    ),

                    # Approval
                    "is_dnof_back_apr_start": (
                        invtrack.is_dnof_back_apr_start
                    ),
                    "date_dnof_back_apr_start": format_date(
                        invtrack.date_dnof_back_apr_start
                    ),

                    "is_dnof_back_apr_end": (
                        invtrack.is_dnof_back_apr_end
                    ),
                    "date_dnof_back_apr_end": format_date(
                        invtrack.date_dnof_back_apr_end
                    ),

                    # Final out
                    "is_dnof_back_out": (
                        invtrack.is_dnof_back_out
                    ),
                    "date_dnof_back_out": format_date(
                        invtrack.date_dnof_back_out
                    ),
                }

            objects.append({
                "invoice_number": inv.number,

                "contract": (
                    inv.cont.number
                    if inv.cont
                    else None
                ),

                "municipality": (
                    inv.mun.name
                    if inv.mun
                    else None
                ),

                "date": format_date(inv.date),

                "phys_prog": inv.phys_prog,

                "total": (
                    float(inv.total)
                    if inv.total is not None
                    else None
                ),

                "desc": inv.desc,
                "is_paid": inv.is_paid,
                "is_end": inv.is_end,

                "tracking": track_data,
            })

        return Response({
            "objects": objects
        })