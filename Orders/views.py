from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import  ListView,DetailView
from .models import Item,OrderItem,Order
from django.utils import  timezone
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

class HomeListView(ListView):
    model = Item
    paginate_by = 1
    template_name = 'Home_page.html'

class ItemDetailView(DetailView):
    template_name = 'Product.html'
    model = Item


def Add_to_Cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs.first()
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity+=1
            order_item.save()
            return JsonResponse({
                'response':'updated'
            })
        else:
            order.items.add(order_item)
            return JsonResponse({
                'response': 'success'
            })
    else:
       order_date=timezone.now()
       order= Order.objects.create(user=request.user,orderd_date=order_date)
       order.items.add(order_item)
    return JsonResponse({
        'response': 'success'
    })



def Remove_from_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_qs=Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            order.items.remove(order_item)
            return JsonResponse({
                'response':'remove'
            })
        else:
            return JsonResponse({
                'response': 'empty'
            })
    else:
        return  redirect('Orders:ItemDetailPage',slug=slug)
