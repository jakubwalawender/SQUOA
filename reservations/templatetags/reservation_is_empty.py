from django.templatetags.cache import register
from reservations.calendar.calendar import ReservationHourType


@register.filter(name="reservation_is_empty")
def reservation_is_empty(value):
    return value == ReservationHourType.EMPTY
