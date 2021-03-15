from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView
from .models import Item,Order,OrderItem
from  django.utils import timezone

class HomeNameList(ListView):
    model = Item
    context_object_name = 'items'
    template_name='home-page.html'




def item_list(request):
    context={
        'items':Item.objects.all()
    }
    return render(request,'home-page.html',context)


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"


def add_to_card(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(item=item,
    user=request.user,
    ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if  order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.qauntity +=1
            order_item.save()

        else:
            order.items.add(order_item)
    else:
        ordered_date=timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)

    return redirect("base:product-view",slug=slug)





def check_out(request):
    return render(request,'checkout-page.html')


def remove_from_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)

    if  order_qs.exists():
        order=order_qs[0]
        #check if order item in the otrder
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(
                        item=item,
                        user=request.user,
                        ordered=False)[0]
            order.items.remove(order_item) 

        else:
            #order does not conatin eorder itwm
            return redirect("base:product-view",slug=slug)       

    else:
        #add a message saying nio have prercf
        return redirect("base:product-view",slug=slug)
    return redirect("base:product-view",slug=slug)


