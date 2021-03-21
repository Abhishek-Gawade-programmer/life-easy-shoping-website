from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView,DetailView,View
from .models import Item,Order,OrderItem
from  django.utils import timezone

from .forms import CheckoutForm

class HomeNameList(ListView):
    model = Item
    context_object_name = 'items'
    paginate_by=10
    template_name='home.html'


class OrderSummaryView(LoginRequiredMixin,View):
    # model = Order
    def get(self,*args,**kwargs):
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            return render(self.request,'order_summary.html',{'order':order})
        except ObjectDoesNotExist:
            messages.error(self.request,f" { self.request.user.username } Don't have Any Item in The Cart")
            return redirect("/")
        
    # template_name=





def item_list(request):
    context={
        'items':Item.objects.all()
    }
    return render(request,'home.html',context)



class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"

@login_required
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
            messages.info(request,f'This {item.title} quntity  was updated')
            return redirect("base:order-summary")

        else:
            messages.info(request,f'This {item.title} already added to your cart')
            order.items.add(order_item)
            return redirect("base:order-summary")
    else:
        ordered_date=timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,f'This {item.title} sucessfully added to your cart')
        return redirect("base:order-summary")



def check_out(View):
    def get(self,*args,**kwargs):
        #form
        form=CheckoutForm()
        context={
            'form': form,
        }


        return render(request,'checkout-page.html',context)

    def post(self,args,**kwargs):
        form=CheckoutForm(self.request.POST or None)
        if form.is_valid():
            print('for is valid')
            return redirect("base:check_out")

@login_required
def remove_single_item_cart(request,slug):
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

            if order_item.qauntity >1:
                order_item.qauntity -=1
            else:
                order.items.remove(order_item) 

            order_item.save()
            messages.info(request,f'This {item.title} is Decreasce by one ')
            return redirect("base:order-summary")

        else:
            #order does not conatin eorder itwm
            messages.info(request,f'This {item.title} not in your cart')
            return redirect("base:product-view")       

    else:
        #add a message saying nio have prercf
        messages.info(request,f'You don"t have Active Order')
        return redirect("base:product-view")



@login_required
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
            messages.info(request,f'This {item.title} removed from your cart')
            return redirect("base:product-view",slug=slug)

        else:
            #order does not conatin eorder itwm
            messages.info(request,f'This {item.title} not in your cart')
            return redirect("base:product-view",slug=slug)       

    else:
        #add a message saying nio have prercf
        messages.info(request,f'You don"t have Active Order')
        return redirect("base:product-view",slug=slug)
    


