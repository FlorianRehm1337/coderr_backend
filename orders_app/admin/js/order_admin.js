(function ($) {
    'use strict';

    $(document).ready(function () {
        var $businessUserSelect = $('#id_business_user');
        var $offerSelect = $('#id_offer');

        function loadOffers(businessUserId) {
            if (!businessUserId) {
                $offerSelect.html('<option value="">---------</option>');
                return;
            }

            $.ajax({
                url: '/admin/get-offers-for-business/',
                data: {
                    'business_user_id': businessUserId
                },
                success: function (data) {
                    $offerSelect.html('<option value="">---------</option>');
                    $.each(data.offers, function (index, offer) {
                        $offerSelect.append(
                            $('<option></option>').val(offer.id).text(offer.title)
                        );
                    });
                },
                error: function () {
                    console.error('Fehler beim Laden der Offers');
                }
            });
        }

        $businessUserSelect.change(function () {
            var businessUserId = $(this).val();
            loadOffers(businessUserId);
        });

        var initialBusinessUserId = $businessUserSelect.val();
        if (initialBusinessUserId) {
            loadOffers(initialBusinessUserId);
        }
    });
})(django.jQuery);
