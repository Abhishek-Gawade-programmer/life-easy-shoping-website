from django import template
from  base.models import Order

register = template.Library()
@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs=Order.objects.filter(user=user,ordered=False)
        if qs.exists():
            return qs[0].items.count()
        return 0


# @register.filter
# def get_str_na_a(short_str):
# 	if short_str == ''


