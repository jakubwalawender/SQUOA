from django.templatetags.cache import register


@register.filter(name="reservation_is_mine")
def reservation_is_mine(value, user):
    if value.user == user:
        return True
    return False
