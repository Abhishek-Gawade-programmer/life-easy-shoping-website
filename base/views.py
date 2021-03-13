from django.shortcuts import render
from .models import Item

def item_list(request):
    return render(request,'item_list.html',context)


