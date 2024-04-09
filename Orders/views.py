from django.shortcuts import render
from django.views.generic import  ListView,DetailView
from .models import Item,OrderItem,Order

class HomeListView(ListView):
    model = Item
    template_name = 'Home_page.html'

class ItemDetailView(DetailView):
    template_name = 'Product.html'
    model = Item