from django.shortcuts import render,get_object_or_404,redirect
from django import forms

from django.contrib import messages

from django.views.generic import ListView,DetailView,View,CreateView,UpdateView
from base.models import Item,Order,OrderItem,BillingAddress,Comment,ShippmentOrder


from .forms import CreateNewItemForm,ItemUpdateFrom

from django.contrib.auth.models import User



class All_product_list(ListView):
	#taking all products
    model = Item
    context_object_name = 'items'
    template_name='easylife_admin/all_items.html'






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
			return redirect("easylife_admin:itemdetailsview",pk=new_item.id) 
		else:
			return render(request,'easylife_admin/create_new_item.html',{'form':form})

	else:
		#new from is user wants to create a item
		form=CreateNewItemForm()
		return render(request,'easylife_admin/create_new_item.html',{'form':form})


def all_user_details(request):
	#showing all user in table
	all_user =User.objects.all()
	for i in all_user:
		i.pending_orders=Order.objects.filter(user=i,ordered=True).count()

	return render(request,'easylife_admin/all_user_list.html',{'all_user':all_user})



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




def itemupdateview(request,pk):
	obj = get_object_or_404(Item, id = pk)
	#using ItemUpdateFrom form for updating the item
	form = ItemUpdateFrom(request.POST or None,instance=obj)

	if form.is_valid(): #check form
		cd=form.cleaned_data
		form.save()
		#messages
		messages.info(request,f'The {obj.title} this Updated Successfully')
		return redirect("easylife_admin:itemdetailsview",pk=obj.id)  

	else:
		return render(request,'easylife_admin/item_update.html',{'form':form,'object':obj})	


def item_details(request,pk):
	
	item=get_object_or_404(Item,pk=pk)
	all_orders=Order.objects.filter(ordered=True)
	total_money=0

	for order in  all_orders:
		total_money+=order.get_total()




	if item.discount_price:
		earn_from_item=item.get_no_of_items()*item.discount_price
	else:
		earn_from_item=item.get_no_of_items()*item.price

	list_count_month=[34,56,12,65,23,45,35,78,34,34,23]


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
		'percentage': round(earn_from_item/total_money*100,2),
		'messages_item':messages_item,
		'user_purchased':item.get_no_of_users_buy(),
		'avrage_rating':round(sum(rate_list)/(len(rate_list) or 1),2),
		'avrage_rating_percentage':  round(((sum(rate_list)/ (len(rate_list) or 1))/5)*100,2),
		'list_count_month':list_count_month,
		'required_items':required_items

		})

def order_review(request,order_id,shipping_id,user_id):
	user=get_object_or_404(User,pk=user_id)
	order_by_user=get_object_or_404(Order,id=order_id,user=user)
	new_shipping_by_user=get_object_or_404(ShippmentOrder,id=shipping_id,order=order_by_user,user=user)

	return render(request,'easylife_admin/order_review.html',{'order':order_by_user,'shipping':new_shipping_by_user,'user':user})














