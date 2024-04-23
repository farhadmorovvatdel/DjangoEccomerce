from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.utils import  timezone

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
    image=models.ImageField()
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




class Gallery(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='item_images')
    description=models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return f'Image of {self.item.title}'





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
        if self.item.discount_price == 0:
            return f'{0}$'
        return (self.get_total_item_price() - self.get_total_discount_item_price())

    def get_final_price(self):
        if self.item.discount_price != 0:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    orderd_date=models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billding_address=models.ForeignKey('BilldingAddress',on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total=0
        for order_item in self.items.all():
            total+=order_item.get_final_price()
        order_discounts = OrderDiscount.objects.filter(order=self)
        for order_discount in order_discounts:
            total -= float(order_discount.discount_code.discount_price)
            if total <=0:
                total=0
        return  total
    def after_dicount(self):
        total=self.get_total()
        order_discounts = OrderDiscount.objects.filter(order=self)
        for order_discount in order_discounts:
            total -= float(order_discount.discount_code.discount_price)
            if total<=0:
                total=0
                return total
        return total
class BilldingAddress(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    street_address=models.CharField(max_length=100)
    apartemant_address=models.CharField(max_length=100)
    country=CountryField(multiple=False)
    zip_cod=models.CharField(max_length=100)
    def __str__(self):
        return  self.user.username

class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    def __str__(self):
        return self.code



class OrderDiscount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('order', 'discount_code')

    def __str__(self):
        return f'{self.order.user, self.discount_code.code}'










