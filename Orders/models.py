from django.db import models
from django.conf import settings
from django.shortcuts import reverse

CATEGORY_CHOICES=(
    ( 'S','Shirt'),
    ( 'SW','Sport Wear'),
    ( 'OW','Outwear')
)
LABEL_CHOICES=(
    ( 'Su','Succeess'),
    ( 'S','secondary'),
    ( 'D','danger')
)
class Item(models.Model):
    title=models.CharField(max_length=100)
    price=models.FloatField()
    discount_price=models.FloatField(null= True,blank=True)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=20,default='S')
    label=models.CharField(choices=LABEL_CHOICES,max_length=20,default="Su")
    slug=models.SlugField()
    description=models.TextField(null=True,blank=True)
    quantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.title
    def get_asbolute_url(self):
        return  reverse('Orders:ItemDetailPage',kwargs={
            'slug':self.slug
        })
    def get_add_to_cart_url(self):
        return  reverse("Orders:add-to-cart",kwargs={
            'slug':self.slug
        })
    def remove_from_cart_url(self):
        return reverse('Orders:remove-from-cart',kwargs={
            'slug':self.slug
        })

class OrderItem(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.title
    def get_total_item_price(self):
        return self.quantity * self.item.price


    def get_total_discount_item_price(self):
        return  self.quantity * self.item.discount_price

    def get_amount_save(self):
        return (self.get_total_item_price() - self.get_total_discount_item_price())

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    orderd_date=models.DateTimeField()
    ordered = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

    def get_total(self):
        total=0
        for order_item in self.items.all():
            total+=order_item.get_final_price()
        return  total
       
