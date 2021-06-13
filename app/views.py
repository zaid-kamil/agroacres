from django.contrib.auth import login
from django.contrib.messages.api import success
from django.db import models
from django.db.models import query_utils
from django.views.generic.base import TemplateView
from stripe.api_resources import checkout, line_item, payment_method
from app.models import Fertilizer, Season, Seed,Purchase,Crop, Soil, Addseed
from django.shortcuts import redirect, render
from .forms import ContactForm, QueryForm,PurchaseForm,AddseedForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.views import View
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def homeview(request):
    ctx ={'title':'welcome'}
    return render(request,'index.html',context= ctx)


def contact(request):
    form=ContactForm()
    if request.method=="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your message has been submitted successfully")
            return redirect('contact')

    ctx = {'form':form}
    return render(request,'users/contact.html',ctx)


def addseed(request):
    form=AddseedForm()
    if request.method=="POST":
        form = AddseedForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Your data has been submitted successfully")
            return redirect('addseed')

    ctx = {'form':form}
    return render(request,'users/addseed.html',ctx)

def purchase(request):
    form = PurchaseForm()
    if 'cart' in request.session:
        cartdata = request.session['cart']
    return render(request,"users/purchase.html")

@login_required
def purchase_one(request,seedpk):
    form = PurchaseForm()
    seed = Seed.objects.get(pk=seedpk)
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            
            fd =form.save(commit=False)
            fd.user = request.user
            
            fd.product_details =f'''item : {seed.name}
            price : {seed.price}
            total : {form.cleaned_data.get('total_amt')}
            qty : {form.cleaned_data.get('qty')}
            '''
            task = fd.save()
            messages.success(request,"Please add payment details for completing purchase")
            return redirect('paynow',pk=fd.id)
    
    seed = Seed.objects.get(pk=seedpk)
    ctx = {
        'form':form,
        'seed':seed,
    }
    return render(request,"users/puchase_one.html",ctx)


# might get deleted
def payment(request,pk):
    # purchase = Purchase.objects.all()
    purchase = Purchase.objects.get(pk=pk)
    ctx = {'purchase':purchase}
    return render(request,'users/payment.html',ctx)


# new implementation with stripe 
from django.contrib.auth.mixins import LoginRequiredMixin
class LandingPage(LoginRequiredMixin, TemplateView):

    template_name = "users/payment.html"

  
    def get_context_data( self,**kwargs):
        # user = request.user
        product_id = self.kwargs["pk"]
        product = Purchase.objects.get(pk=product_id)
        context = super(LandingPage,self).get_context_data(**kwargs)
        context.update({
            "product":product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })

        return context

class CheckoutView(LoginRequiredMixin,TemplateView):
    
    def post(self, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Purchase.objects.get(pk=product_id)
        price = product.total_amt*100

        YOUR_DOMAIN = "http://127.0.0.1:8000"

        checkout_session =stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items = [
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': price,
                        'product_data': {
                            'name': product.product_details
                        },
                    },
                    'quantity':1
                },


            ],
            mode = 'payment',
            success_url = YOUR_DOMAIN+'/success',
            cancel_url = YOUR_DOMAIN + '/cancle'
        )
        return JsonResponse({
            'id': checkout_session.id
        })

class successview(LoginRequiredMixin,TemplateView):
    template_name = 'stripe/stripe_payment_success.html'

class cancleview(LoginRequiredMixin,TemplateView):
    template_name = 'stripe/stripe_payment_cancle.html'

#########################


def about(request):
    return render(request,"users/about.html")


    
def query(request):
    form=QueryForm()
    if request.method=="POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your query has been submitted successfully")
            return redirect('query')

    ctx = {'form':form}
    return render(request,"users/query.html",ctx)

def soil(request):
    soil = Soil.objects.all()
    ctx = {'soil':soil}
    return render(request,'product/soil.html',ctx)

def seed(request):
    seeds= Seed.objects.all()
    ctx = {'seeds':seeds}
    return render(request,'product/seed.html',ctx)

def dashboard(request):
    crop = Crop.objects.all()
    ctx = {'crop':crop}
    return render(request,'product/dashboard.html',ctx)

def allcrops(request):
    crop = Crop.objects.all()
    ctx = {'crop':crop}
    return render(request,'product/allcrops.html',ctx)

def searchcrop(request):
    query = request.GET.get('s','')
    if len(query) > 0:
        data = Crop.objects.filter(name__icontains = query)
        ctx = {'query':query,'results': data}
        if len(data)>0:
            messages.success(request,f"search result found for {query}")
        else:
            messages.error(request,f"search result not found for {query}")

    else:
        ctx = {"message": "No query is given"}

    return render(request,'product/searchcrop.html',ctx)

@login_required
def add_to_cart(request,seedpk):
    messages.success(request,'added to cart')
    return redirect(request, 'user/addcart.html')

def season(request):
    season= Season.objects.all()
    ctx = {'seeason':season}
    return render(request,'product/season.html')

def fertilizer(request):
    fertilizer = Fertilizer.objects.all()
    ctx = {'fertilizer':fertilizer}
    return render(request,'product/fertilizer.html')

def crop(request):
    crop= Crop.objects.all()
    ctx = {'crop':crop}
    return render(request,'product/crop.html')

def training(request):
     return render(request,'product/training.html')

