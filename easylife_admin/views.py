from django.shortcuts import render,get_object_or_404,redirect
from django import forms

from django.contrib import messages

from django.views.generic import ListView,DetailView,View,CreateView,UpdateView
from base.models import Item,Order,OrderItem,BillingAddress,Comment,ShippmentOrder


from .forms import CreateNewItemForm,ItemUpdateFrom,OrderVerificationForm,OrderReportSpamForm

from django.contrib.auth.models import User

from django.http import HttpResponse
#CELERY TASKS
from base.tasks import send_email


#SENDING EMAIL 
from django.conf import settings 
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#TIME
from django.utils import timezone

from base.models import Order,MAHARASHTRA_DISTRICTS

from datetime import datetime, timedelta

#LOGIN VIEWS


from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin





#EMAIL SETINGS
from_email = settings.EMAIL_HOST_USER


def not_allow_coustomer(view_func):
	def wrapper_func(request,*args, **kwargs):
		if request.user.is_authenticated:
		    if request.user.groups.filter(name='admin').exists():
		        return view_func(request,*args, **kwargs)
		    else:
		    	return HttpResponse('You are not admin ')

	return wrapper_func



@login_required
@not_allow_coustomer
def admin_dashboard(request):


	# TODO: OF LAST MONTH DUE TO DAY ISSUE
	#showing all user in table
	all_shipments = ShippmentOrder.objects.all()
	last_month = timezone.now() - timedelta(days=30)
	now_date=timezone.now()

	list_months=[i for i in range(1,13)]

	this_year_sale=[]
	last_year_sale=[]

	for month_number in list_months:
		this_year_sale.append(
						all_shipments.filter(
							payment_done_date__month=month_number,
							payment_done_date__year=now_date.year,

				).count())

		last_year_sale.append(
						all_shipments.filter(
							payment_done_date__month=month_number,
							payment_done_date__year=now_date.year-1,

				).count())
		
		




	number_of_order=all_shipments.count()
	orders_by_district = []

	for short_district_name in MAHARASHTRA_DISTRICTS:
		orders_by_district.append(all_shipments.filter(order__billing_address__city=short_district_name[0]).count())

	count_user =User.objects.count()-1


	#item ordered
	all_item=Item.objects.all()
	name_items=[]
	items_quantity=[]
	for item in all_item:

		if item.get_no_of_items() != 0 :
			name_items.append(item.title[:10]+f'({item.id})')
			items_quantity.append(item.get_no_of_items())

	total_sales=0
	verification_left=0
	payment_left=0
	delivery_left=0
	succesfully_orders=0

	last_month_sales=0
	for shipment_last_month in all_shipments.filter(payment_done_date__gte=last_month):
		if shipment_last_month.get_order_complete():
			last_month_sales+=shipment_last_month.order.get_total()



	for shipment in all_shipments:
		if shipment.get_order_complete():
			 total_sales+=shipment.order.get_total()
			 succesfully_orders+=1
		if not shipment.verify_order:
			verification_left+=1

		if not shipment.payment_done:
			payment_left+=1
		if not shipment.delivered:
			delivery_left+=1
		
	total_sales=total_sales or 1


	return render(request,'easylife_admin/main_admin_dashboard.html',{
			'all_shipments':all_shipments,
			'total_sales':total_sales,'count_user':count_user,
			'verification_left':verification_left,'succesfully_orders':succesfully_orders,
			'payment_left':payment_left,'delivery_left':delivery_left,

			'last_month_sales':last_month_sales,
			'last_month_sales_percentage':last_month_sales//total_sales*100,
			'number_of_order':number_of_order,
			'verification_pecentage':int((verification_left/(number_of_order or 1 ) )*100),
			'verified_order':number_of_order-verification_left,
			'payment_done':number_of_order-verification_left,
			'payment_pecentage':int((payment_left/(number_of_order or 1))*100),
			'delivery_compelted':number_of_order-delivery_left,
			'delivery_compelted_percentage':((number_of_order-delivery_left)/(number_of_order or 1))*100,
			'orders_left': number_of_order- succesfully_orders,
			'orders_left_percentage':((number_of_order- succesfully_orders)/(number_of_order or 1 ) )*100,
			'orders_by_district':orders_by_district,
			'this_year_sale':this_year_sale,'last_year_sale':last_year_sale, 
			'name_items':name_items, 'items_quantity':items_quantity


			})


@login_required
@not_allow_coustomer
def All_product_list(request):
	#taking all products
    items=Item.objects.all()
    return render(request,'easylife_admin/all_items.html',{'items':items})





