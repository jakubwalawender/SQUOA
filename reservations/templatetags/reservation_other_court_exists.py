from django.templatetags.cache import register
from django.db.models import Q
from reservations.models import ActivitySubscription


@register.simple_tag(name="reservation_other_court_exists")
def reservation_other_court_exists(user, weekday, hour, type):
    if ActivitySubscription.objects.filter(~Q(type=type), user=user, weekday=weekday, hour__time=hour).exists():
        return True
    return False
