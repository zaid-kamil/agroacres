
from django import contrib
from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from django.conf  import settings
# from app.views import (
#     CreateCheckoutSession,
#     SuccessView,
#     CancelView
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('user',include('userauth.urls')),
    
    path('accounts/',include('django.contrib.auth.urls')),
    
#     path('cancel/', CancelView.as_view(), name='cancel'),
#     path('success/', SuccessView.as_view(), name='success'),
#     path('create-checkout-session/<pk>/', CreateCheckoutSession.as_view(), name='create-checkout-session')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)