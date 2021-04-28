from django.shortcuts import render,get_object_or_404,redirect
from django import forms

from django.contrib import messages

from django.views.generic import ListView,DetailView,View,CreateView,UpdateView
from base.models import Item,Order,OrderItem,BillingAddress,Comment,ShippmentOrder


from .forms import CreateNewItemForm,GeeksForm

from django.contrib.auth.models import User



class All_product_list(ListView):
    model = Item
    context_object_name = 'items'
    template_name='easylife_admin/all_items.html'






def ItemCreateView(request):
	if request.method == 'POST':

		form=CreateNewItemForm(request.POST , request.FILES)
		if form.is_valid():
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

			new_item.save()
		else:
			return render(request,'easylife_admin/create_new_item.html',{'form':form})

	else:
		form=CreateNewItemForm()
		return render(request,'easylife_admin/create_new_item.html',{'form':form})


def all_user_details(request):
	all_user =User.objects.all()
	for i in all_user:
		i.pending_orders=Order.objects.filter(user=i,ordered=True).count()

	return render(request,'easylife_admin/all_user_list.html',{'all_user':all_user})



def user_details(request,pk):
	user=get_object_or_404(User,pk=pk)
	shippment_order_user= ShippmentOrder.objects.filter(user=user)
	earn_money=0
	item_purchased=0
	no_verified=ShippmentOrder.objects.filter(user=user,verify_order=False).count()


	for shippment_order in shippment_order_user.filter(verify_order=True,payment_done=True):
		earn_money+=shippment_order.order.get_total()
		item_purchased+=shippment_order.order.items.count()

	return render(request,'easylife_admin/user_detail_view.html',{
		'shippment_order_user':shippment_order_user,
		'user':user,'earn_money':earn_money,'item_purchased':item_purchased,'no_verified':no_verified,'last_order':shippment_order_user.last()})







def itemupdateview(request,pk):
	obj = get_object_or_404(Item, id = pk)

	form = GeeksForm(request.POST or None,instance=obj)

	if form.is_valid(): #send form
		cd=form.cleaned_data
		form.save()
		# messages.success(request, f'''Note <a href="{reverse('note_update',args=[str(obj.pk)])}" class="alert-link">"{obj.heading}"</a> successfully Updated''')
		# return redirect(Note.objects.filter(author=request.user).get(id=pk).get_absolute_url())

	else:
		return render(request,'easylife_admin/item_details_and_update.html',{'form':form,'object':obj})	















