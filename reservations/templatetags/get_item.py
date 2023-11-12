from django.templatetags.cache import register


@register.filter(name="get_item")
def get_item(dictionary, key):
    return dictionary.get(key)
