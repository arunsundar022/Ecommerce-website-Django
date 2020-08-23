from django.urls import path
from . import views


urlpatterns=[
    path('',views.store,name='Store'),
    path('cart/',views.cart,name='Cart'),
    path('checkout/',views.checkout,name='Checkout'),
    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),


]
