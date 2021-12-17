from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.index , name='home'),
    path('delete/<city_name>/' , views.del_city, name='del_city'),
    path('_' , views.del_everycity , name='del_everything')
]
