
from app.models import Purchase
from django.urls import path
from .views import crop, fertilizer,edit_profile, homeview, searchcrop, contact, purchase_one,addseed, season,dashboard, soil,about,query, training,seed,purchase,add_to_cart
from .views import payment,LandingPage, successview, cancleview,CheckoutView
from .views import crop, fertilizer, homeview, searchcrop,profile, contact, purchase_one,addseed, season,dashboard, soil,about,query,view_cart, training,seed,purchase,add_to_cart,allcrops
from .views import payment
from .views import LandingPageCart

urlpatterns = [
    path('', homeview, name='home'),
    path('contact/',contact, name='contact'),
    path('about/',about, name='about'),
    path('addseed/',addseed, name='addseed'),
    path('soil/',soil, name='soil'),
    path('seed/',seed, name='seed'),
    path('season/',season, name='season'),
    path('profile/',profile, name='profile'),
    path('edit_profile/<int:pk>/',edit_profile, name='edit_profile'),
    path('crop/',crop, name='crop'),
    path('allcrops/',allcrops, name='allcrops'),
    path('dashboard/',dashboard, name='dashboard'),
    path('searchcrop/',searchcrop, name='searchcrop'),
    path('purchase/',purchase, name='purchase'),
    path('purchase/seed/<int:seedpk>',purchase_one, name='purchase_one'),
    path('add_to_cart/seed/<int:seedpk>',add_to_cart, name='add_to_cart'),
    path('view_cart/',view_cart,name='view_cart'),
    path('fertilizer/',fertilizer, name='fertilizer'),
    path('training/',training, name='training'),
    path('query/',query, name='query'),
    path('pay/<int:pk>',LandingPage.as_view(),name='paynow'),
    path('paycart/<int:amt>',LandingPageCart.as_view(),name='paycart'),
    path('success/', successview.as_view(), name='success'),
    path('cancel/', cancleview.as_view(), name='cancel'),
    path('checkout/<pk>/', CheckoutView.as_view(),name='checkout')
]