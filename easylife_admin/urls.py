from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings 
from .views import (
                SuccessView,All_product_list
                    )

app_name='easylife_admin'


urlpatterns = [

	 path('all_items/', All_product_list.as_view(), name='all_items'),
    path('success/', SuccessView.as_view(), name='success'),

]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
