from django.urls import path, include

from ecommerce import views

urlpatterns = [

    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('update_item/', views.updateItem, name='update_item'),

    path('login_user/', views.login_view, name='login' , ),

]
