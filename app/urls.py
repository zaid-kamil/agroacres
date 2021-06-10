
from app.models import Purchase
from django.urls import path
from .views import crop, fertilizer, homeview, searchcrop, contact, purchase_one,addseed, season,dashboard, soil,about,query, training,seed,purchase,add_to_cart
from .views import payment

urlpatterns = [
    path('', homeview, name='home'),
    path('contact/',contact, name='contact'),
    path('about/',about, name='about'),
    path('addseed/',addseed, name='addseed'),
    path('soil/',soil, name='soil'),
    path('seed/',seed, name='seed'),
    path('season/',season, name='season'),
    path('crop/',crop, name='crop'),
    path('dashboard/',dashboard, name='dashboard'),
    path('searchcrop/',searchcrop, name='searchcrop'),
    path('purchase/',purchase, name='purchase'),
    path('purchase/seed/<int:seedpk>',purchase_one, name='purchase_one'),
    path('addcart/seed/<int:seedpk>',add_to_cart, name='add_to_cart'),
    path('fertilizer/',fertilizer, name='fertilizer'),
    path('training/',training, name='training'),
    path('query/',query, name='query'),
    path('pay/<int:pk>',payment,name='paynow'),
]