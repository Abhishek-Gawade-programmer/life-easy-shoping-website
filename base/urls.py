from django.urls import path
from .views import (item_list,check_out,ItemDetailView,
                    HomeNameList,add_to_card,
                    remove_from_cart,OrderSummaryView,remove_single_item_cart
                    )

app_name='base'


urlpatterns = [
    path('check_out/',check_out.as_view(),name ='check-out'),
    path('product_view/<slug>/',ItemDetailView.as_view(),name ='product-view'),
    path('order-summary/',OrderSummaryView.as_view(),name ='order-summary'),

    path('add-to-cart/<slug>/',add_to_card,name ='add-to-cart'),
    path('remove-from-cart/<slug>/',remove_from_cart,name ='remove-from-cart'),
     path('remove-single-item-from-cart/<slug>/',remove_single_item_cart,name ='remove-single-item-from-cart'),
    path('',HomeNameList.as_view(),name ='item-list'),
    
    
]
