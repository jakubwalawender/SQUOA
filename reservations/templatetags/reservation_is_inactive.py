from django.templatetags.cache import register
from reservations.calendar.calendar import ReservationHourType


@register.filter(name="reservation_is_inactive")
def reservation_is_inactive(value):
    return value == ReservationHourType.INACTIVE
