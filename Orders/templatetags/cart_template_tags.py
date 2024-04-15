from django import  template
from Orders.models import  Order
register=template.Library()

@register.filter
def Cart_Item_Count(user):
    if user.is_authenticated:
        qs=Order.objects.filter(user=user,ordered=False)
        if qs.exists():
            return qs.first().items.count()
    return  0