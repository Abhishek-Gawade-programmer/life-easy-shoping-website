from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings 
from .views import (
                All_product_list,ItemCreateView,all_user_details
                    )

app_name='easylife_admin'


urlpatterns = [
	path('all_user_details/', all_user_details, name='all_user_details'),
	 path('add_items/', ItemCreateView, name='add_items'),
	 path('all_items/', All_product_list.as_view(), name='all_items'),

]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
