from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings 
from .views import (check_out,ItemDetailView,
                    HomeNameList,add_to_card,
                    remove_from_cart,OrderSummaryView,remove_single_item_cart,
                    PaymentView
                    )

app_name='base'


urlpatterns = [
    path('check_out/',check_out.as_view(),name ='check-out'),
    path('product_view/<slug>/',ItemDetailView.as_view(),name ='product-view'),
    path('order-summary/',OrderSummaryView.as_view(),name ='order-summary'),

    path('add-to-cart/<slug>/',add_to_card,name ='add-to-cart'),
    path('remove-from-cart/<slug>/',remove_from_cart,name ='remove-from-cart'),

    path('remove-single-item-from-cart/<slug>/',remove_single_item_cart,name ='remove-single-item-from-cart'),

    path('payment/<payment_option>/',PaymentView.as_view(),name ='payment'),
    path('',HomeNameList.as_view(),name ='item-list'),
    
    


]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
