from django.contrib.auth.decorators import login_required
from  django.contrib.auth .mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import  ListView,DetailView,View
from .models import Item,OrderItem,Order,BilldingAddress,OrderDiscount,DiscountCode
from django.utils import  timezone
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckOutForm


class HomeListView(ListView):
    model = Item
    paginate_by = 1
    template_name = 'Home_page.html'

class ItemDetailView(DetailView):
    template_name = 'orders/Product.html'
    model = Item
    def get_context_data(self,**kwargs):
        request=self.request
        context=super(ItemDetailView,self).get_context_data(**kwargs)
        context['is_authenticated']=request.user.is_authenticated
        return context


@login_required(redirect_field_name=None)
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

def Header(request):
    if request.user.is_authenticated:
      qs = Order.objects.filter(user=request.user,ordered=False)
      if qs.exists():
        item_count=qs.first().items.count()
        return render(request,'header.html',{'item_count':item_count})
      else:
          return render(request,'header.html',{'item_count':0})
    return  render(request,'header.html')

@login_required(redirect_field_name=None)
def Remove_from_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            order.items.remove(order_item)

            return JsonResponse({
                'response':'remove',


            })
        else:
            return JsonResponse({
                'response': 'empty'
            })
    return JsonResponse({
        'response':'empty'
    })

class Order_Summary(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
          order=Order.objects.get(user=self.request.user,ordered=False)
          return  render(self.request, 'orders/Order-summary.html', {'object':order})
        except ObjectDoesNotExist:

            return  redirect('Orders:HomePage')

@login_required(redirect_field_name=None)
def cart_item_count(request):
    qs = Order.objects.filter(user=request.user, ordered=False)
    if qs.exists():
        item_count= qs.first().items.count()
        return  JsonResponse({
            'item_count':item_count
        })
    return JsonResponse({
        'item_count':0
    })

def Faviorate_Item(request,id):
    item_id=str(id)
    faviorated_items=request.session.get('faviorated_items',[])
    if item_id in faviorated_items:
        faviorated_items.remove(item_id)
        faviorate=False
    else:
        faviorated_items.append(item_id)
        faviorate=True
    request.session['faviorated_items'] = faviorated_items
    request.session.modified = True

    return JsonResponse({'faviorate':faviorate})



@login_required(redirect_field_name=None)
def Remove_single_item_from_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            if order_item.quantity >1:
               order_item.quantity -=1
               order_item.save()
               save_amount = order_item.get_amount_save()
               final_price = order_item.get_final_price()
               order_total = order_qs.first().get_total()

               return JsonResponse({
                   'response': 'remove',
                   'quantity': order_item.quantity,
                   'save_amount': save_amount,
                   'final_price': final_price,
                   'order_total': order_total
               })
            else:
                order.items.remove(order_item)

                return  JsonResponse({
                    'response':'ItemRemoved'
                })




    #     else:
    #         return JsonResponse({
    #             'response': 'empty'
    #         })
    # return JsonResponse({
    #     'response':'empty'
    # })

@login_required(redirect_field_name=None)
def add_single_item_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order=Order.objects.filter(user=request.user,ordered=False)
    if order.exists():
       order_item=OrderItem.objects.filter(item=item,user=request.user,ordered=False).first()
       order_item.quantity+=1
       order_item.save()
       save_amount = order_item.get_amount_save()
       final_price = order_item.get_final_price()
       order_total = order.first().get_total()
       return JsonResponse(
           {
               'response':'success',
               'quantity':order_item.quantity,
               'save_amount': save_amount,
               'final_price': final_price,
               'order_total': order_total

            })


class CheckOutView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        order=Order.objects.filter(user=self.request.user ,ordered=False).first()
        if order.items.count()==0:
            return redirect('Orders:HomePage')
        form = CheckOutForm()
        return  render(self.request,'orders/CheckOut.html',{'form':form})

    def post(self,*args,**kwargs):
        form=CheckOutForm(self.request.POST or None)
        try:
            order=Order.objects.filter(user=self.request.user,ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartemant_address = form.cleaned_data.get('apartemant_address')
                country = form.cleaned_data.get('country')
                zip_cod = form.cleaned_data.get('zip_cod')
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get(' save_info')
                # payment_option = form.cleaned_data.get('payment_option')
                billding_address = BilldingAddress(user=self.request.user,
                           street_address=street_address, apartemant_address=apartemant_address,
                           country=country, zip_cod=zip_cod,)
                billding_address.save()
                order.billding_address=billding_address

                return JsonResponse({
                    'response':'ok'
                })


        except ObjectDoesNotExist:
            return redirect('Orders:HomePage')

        return render(self.request, 'orders/CheckOut.html', {'form': form})



class CouponView(View):

    def post(self,request,*args,**kwargs):
        cod_copon=self.request.POST.get('code-coupon')
        copon=DiscountCode.objects.filter(code__exact=cod_copon).first()
        order=Order.objects.filter(user=request.user,ordered=False).first()
        if copon and order:
            discount=OrderDiscount.objects.filter(order=order,discount_code=copon)
            if discount.exists():
                return  JsonResponse({'response':"already"})
            else:
                discount=OrderDiscount.objects.create(order=order,discount_code=copon).save()
                final_price=order.after_dicount()


                return  JsonResponse({'response':'Valid',
                                      'final_price':final_price})
        else:
            return  JsonResponse({
                'response':'NotValid'
            })









