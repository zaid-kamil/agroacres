from django.contrib.auth import login
from django.db.models import query_utils
from app.models import Fertilizer, Season, Seed,Purchase,Crop, Soil, Addseed
from django.shortcuts import redirect, render
from .forms import ContactForm, QueryForm,PurchaseForm,AddseedForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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

def payment(request,pk):
    purchase = Purchase.objects.get(pk=pk)
    ctx = {'purchase':purchase}
    return render(request,'users/payment.html',ctx)




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

def searchcrop(request):
    query = request.GET.get('s','')
    if len(query) > 0:
        data = Crop.objects(name_contains = query)
        ctx = {'query':query,'results': data}
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

