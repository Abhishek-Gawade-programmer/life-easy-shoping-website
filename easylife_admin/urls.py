from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings 
from .views import (
                All_product_list,ItemCreateView,all_user_details,
                user_details,itemupdateview
                    )

app_name='easylife_admin'


urlpatterns = [
	path('item-update-view/<pk>/', itemupdateview, name='itemupdateview'),
	path('all-user-details/', all_user_details, name='all_user_details'),
	path('user-details/<pk>/', user_details, name='user_details'),
	 path('add-items/', ItemCreateView, name='add_items'),
	 path('all-items/', All_product_list.as_view(), name='all_items'),

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
