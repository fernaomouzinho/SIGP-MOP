from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from company.models import Company,CompUser
from users.decorators import allowed_users
from sigp.utils import get_roles

# class APICompanyList(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         companies = Company.objects.all().order_by('name')
#         objects = []

#         for comp in companies:
#             objects.append({
#                 'id': comp.id,
#                 'name': comp.name,
#                 'reg_number': comp.reg_number,
#                 'start_date': comp.start_date,
#                 'email': comp.email,
#                 'phone': comp.phone,
#                 'website': comp.website,
#                 'address': comp.address,
#                 'type': comp.type,
#                 'country': comp.country.name if comp.country else None,
#                 'city': comp.city,
#                 'municipality': comp.municipality.name if comp.municipality else None,
#                 'lat': comp.lat,
#                 'lng': comp.lng,
#                 'is_active': comp.is_active,
#                 'user': comp.user.username if comp.user else None,
#                 'datetime': comp.datetime,
#                 'hashed': comp.hashed,
#             })

#         return Response({'objects': objects})


# @login_required
# class APICompanyList(APIView):
#     authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         user = request.user
#         is_admin = user.groups.filter(name="admin").exists()

#         if is_admin:
#             companies = Company.objects.all().select_related("country", "municipality", "user").order_by("name")
#         else:
#             try:
#                 comp_user = CompUser.objects.select_related("comp__country", "comp__municipality", "comp__user").get(user=user)
#                 companies = [comp_user.comp]
#             except CompUser.DoesNotExist:
#                 return Response(
#                     {"error": "User has no company assigned"},
#                     status=400
#                 )

#         objects = []
#         for comp in companies:
#             objects.append({
#                 "id": comp.id,
#                 "name": comp.name,
#                 "reg_number": comp.reg_number,
#                 "start_date": comp.start_date,
#                 "email": comp.email,
#                 "phone": comp.phone,
#                 "website": comp.website,
#                 "address": comp.address,
#                 "type": comp.type,
#                 "country": comp.country.name if comp.country else None,
#                 "city": comp.city,
#                 "municipality": comp.municipality.name if comp.municipality else None,
#                 "lat": comp.lat,
#                 "lng": comp.lng,
#                 "is_active": comp.is_active,
#                 "user": comp.user.username if comp.user else None,
#                 "datetime": comp.datetime,
#                 "hashed": comp.hashed,
#             })

#         return Response({"objects": objects})

from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response

from users.decorators import allowed_users
from sigp.utils import get_roles

from company.models import Company, CompUser


@method_decorator(allowed_users(allowed_roles=['sigp_admin','sigp_dna','sigp_dna_s','sigp_op','sigp_uivp',]),name='dispatch')
class APICompanyList(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        roles = get_roles(request)

        # -----------------------------------------
        # Check SIGP admin
        # -----------------------------------------
        is_admin = 'sigp_admin' in roles
        if is_admin:
            companies = ( Company.objects.select_related("country","municipality","user").all().order_by("name"))
        else:
            # SSO user ID from JWT
            user_id = request.user.id

            comp_user = (
                CompUser.objects
                .select_related(
                    "comp__country",
                    "comp__municipality",
                    "comp__user"
                )
                .filter(user_id=user_id)
                .first()
            )

            if not comp_user:
                return Response(
                    {
                        "error": "User has no company assigned"
                    },
                    status=400
                )

            companies = [comp_user.comp]

        # -----------------------------------------
        # Build response
        # -----------------------------------------
        objects = []

        for comp in companies:

            objects.append({
                "id": comp.id,
                "name": comp.name,
                "reg_number": comp.reg_number,
                "start_date": comp.start_date,
                "email": comp.email,
                "phone": comp.phone,
                "website": comp.website,
                "address": comp.address,
                "type": comp.type,

                "country": (
                    comp.country.name
                    if comp.country else None
                ),

                "city": comp.city,

                "municipality": (
                    comp.municipality.name
                    if comp.municipality else None
                ),

                "lat": comp.lat,
                "lng": comp.lng,
                "is_active": comp.is_active,

                "user": (
                    comp.user.username
                    if comp.user else None
                ),

                "datetime": comp.datetime,
                "hashed": comp.hashed,
            })

        return Response({
            "objects": objects
        })