from django.urls import path
from .views import item_list,check_out,ItemDetailView,HomeNameList,add_to_card

app_name='base'


urlpatterns = [
    path('check_out/',check_out,name ='check-out'),
    path('product_view/<slug>/',ItemDetailView.as_view(),name ='product-view'),
    path('add-to-cart/<slug>/',add_to_card,name ='add-to-cart'),
    path('',HomeNameList.as_view(),name ='item-list'),
    
    
]