@login_required
@not_allow_coustomer
def ItemCreateView(request):
	#form sumbitted by user
	if request.method == 'POST':
		#putting the values in form and checking if form is valid
		form=CreateNewItemForm(request.POST , request.FILES)

		if form.is_valid():
			#assining form data to the variable
			title=form.cleaned_data.get('title')
			price=form.cleaned_data.get('price')
			discount_price=form.cleaned_data.get('discount_price')
			category= 'A' if form.cleaned_data.get('category') else 'NA'
			label_name=form.cleaned_data.get('label_name')
			label=form.cleaned_data.get('label')
			description=form.cleaned_data.get('description')
			image=form.cleaned_data.get('image')
			image2=form.cleaned_data.get('image2')
			image3=form.cleaned_data.get('image3')
			image4=form.cleaned_data.get('image4')
			image5=form.cleaned_data.get('image5')
			image6=form.cleaned_data.get('image6')

			#creating a new product
			new_item=Item.objects.create(

       			title=title,
				price=price,
				discount_price=discount_price,
				category=category,
				label_name=label_name,
				label=label,
				description=description,
				image=image,
				image2=image2,
				image3=image3,
				image4=image4,
				image5=image5,
				image6=image6,

	        	)

			#saving the item and redirecting to deatil page
			new_item.save()
			
			subject= f"(Easylife) New Product is Released Buy It Now !!!"
			html_message = render_to_string('email_for_new_products.html', {'new_item':new_item})
			plain_message = strip_tags(html_message)
			to = [ user.email for user in User.objects.all()]
			
			send_email.delay(subject,html_message,plain_message,from_email,to)
			messages.success(request, f"To All Users is send For New Product Released !!!!")


			return redirect("easylife_admin:itemdetailsview",pk=new_item.id) 
		else:
			return render(request,'easylife_admin/create_new_item.html',{'form':form})

	else:
		#new from is user wants to create a item
		form=CreateNewItemForm()
		return render(request,'easylife_admin/create_new_item.html',{'form':form})

@login_required
@not_allow_coustomer
def all_user_details(request):
	#showing all user in table
	all_user =User.objects.all()
	for i in all_user:
		i.pending_orders=Order.objects.filter(user=i,ordered=True).count()

	return render(request,'easylife_admin/all_user_list.html',{'all_user':all_user})


@login_required
@not_allow_coustomer
def user_details(request,pk):
	#user deatils view

	#geting the user or 404 error
	user=get_object_or_404(User,pk=pk)

	#orders of that users
	shippment_order_user= ShippmentOrder.objects.filter(user=user)
	#how much money earn from user
	earn_money=0
	#how item purchased by user
	item_purchased=0

	#non verifiy orders associated to user
	no_verified=ShippmentOrder.objects.filter(user=user,verify_order=False).count()


	for shippment_order in shippment_order_user.filter(verify_order=True,payment_done=True):
		earn_money+=shippment_order.order.get_total()
		item_purchased+=shippment_order.order.items.count()

	return render(request,'easylife_admin/user_detail_view.html',{
		'shippment_order_user':shippment_order_user[::-1],
		'user':user,'earn_money':earn_money,'item_purchased':item_purchased,'no_verified':no_verified,'last_order':shippment_order_user.last()})



@login_required
@not_allow_coustomer
def itemupdateview(request,pk,order_id=None,shipping_id=None,user_id=None):
	obj = get_object_or_404(Item, id = pk)
	#using ItemUpdateFrom form for updating the item
	form = ItemUpdateFrom(request.POST or None,instance=obj)

	if form.is_valid(): #check form
		cd=form.cleaned_data
		form.save()
		#messages
		messages.info(request,f'The {obj.title} this Updated Successfully')
		if not user_id:
			return redirect("easylife_admin:itemdetailsview",pk=obj.id)  
		else:
			return redirect("easylife_admin:order-review",order_id=order_id,shipping_id=shipping_id,user_id=user_id)  


	else:
		return render(request,'easylife_admin/item_update.html',{'form':form,'object':obj})	

@login_required
@not_allow_coustomer
def item_details(request,pk):
	
	item=get_object_or_404(Item,pk=pk)
	all_orders=Order.objects.filter(ordered=True)
	total_money=0
	now_date=timezone.now()
	list_months=[i for i in range(1,13)]


	this_year_item_sale=[]
	last_year_item_sale=[]
	for month_number in list_months: 
		this_year_item_sale.append(
				item.get_no_of_items_of_that_month(month_number,now_date.year))

		last_year_item_sale.append(
				item.get_no_of_items_of_that_month(month_number,now_date.year-1)
				)


	for order in  all_orders:
		total_money+=order.get_total()




	if item.discount_price:
		earn_from_item=item.get_no_of_items()*item.discount_price
	else:
		earn_from_item=item.get_no_of_items()*item.price



	messages_item=Comment.objects.filter(product=item)[::-1]
	rate_list=[]
	for user_rating in messages_item:
		if user_rating.rating !=0:
			rate_list.append(user_rating.rating)

	required_items=0
	for sp in  ShippmentOrder.objects.filter(verify_order=True):
		for order_item in sp.order.items.all():
			if order_item.item == item:
				required_items+= order_item.qauntity



	return render(request,'easylife_admin/item_detail.html',
		{'item':item,'earn_from_item':earn_from_item,
		'percentage': round(earn_from_item/(total_money*100 or 1),2),
		'messages_item':messages_item,
		'user_purchased':item.get_no_of_users_buy(),
		'avrage_rating':round(sum(rate_list)/(len(rate_list) or 1),2),
		'avrage_rating_percentage':  round(((sum(rate_list)/ (len(rate_list) or 1))/5)*100,2),
		'required_items':required_items,
		'this_year_item_sale':this_year_item_sale, 
		'last_year_item_sale':last_year_item_sale

		})
