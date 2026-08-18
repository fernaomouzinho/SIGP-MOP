def get_roles(request):
    user = getattr(request, "auth_user", None)

    if user:
        return user.get("roles", [])

    return request.session.get("jwt_roles", [])