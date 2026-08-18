# portal/middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from types import SimpleNamespace
from django.shortcuts import redirect
from urllib.parse import urlencode
import requests
import logging
import time

logger = logging.getLogger(__name__)


class SIGPSSOMiddleware(MiddlewareMixin):
    """
    Enterprise SSO Middleware

    FEATURES
    --------
    1. First portal access with token:
       http://127.0.0.1:8001/?token=JWT

    2. Creates secure local portal session

    3. Every request auto-authenticates from session

    4. Sync logout from Main System

    5. Prevents infinite loops

    6. Redirects to React login if no auth
    """

    EXCLUDED_PREFIXES = (
        "/static/",
        "/media/",
        "/favicon.ico",
        "/mopportaladmin23/",
        "/api/portal-auth-status/",
    )

    LOGIN_URL = "http://localhost:5173/login"
    MAIN_CHECK_URL = "http://127.0.0.1:8000/api/check-session/"

    # =====================================================
    # MAIN ENTRY
    # =====================================================
    def process_request(self, request):

        path = request.path

        # -----------------------------------------
        # skip static/login/api status
        # -----------------------------------------
        if path.startswith(self.EXCLUDED_PREFIXES):
            return

        # =================================================
        # MODE 1: EXISTING PORTAL SESSION
        # =================================================
        if request.session.get("sso_authenticated"):

            if self.is_session_invalid(request):
                request.session.flush()
                return redirect(self.LOGIN_URL)

            return self.attach_user_from_session(request)

        # =================================================
        # MODE 2: FIRST LOGIN WITH TOKEN
        # =================================================
        token = request.GET.get("token") or self.extract_bearer(request)

        if token:
            if self.login_from_token(request, token):
                return self.attach_user_from_session(request)

        # =================================================
        # MODE 3: NO SESSION / NO TOKEN
        # =================================================
        request.user = AnonymousUser()

        # API request = return nothing, let view handle
        if path.startswith("/api/"):
            return

        # page request = redirect login
        return redirect(self.LOGIN_URL)

    # =====================================================
    # ATTACH USER
    # =====================================================
    def attach_user_from_session(self, request):

        user_id = request.session.get("portal_user_id")
        print(user_id)
        username = request.session.get("portal_user")
        print(username)
        roles = request.session.get("portal_roles", [])
        print(roles)

        if not user_id or not username:
            request.session.flush()
            request.user = AnonymousUser()
            return

        request.user = SimpleNamespace(
            is_authenticated=True,
            id=user_id,
            username=username,
            is_staff=True,
            is_superuser=False,
        )

        request.auth_user = {
            "id": user_id,
            "username": username,
            "roles": roles,
        }

        request.portal_user = username
        request.portal_roles = roles

    # =====================================================
    # LOGIN FROM TOKEN
    # =====================================================
    def login_from_token(self, request, token):

        try:
            payload = JWTAuthentication().get_validated_token(token).payload

            if payload.get("iss") != "main-system":
                return False

            user_id = payload.get("user_id")
            username = payload.get("username")
            roles = payload.get("roles", [])
            
            print("user_id",user_id,"username:",username,"roles",roles)

            request.session["sso_authenticated"] = True
            request.session["portal_user_id"] = user_id
            request.session["portal_user"] = username
            request.session["portal_roles"] = roles
            request.session["jwt_jti"] = payload.get("jti")
            request.session["jwt_session_version"] = payload.get("session_version")
            request.session["last_sso_check"] = 0

            request.session.set_expiry(getattr(settings, "PORTAL_SESSION_AGE", 28800))
            request.session.save()

            logger.info("Portal login success: %s", username)
            return True

        except Exception as e:
            logger.warning("JWT LOGIN FAILED: %s", str(e))
            return False

    # =====================================================
    # CENTRAL SESSION VALIDATION
    # =====================================================
    def is_session_invalid(self, request):

        now = int(time.time())

        interval = getattr(settings, "SSO_CHECK_INTERVAL", 30)
        last = request.session.get("last_sso_check", 0)

        # reduce API spam
        if now - last < interval:
            return False

        request.session["last_sso_check"] = now

        try:
            res = requests.get(
                self.MAIN_CHECK_URL,
                params={
                    "jti": request.session.get("jwt_jti"),
                    "user_id": request.session.get("portal_user_id"),
                    "session_version": request.session.get(
                        "jwt_session_version"
                    ),
                },
                timeout=2,
            )

            if res.status_code == 200:
                data = res.json()

                if data.get("active") is False:
                    logger.info("Main system logout detected")
                    return True

                return False

            return False

        except Exception as e:
            logger.warning("SSO CHECK FAILED: %s", str(e))
            return False

    # =====================================================
    # EXTRACT BEARER TOKEN
    # =====================================================
    def extract_bearer(self, request):

        auth = request.META.get("HTTP_AUTHORIZATION")

        if not auth:
            return None

        if auth.startswith("Bearer "):
            return auth.split(" ")[1]

        return None