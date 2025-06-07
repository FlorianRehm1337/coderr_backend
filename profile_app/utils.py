from auth_app.models import BusinessProfile


def build_data(user, user_role):
    data = {
        "user": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user_role.first_name or '',
        "last_name": user_role.last_name or '',
        "type": user_role.type,
        "created_at": user_role.uploaded_at,
        "file": user_role.file.url if user_role.file else None,
    }

    if isinstance(user_role, BusinessProfile):
        data.update({
            "location": user_role.location or '',
            "tel": user_role.tel or '',
            "description": user_role.description or '',
            "working_hours": user_role.working_hours or '',
        })
    else:
        data.update({
            "location": '',
            "tel": '',
            "description": '',
            "working_hours": '',
        })

    return data
