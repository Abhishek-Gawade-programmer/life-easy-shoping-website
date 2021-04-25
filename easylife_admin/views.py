from django.shortcuts import render,get_object_or_404,redirect
from django import forms

from django.contrib import messages

from django.views.generic import ListView,DetailView,View,CreateView
from base.models import Item,Order,OrderItem,BillingAddress,Comment


from .forms import CreateNewItemForm

from django.contrib.auth.models import User
from base.models import Order,ShippmentOrder











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
			print('asfjkansf',category,form.cleaned_data.get('category'),form.cleaned_data.get('category')=='on')
			label_name=form.cleaned_data.get('label_name')
			label=form.cleaned_data.get('label')
			description=form.cleaned_data.get('description')

			if len(dict(request.FILES)['image']) > 6:
				##messagse 
				return redirect("easylife_admin:add_items")



			new_item=Item.objects.create(

       			title=title,
				price=price,
				discount_price=discount_price,SS
				category=category,
				label_name=label_name,
				label=label,
				description=description,
				image=dict(request.FILES)['image'][0],


	        	)

			new_item.save()

			# print('ddddddddddd', dict(request.FILES))
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

























# @login_required
# def NoteUpdateView(request,pk):
# 	obj = get_object_or_404(Note, id = pk)

# 	form = NoteForm(request.POST or None, instance = obj)

# 	if form.is_valid(): #send form
# 		cd=form.cleaned_data
# 		if cd.get('password_required') or  (obj.password_required):
# 			item_dict['update_the_note']=[form,pk]
# 			request.session['allow_if_password_is_confirm']=False
# 			return redirect('check_password')
# 		else:
# 			form.save()
# 			messages.success(request, f'''Note <a href="{reverse('note_update',args=[str(obj.pk)])}" class="alert-link">"{obj.heading}"</a> successfully Updated''')
# 			return redirect(Note.objects.filter(author=request.user).get(id=pk).get_absolute_url())

# 	else:#want form
# 		if (not obj.password_required) or request.session.get('allow_if_password_is_confirm'):
# 			return render(request,'noteshtmls/note_update.html',{'form':form,'object':obj})	
# 		elif (obj.password_required):
# 			request.session['allow_if_password_is_confirm']=False
# 			item_dict['allow_update_form']=obj.pk
# 			return redirect('check_password')









# def item_detail_admin(request,slug):
# 	item=Item.objects.get(slug=slug)
#     messages_item=Comment.objects.filter(product=item)[::-1]
#     context={
#         'object':item,
#         'messages_item':messages_item,
#         'range': range(1,6)


#     }
#     return render(request,'product-page.html',context)











