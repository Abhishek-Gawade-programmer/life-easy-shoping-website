from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView,DetailView,View
from .models import Item,Order,OrderItem,BillingAddress,Comment,ShippmentOrder
from  django.utils import timezone
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

import json
import stripe




#HTML TO PDF
import os
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders



#SENDING EMAIL 
from django.conf import settings 
from django.template.loader import render_to_string
from django.utils.html import strip_tags


#CELERY TASKS
from .tasks import send_email


from django.utils import timezone






stripe.api_key = settings.STRIPE_SECRET_KEY

from .forms import CheckoutForm







def HomeNameList(request):
    items=Item.objects.all()
    if request.user.is_authenticated:
        if request.user.groups.filter(name='admin').exists():
            return redirect("easylife_admin:admin_dashboard")

        return render(request,'home.html',{'items':items})

    return render(request,'home.html',{'items':items})


class OrderSummaryView(LoginRequiredMixin,View):
    # model = Order
    def get(self,*args,**kwargs):
        try:
            # geting the order wich not checekouted yet
            order=Order.objects.get(user=self.request.user,ordered=False)
            
            
            return render(self.request,'order_summary.html',{'order':order})
        except ObjectDoesNotExist:
            # try to geting order summary even if order does not exist


            messages.error(self.request,f" { self.request.user.get_full_name() } Don't have Any Item in The Cart")
            return redirect("base:item-list")






def item_detail_view(request,slug):
    item=get_object_or_404(Item,slug=slug)
    messages_item=Comment.objects.filter(product=item)[::-1]

    #add some different logic
    images_list=[]
    if item.image:
        images_list.append(item.image.url)

        if item.image2:
            images_list.append(item.image2.url)

            if item.image3:
                images_list.append(item.image3.url)

                if item.image4:
                    images_list.append(item.image4.url)

                    if item.image5:
                        images_list.append(item.image5.url)
                        if item.image6:
                            images_list.append(item.image6.url)



    context={
        'object':item,
        'messages_item':messages_item,
        'images_list':images_list,


        'range': range(1,6)


    }
    return render(request,'product-page.html',context)



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
            messages.info(request,f'This {item.title} added to your cart')
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

        try:
            order=Order.objects.get(user=self.request.user,ordered=False)



            context={
                'form': form,
                'order':order,
                 "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
            }
            return render(self.request,'checkout-page.html',context)

        except:
            messages.info(self.request,f'You don"t have Active Order')
            return redirect("base:item-list")   


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
                payment_option=form.cleaned_data.get('payment_option')

            
                #saving the from data to database via model
                billing_address=BillingAddress(
                    user=self.request.user,
                    city=city,
                    phone_number=phone_number,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    pin_code=pin_code,
                    payment_option=payment_option
                    
                    )
                #saved to database
                billing_address.save()
                
                #aattact billing address to order
                order.billing_address = billing_address


                order.ordered_date=timezone.now()

                order.ordered=True

                order.save()
                if billing_address.payment_option=='S':
                     return render(self.request,'payment.html',{'order':order,"STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY}) 
                    



                # TODO: add redirect to slected paymennt option



                messages.success(self.request,f' Sucessfully Checkout !!')
                return redirect("base:success",pk=order.id)

            #error in validation of from
            messages.warning(self.request,f'⚠️  Failed to checkout')

            
            return redirect("base:check-out")



        except ObjectDoesNotExist:
            #if order does not exist
            messages.error(self.request,f" { self.request.user.get_full_name() } Don't have Any Item in The Cart")
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





class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        order=Order.objects.get(pk=self.kwargs['pk'])

        all_product_info=[]
        for order_item in order.items.all():
            product_info={
                'price_data': {
                                'currency': 'inr',
                                'unit_amount':int(order_item.item.discount_price)*100 if order_item.item.discount_price else int(order_item.item.price)*100 ,
                                'product_data': {
                                    'name':order_item.item.title,
                                    'images': ['https://post.healthline.com/wp-content/uploads/2020/08/young-woman-wheelchair-disabled-732x549-thumbnail.jpg'],
                                },
                            },
                            'quantity': order_item.qauntity,
                        }
            all_product_info.append(product_info)


        YOUR_DOMAIN='http://127.0.0.1:8000'
        x=f'Order No #{order.id}'
        price=int(order.get_total())*100
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            

            line_items=all_product_info,
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/'+f'{order.pk}/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        return JsonResponse({'id': checkout_session.id})



@login_required
def SuccessView(request,pk):

    order_by_user=get_object_or_404(Order,pk=pk,user=request.user,ordered=True)

    new_shipping_by_user=ShippmentOrder.objects.create(
            user=request.user,
            order=order_by_user,
    )
    if order_by_user.billing_address.payment_option=='S':
        new_shipping_by_user.payment_done=True
        new_shipping_by_user.payment_done_date=now_date=timezone.now()



    new_shipping_by_user.save()

    return render(request,'success.html',{'order':order_by_user,'shipping':new_shipping_by_user})




@login_required
def invoice_generate(request,order_id,shipping_id):
    order_by_user=get_object_or_404(Order,id=order_id,user=request.user)
    new_shipping_by_user=get_object_or_404(ShippmentOrder,id=shipping_id,order=order_by_user,user=request.user)
    
    subject= f"(Easylife) Successfully Order is Record Please See You invoice"
    html_message = render_to_string('invoice_email_template.html', {'order':order_by_user,'shipping':new_shipping_by_user,'request':request})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = [request.user.email,'abhishekgawadeprogrammer@gmail.com']
    send_email.delay(subject,html_message,plain_message,from_email,to)
    messages.success(request, f"Your invoice is also Sended to you email")



    return render(request,'invoice.html',{'order':order_by_user,'shipping':new_shipping_by_user})



class CancelView(LoginRequiredMixin,TemplateView):
    template_name = "cancel.html"

@login_required
@csrf_exempt
def stripe_webhook(request):
    payload = request.body


    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # RO DO :seND EMAIL

    return HttpResponse(status=200)


@login_required
def rate_comment_on_product(request):
    if request.method=='POST' :
        item=get_object_or_404(Item,slug=request.POST.get('slug'))


        update_comment = Comment.objects.filter(user=request.user,product=item)
        if  update_comment.exists():
            #update a comment is eixits


            user_comment=update_comment[0]
            user_comment.body=request.POST.get('message')
            user_comment.rating=int(request.POST.get('num_rate'))
            user_comment.save()
        else:
            #create a new comment
            user_comment=Comment.objects.create(user=request.user,product=item,
                            rating=int(request.POST.get('num_rate')),
                            body=request.POST.get('message'))
            user_comment.save()

        # print('asjkfhausfbubyu',x)
        return JsonResponse({'success':'true','score':request.POST.get('num_rate')},safe=False)
    return JsonResponse({'success':'false'})



@login_required
def render_pdf_view(request,order_id,shipping_id):

    order_by_user=get_object_or_404(Order,id=order_id,user=request.user)
    new_shipping_by_user=get_object_or_404(ShippmentOrder,id=shipping_id,order=order_by_user,user=request.user)
    from django.utils import timezone
    now_date=timezone.now()

    template_path = 'invoice_pdf.html'
    context = {'order':order_by_user,'shipping':new_shipping_by_user,'request':request,'now_date':now_date}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{request.user.get_full_name()}_invioce_number_{order_id}.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




@login_required
def all_invoice_view(request):

    all_invoice=ShippmentOrder.objects.filter(user=request.user)

    return render(request,'all_invoice_view.html',{'all_invoice':all_invoice})



















    


