from django.urls import path
from .views import item_list,check_out

app_name='base'


urlpatterns = [
    path('check_out/',check_out,name ='check-out'),
    path('',item_list,name ='item-list'),
    
    
]
