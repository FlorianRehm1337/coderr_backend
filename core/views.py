# views.py oder admin_views.py
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods

from auth_app.models import BusinessProfile
from offers_app.models import Offer

@staff_member_required
@require_http_methods(["GET"])
def get_offers_for_business(request):
    """
    AJAX View um Offers für einen bestimmten Business User zu laden
    """
    business_user_id = request.GET.get('business_user_id')

    if not business_user_id:
        return JsonResponse({'offers': []})

    try:
        business_user = BusinessProfile.objects.get(id=business_user_id)
        offers = Offer.objects.filter(business_user=business_user)

        offers_data = [
            {
                'id': offer.id,
                'title': str(offer)
            }
            for offer in offers
        ]

        return JsonResponse({'offers': offers_data})

    except BusinessProfile.DoesNotExist:
        return JsonResponse({'offers': []})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
