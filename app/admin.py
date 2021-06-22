from app.models import Addseed, Cart, Contact, Crop, Fertilizer, Purchase, Query, Season, Seed, Soil, TrainingRegistration ,Profile
from django.contrib import admin

# Register your models here.
admin.site.register(Profile)
admin.site.register(Soil)
admin.site.register(Season)
admin.site.register(Seed)
admin.site.register(Cart)
admin.site.register(Fertilizer)
admin.site.register(Crop)
admin.site.register(Purchase)
admin.site.register(Addseed)
admin.site.register(Contact)
admin.site.register(Query)
admin.site.register(TrainingRegistration)
