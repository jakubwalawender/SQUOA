from django.templatetags.cache import register

from reservations.models import ActivitySubscription


@register.filter(name="int_to_weekday_short")
def int_to_weekday_short(value):
    try:
        return ActivitySubscription.Weekday(str(value)).label[:2]
    except Exception as e:
        return None
