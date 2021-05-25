from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings 
from .views import (check_out,item_detail_view,
                    HomeNameList,add_to_card,
                    remove_from_cart,OrderSummaryView,remove_single_item_cart,CreateCheckoutSessionView,
                    SuccessView,CancelView,stripe_webhook,
                    rate_comment_on_product,invoice_generate,
                    render_pdf_view,all_invoice_view
                    )

app_name='base'


urlpatterns = [

    path('rate_comment_on_product/',rate_comment_on_product,name ='rate_comment_on_product'),

    path('check_out/',check_out.as_view(),name ='check-out'),
    path('product_view/<slug>/',item_detail_view,name ='product-view'),
    path('order-summary/',OrderSummaryView.as_view(),name ='order-summary'),

    path('add-to-cart/<slug>/',add_to_card,name ='add-to-cart'),
    path('remove-from-cart/<slug>/',remove_from_cart,name ='remove-from-cart'),

    path('remove-single-item-from-cart/<slug>/',remove_single_item_cart,name ='remove-single-item-from-cart'),

    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),

    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/<pk>/', SuccessView, name='success'),
    path('invoice-generate/<int:order_id>/<int:shipping_id>/', invoice_generate, name='invoice-generate'),
    path('all-invoice-view/', all_invoice_view, name='all_invoice_view'),

    

    path('invoice-pdf-view/<int:order_id>/<int:shipping_id>/', render_pdf_view   , name='invoice-pdf-view'),



    
    # path('payment/<payment_option>/',PaymentView.as_view(),name ='payment'),
    path('',HomeNameList,name ='item-list'),
    

    
    


]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
