# orders_app/utils.py oder helpers.py
def get_user_type(user):
    """
    Bestimmt den User-Typ basierend auf den Profilen
    """
    if hasattr(user, 'customer') and user.customer.type == 'customer':
        return 'customer'
    elif hasattr(user, 'business') and user.business.type == 'business':
        return 'business'
    return None

def get_user_profile(user):
    """
    Gibt das entsprechende Profil zurück
    """
    user_type = get_user_type(user)
    if user_type == 'customer':
        return user.customer
    elif user_type == 'business':
        return user.business
    return None

def is_customer(user):
    """
    Prüft ob User ein Customer ist
    """
    return get_user_type(user) == 'customer'

def is_business(user):
    """
    Prüft ob User ein Business ist
    """
    return get_user_type(user) == 'business'
