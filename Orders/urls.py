from django.urls import path
from .views import HomeListView,ItemDetailView,Add_to_Cart

app_name='Orders'
urlpatterns=[
    path('',HomeListView.as_view(),name='HomePage'),
    path('product/<slug>',ItemDetailView.as_view(),name='ItemDetailPage'),
    path('add-to-cart/<slug>',Add_to_Cart,name='add-to-cart'),
]
