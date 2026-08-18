from django.http import JsonResponse
import requests

def portal_auth_status(request):

    jti = request.session.get("jwt_jti")
    user_id = request.session.get("portal_user_id")
    session_version = request.session.get("jwt_session_version")

    if not jti or not user_id:
        return JsonResponse({"active": False})

    try:
        res = requests.get(
            "http://127.0.0.1:8000/api/check-session/",
            params={
                "jti": jti,
                "user_id": user_id,
                "session_version": session_version,
            },
            timeout=3,
        )

        if res.status_code != 200:
            return JsonResponse({"active": True})  # fail-safe

        data = res.json()

        #  ONLY MAIN SYSTEM DECIDES
        if data.get("active") is False:
            request.session.flush()
            return JsonResponse({"active": False})

        # optional sync
        if "session_version" in data:
            request.session["jwt_session_version"] = data["session_version"]

        return JsonResponse({"active": True})

    except Exception:
        return JsonResponse({"active": True})