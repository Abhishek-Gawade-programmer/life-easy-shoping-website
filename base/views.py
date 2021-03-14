from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Item

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






def check_out(request):
    return render(request,'checkout-page.html')

def product_view(request):
    return render(request,'product-page.html')
