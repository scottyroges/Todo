from app.auth.get_request import get_request


def is_owner_or_admin(object_owner_id):
    return is_owner(object_owner_id) or is_admin()


def is_owner(object_owner_id):
    return object_owner_id == get_request().user_id


def is_admin():
    request = get_request()
    if request.groups:
        for group in request.groups:
            if group == "Admin":
                return True
    return False