from django.templatetags.cache import register

from reservations.models import ActivitySubscription


@register.filter(name="int_to_weekday")
def int_to_weekday(value):
    try:
        return ActivitySubscription.Weekday(str(value)).label
    except Exception as e:
        return None

