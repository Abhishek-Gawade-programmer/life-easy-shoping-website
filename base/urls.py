from django.urls import path
from .views import item_list,check_out,product_view,HomeNameList

app_name='base'


urlpatterns = [
    path('check_out/',check_out,name ='check-out'),
    path('product_view/',product_view,name ='product-view'),
    path('',HomeNameList.as_view(),name ='item-list'),
    
    
]
