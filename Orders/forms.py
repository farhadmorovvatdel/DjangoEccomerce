from django import  forms
from django_countries.fields import CountryField

PAYMENT_CHOICES=(
    ('S','Stripe'),
    ('P','Paypal')
)
class CheckOutForm(forms.Form):
    street_address=forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={
        'placeholder':'Write Your Street',
         'class':'form-group col-md-12',
         'id':'street_address'
    }))
    apartemant_address=forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={
        'placeholder':'Write Your apartemant address',
         'class':'form-group col-md-12',
        'id': 'apartemant_address'
    }))
    country = CountryField(blank_label="(select country)").formfield(required=False)
    zip_cod=forms.CharField(required=False,widget=forms.TextInput(attrs={
        'placeholder':'Write Your zipcode',
         'class':'form-group col-md-12',
        'id': 'zip_cod'
    }))
    same_shipping_addres=forms.BooleanField(widget=forms.CheckboxInput())
    save_info=forms.BooleanField(widget=forms.CheckboxInput())
    payment_option=forms.ChoiceField(widget=forms.RadioSelect(),choices=PAYMENT_CHOICES)
