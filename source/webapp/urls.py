from django.contrib import admin
from django.urls import path
from webapp.views import ProductList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete, AddItemToCart, \
    CartList, CartDelete, OrderCreate, CartDeleteOne

app_name = 'webapp'

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('product/<int:pk>/view/', ProductDetail.as_view(), name='product_view'),
    path('product/<int:pk>/add_to_cart/', AddItemToCart.as_view(), name='add_to_cart'),
    path('product/<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('product/add/', ProductCreate.as_view(), name='product_add'),
    path('cart/', CartList.as_view(), name='cart_index'),
    path('order/', OrderCreate.as_view(), name='order_create'),
    path('cart/<int:pk>/delete/', CartDelete.as_view(), name='cart_delete'),
    path('cart/<int:pk>/delete_one/', CartDeleteOne.as_view(), name='cart_delete_one'),
]