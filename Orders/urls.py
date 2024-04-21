from django.urls import path
from .views import HomeListView,ItemDetailView,\
    Add_to_Cart,Remove_from_cart,Order_Summary\
    ,cart_item_count,Faviorate_Item,Remove_single_item_from_cart,\
    add_single_item_cart,CheckOutView
app_name='Orders'
urlpatterns=[
    path('',HomeListView.as_view(),name='HomePage'),
    path('order-summary/',Order_Summary.as_view(),name='OrderSummary'),
    path('product/<slug>',ItemDetailView.as_view(),name='ItemDetailPage'),
    path('add-to-cart/<slug>',Add_to_Cart,name='add-to-cart'),
    path('remove-from-cart/<slug>',Remove_from_cart,name='remove-from-cart'),
    path('faviorate-item/<id>',Faviorate_Item,name='faviorate-item'),
    path('cart-item-count/',cart_item_count,name='cart_item_count'),
    path('remove-single-item-from-cart/<slug>',Remove_single_item_from_cart,name='remove-single-item'),
    path('add-single-item-to-cart/<slug>',add_single_item_cart,name='add-single-item'),
    path('checkout/',CheckOutView.as_view(),name='check-out'),


]
