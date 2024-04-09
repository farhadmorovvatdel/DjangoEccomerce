from django.urls import path
from .views import HomeListView,ItemDetailView

app_name='Orders'
urlpatterns=[
    path('',HomeListView.as_view(),name='HomePage'),
    path('product/<slug>',ItemDetailView.as_view(),name='ItemDetailPage'),
]
