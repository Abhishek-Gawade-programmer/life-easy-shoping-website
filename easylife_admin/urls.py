from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings 
from .views import (
                All_product_list,ItemCreateView,all_user_details,
                user_details,itemupdateview,
                item_details,order_review,admin_dashboard

                    )

app_name='easylife_admin'


urlpatterns = [
	path('order-review/<int:order_id>/<int:shipping_id>/<int:user_id>/', order_review, name='order-review'),
	path('item-details/<pk>/', item_details, name='itemdetailsview'),
	path('item-update/<int:order_id>/<int:shipping_id>/<int:user_id>/<pk>/', itemupdateview, name='itemupdateview-redirect'),
	path('item-update/<pk>/', itemupdateview, name='itemupdateview'),
	path('all-user-details/', all_user_details, name='all_user_details'),
	path('user-details/<pk>/', user_details, name='user_details'),
	 path('add-items/', ItemCreateView, name='add_items'),
	 path('all-items/', All_product_list, name='all_items'),

	path('', admin_dashboard, name='admin_dashboard'),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
