from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView,DetailView,View
from .models import Item,Order,OrderItem,BillingAddress
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
            # geting the order wich not checekouted yet
            order=Order.objects.get(user=self.request.user,ordered=False)
            return render(self.request,'order_summary.html',{'order':order})
        except ObjectDoesNotExist:
            # try to geting order summary even if order does not exist


            messages.error(self.request,f" { self.request.user.username } Don't have Any Item in The Cart")
            return redirect("/")







class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"

@login_required
def add_to_card(request,slug):

    #get the item (product if exists) from database

    item=get_object_or_404(Item,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(item=item,
    user=request.user,
    ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if  order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():

            #increase the quantity by 1 is product exists in order
            order_item.qauntity +=1
            order_item.save()
            messages.info(request,f'This {item.title} quntity  was updated')
            return redirect("base:order-summary")

        else:
            #add the product in order
            messages.info(request,f'This {item.title} already added to your cart')
            order.items.add(order_item)
            return redirect("base:order-summary")
    else:
        ordered_date=timezone.now()
        # create new order is not exists
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,f'This {item.title} sucessfully added to your cart')
        return redirect("base:order-summary")





class check_out(LoginRequiredMixin,View):

    
    def get(self,*args,**kwargs):
        # get check out form
        form=CheckoutForm()
        context={
            'form': form,
        }


        return render(self.request,'checkout-page.html',context)
        


    def post(self,*args,**kwargs):
        # valiad check out form 
        form=CheckoutForm(self.request.POST or None)


        try:
            order=Order.objects.get(user=self.request.user,ordered=False)

            if form.is_valid():

                user=form.cleaned_data.get('user')
                city=form.cleaned_data.get('city')
                phone_number=form.cleaned_data.get('phone_number')
                street_address=form.cleaned_data.get('street_address')
                apartment_address=form.cleaned_data.get('apartment_address')
                pin_code=form.cleaned_data.get('pin_code')

            
                #saving the from data to database via model
                billing_address=BillingAddress(
                    user=self.request.user,
                    city=city,
                    phone_number=phone_number,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    pin_code=pin_code
                    
                    )
                #saved to database
                billing_address.save()

                #aattact billing address to order
                order.billing_address = billing_address
                order.save()

                # TODO: add redirect to slected paymennt option


                messages.success(self.request,f' Sucessfully Checkout !!')
                return redirect("base:check-out")

            #error in validation of from
            messages.warning(self.request,f'⚠️  Failed to checlout')
            
            return redirect("base:check-out")



        except ObjectDoesNotExist:
            #if order does not exist
            messages.error(self.request,f" { self.request.user.username } Don't have Any Item in The Cart")
            return redirect("base:order-summary")




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


class PaymentView(View):
    def get(self,*args, **kwargs):
        return render(self.request,"payment.html")

    


