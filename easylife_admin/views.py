from django.shortcuts import render
from django.views.generic import TemplateView

from django.views.generic import ListView,DetailView,View
from base.models import Item,Order,OrderItem,BillingAddress,Comment








class All_product_list(ListView):
    model = Item
    context_object_name = 'items'
    template_name='easylife_admin/all_items.html'







# def item_detail_admin(request,slug):
# 	item=Item.objects.get(slug=slug)
#     messages_item=Comment.objects.filter(product=item)[::-1]
#     context={
#         'object':item,
#         'messages_item':messages_item,
#         'range': range(1,6)


#     }
#     return render(request,'product-page.html',context)








class SuccessView(TemplateView):
    template_name = "easylife_admin/container.html"




