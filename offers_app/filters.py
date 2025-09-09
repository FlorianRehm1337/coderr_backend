class OfferFilterHelper:
    @staticmethod
    def filter_details_by_request(details_qs, request):
        """
        Zentrale Filterlogik für Details - kann in ViewSet und Serializer verwendet werden
        """
        if not request:
            return details_qs

        min_price = request.query_params.get('min_price')
        max_delivery_time = request.query_params.get('max_delivery_time')

        if min_price:
            try:
                details_qs = details_qs.filter(price__gte=float(min_price))
            except ValueError:
                pass

        if max_delivery_time:
            try:
                details_qs = details_qs.filter(delivery_time_in_days__lte=int(max_delivery_time))
            except ValueError:
                pass

        return details_qs
