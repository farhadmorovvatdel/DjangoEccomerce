from django.urls import path
from .views import HomeListView,ItemDetailView,Add_to_Cart,Remove_from_cart,Order_Summary,cart_item_count

app_name='Orders'
urlpatterns=[
    path('',HomeListView.as_view(),name='HomePage'),
    path('order-summary/',Order_Summary.as_view(),name='HomePage'),
    path('product/<slug>',ItemDetailView.as_view(),name='ItemDetailPage'),
    path('add-to-cart/<slug>',Add_to_Cart,name='add-to-cart'),
    path('remove-from-cart/<slug>',Remove_from_cart,name='remove-from-cart'),
    path('cart-item-count/',cart_item_count,name='cart-item-count'),


]
