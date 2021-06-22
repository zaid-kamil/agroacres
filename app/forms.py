from django import forms
from django.forms import ModelForm

from .models import Contact,Query,Purchase,Addseed,Profile



class ContactForm(ModelForm):
    
    class Meta:
        model = Contact
        fields = ("name","email","mobile","occupation","message")


class QueryForm(ModelForm):
    
    class Meta:
        model = Query
        fields = ("name","email","mobile","occupation","message")



class PurchaseForm(ModelForm):
    
    total_amt =forms.FloatField(required=False, disabled=False)
    qty = forms.IntegerField()
    class Meta:
        
        model = Purchase
        fields = ('address','city','country','pincode','qty', 'total_amt')



class AddseedForm(ModelForm):
    

    class Meta:
        
        model = Addseed
        fields = ('name','mobile','address','total_amt','price','product_detail','img')

class ProfileForm(ModelForm):
    
    class Meta:
        model = Profile
        fields = ('name','address','email','mobile','occupation')