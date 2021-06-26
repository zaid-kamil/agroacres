from re import L
from django.contrib.auth import login
from django.contrib.messages.api import success
from django.db import models
from django.db.models import query_utils
from django.views.generic.base import TemplateView
from stripe.api_resources import checkout, line_item, payment_method
from app.models import Cart, Fertilizer, Season, Seed,Purchase,Crop, Soil, Addseed,Profile
from django.shortcuts import redirect, render
from .forms import ContactForm, QueryForm,PurchaseForm,AddseedForm,ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse, request
from django.views import View
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def homeview(request):
    ctx ={'title':'welcome'}
    return render(request,'index.html',context= ctx)

@login_required
def profile(request):
    users = Profile.objects.filter(user__pk=request.user.pk)
    if len(users)==1:
        context= {'profile':users}
    else:
        context = {'profile': None}
    return render(request, 'users/profile.html',context)

def edit_profile(request, pk):
    try:
        udata = Profile.objects.filter(pk=pk)
        if len(udata)==1:
            form = ProfileForm(instance=udata[0])
        else:
            form = ProfileForm()
        if request.method=='POST':
            if len(udata)==1:
                form = ProfileForm(request.POST, request.FILES, instance=udata[0])
            else:
                form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                fd=form.save(commit=False)
                fd.user=request.user
                fd.email=request.user.email
                fd.save()
                return redirect('profile')
            else:
                print("form is invalid")
        context = {"form":form}
        return render(request, 'users/edit_profile.html', context)
    except Exception as e:
        print('some error occurred',e)
        return redirect('profile')

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

@login_required
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

@login_required
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
@login_required
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
            cancel_url = YOUR_DOMAIN + '/cancel'
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


@login_required   
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
    
    return render(request,'product/soil.html')

def seed(request):
    seeds = Seed.objects.all()
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
        data1 = Crop.objects.filter(name__icontains = query)
        data2 = Soil.objects.filter(name__icontains = query)
        data3 = Fertilizer.objects.filter(name__icontains = query)
        data4 = Season.objects.filter(name__icontains = query)

        ctx = {'query':query,'results1': data1, 'results2': data2 , 'results3': data3, 'results4': data4}
       
    



    else:
        ctx = {"message": "No query is given"}

    return render(request,'product/searchcrop.html',ctx)

@login_required
def add_to_cart(request,seedpk):
    
    seed = Seed.objects.get(pk=seedpk)
    cart = Cart(user=request.user,seed=seed)
    cart.save()
    messages.success(request,f"  {seed.name} : Product addded to cart")
    return redirect('seed')

@login_required
def view_cart(request):
    cart = Cart.objects.filter(user__pk=request.user.pk)
    # print("test",cart)
    ctx={'cart':cart}
    return render(request,'users/view_cart.html',ctx)

class LandingPageCart(LoginRequiredMixin, TemplateView):
    template_name = "users/purchase.html"

    def get_context_data(self, **kwargs):
        # cart_id = request.user
        amt_id = self.kwargs["amt"]
        # print(amt_id)
        cart = Cart.objects.all()
        contxt = super(LandingPageCart,self).get_context_data(**kwargs)
        contxt.update({
            "cart": cart,
            "amt":amt_id,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })

        return contxt

class CheckoutViewCart(LoginRequiredMixin, TemplateView): 
    
    def post(self, *args, **kwargs):

        amt_id = self.kwargs["price"]
        price = amt_id*100
        print('amount: ', amt_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"

        checkout_session =stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items = [
                {
                     
                        'name':'Cart Purchase',
                        'quantity':1,
                        'currency':'inr',
                        'amount': int(price),
                    
                },


            ],
            mode = 'payment',
            success_url = YOUR_DOMAIN+'/success',
            cancel_url = YOUR_DOMAIN + '/cancel'
        )
        return JsonResponse({
            'id': checkout_session.id
        })


# class LandingPageCart(LoginRequiredMixin, TemplateView):

#     template_name = "users/payment.html"

  
#     def get_context_data( self,**kwargs):
#         # user = request.user
#         product_id = self.kwargs["pk"]
#         product = Purchase.objects.get(pk=product_id)
#         context = super(LandingPage,self).get_context_data(**kwargs)
#         context.update({
#             "product":product,
#             "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
#         })

#         return context

def season(request):
    
    return render(request,'product/season.html')

def fertilizer(request):
    
    return render(request,'product/fertilizer.html')

def crop(request):
    crop= Crop.objects.all()
    ctx = {'crop':crop}
    return render(request,'product/crop.html')

def training(request):
     return render(request,'product/training.html')