@login_required
@not_allow_coustomer
def order_review(request,order_id,shipping_id,user_id):
	user=get_object_or_404(User,pk=user_id)
	order_by_user=get_object_or_404(Order,id=order_id,user=user)
	new_shipping_by_user=get_object_or_404(ShippmentOrder,id=shipping_id,order=order_by_user,user=user)
	item_available=True

	for order_item in new_shipping_by_user.order.items.all():
		if  order_item.item.category == 'NA':
			item_available=False


	form = OrderVerificationForm(request.POST or None,instance=new_shipping_by_user)
	form_report_spam=OrderReportSpamForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid() and not(request.POST.get('description')): #check form
			cd=form.cleaned_data


			if (cd['verify_order'] ) and  not (cd['delivered']  or  cd['payment_done']):
				new_shipping_by_user.verify_done_date=timezone.now()
				new_shipping_by_user.save()
				
				subject= f"(Easylife) Your Order is Been Verified Successfully !!"
				html_message = render_to_string('email_for_order_verification_complatete.html', {'order':order_by_user,'shipping':new_shipping_by_user,'request':request})
				plain_message = strip_tags(html_message)
				
				to = [user.email,'abhishekgawadeprogrammer@gmail.com']
				send_email.delay(subject,html_message,plain_message,from_email,to)
				messages.success(request, f"Order no {order_by_user.id} VERIFICATION IS DONE AND EMAIL IS SEND TO USER WAITING FOR STARTING DELIVERY")



			elif (cd['verify_order'] and cd['delivered'])  and  not ( cd['payment_done']):
				new_shipping_by_user.delivered_done_date=timezone.now()
				subject= f"(Easylife) Your Order delivery ha been started Your product will delivered Soon !!"
				html_message = render_to_string('email_for_order_dealivary_done.html', {'order':order_by_user,'shipping':new_shipping_by_user,'request':request})
				plain_message = strip_tags(html_message)

				to = [user.email,'abhishekgawadeprogrammer@gmail.com']
				send_email.delay(subject,html_message,plain_message,from_email,to)
				messages.success(request, f"Order no {order_by_user.id} DELIVERY STARTED  AND EMAIL IS SEND TO USER WAITING FOR STARTING PAYMENT DONE")



			elif (cd['verify_order'] and cd['delivered'])  and  cd['payment_done']:
				new_shipping_by_user.payment_done_date=timezone.now()				
				subject= f"(Easylife) Your Order Payment is Done So Enjoy Your Product Thanks"
				html_message = render_to_string('email_for_order_payment_done.html', {'order':order_by_user,'shipping':new_shipping_by_user,'request':request})
				plain_message = strip_tags(html_message)
				to = [user.email,'abhishekgawadeprogrammer@gmail.com']
				send_email.delay(subject,html_message,plain_message,from_email,to)
				messages.success(request, f"Order no {order_by_user.id} ORDER PAYMENTS IS DONE and email is successfully send to user")
			new_shipping_by_user.save()
			form.save()
			return redirect("easylife_admin:order-review",order_id=order_id, shipping_id=shipping_id,user_id=user_id)






		elif form_report_spam.is_valid():
			
			subject= f"(Easylife) Your Order{new_shipping_by_user.id} REPORTED SPAM AND DELETED!!"
			html_message = render_to_string('report_order_spam_email.html', {'description':request.POST.get('description')})
			plain_message = strip_tags(html_message)
			to = [user.email,'abhishekgawadeprogrammer@gmail.com']
			new_shipping_by_user.delete()
			new_shipping_by_user.save()
			order_by_user.delete()
			order_by_user.save()

			send_email.delay(subject,html_message,plain_message,from_email,to)
			messages.error(request, f"Order no {new_shipping_by_user.id} HAS BEEN REPORTED SPAM AND DELETED. EMAIL IS SEND TO USER")
			return redirect("easylife_admin:admin_dashboard")

	

	return render(request,'easylife_admin/order_review.html',{'order':order_by_user,'shipping':new_shipping_by_user,
																'user':user,'item_available':item_available,
																'order_verification_form':form,
																'form_report_spam':form_report_spam,
																})













