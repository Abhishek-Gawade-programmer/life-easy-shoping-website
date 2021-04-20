from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib import messages

from django.views.generic import ListView,DetailView,View,CreateView
from base.models import Item,Order,OrderItem,BillingAddress,Comment


from .forms import CreateNewItemForm








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
			image=form.cleaned_data.get('image')

			new_item=Item.objects.create(

       			title=title,
				price=price,
				discount_price=discount_price,
				category=category,
				label_name=label_name,
				label=label,
				description=description,
				image=image,


	        	)

			new_item.save()


			print("losdhisudnfuisnduifi")
			print(request.POST)
		else:
			print("losdhisudnfuisnduifi",form.errors)
			return render(request,'easylife_admin/create_new_item.html',{'form':form})

	else:
		form=CreateNewItemForm()
		return render(request,'easylife_admin/create_new_item.html',{'form':form})


def all_user_details(request):
	return render(request,'easylife_admin/all_user_list.html')




























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











