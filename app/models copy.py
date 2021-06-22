from collections import defaultdict
from django.db import models
from django.db.models import fields
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

gender_option = {
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Others'),

}

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be of 10 digits.")


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE, default='')
    Full_Name = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=6,choices = gender_option, default="")
    address = fields.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be of 10 digits.")
    mobile = models.CharField(max_length=15,validators=[phone_regex])
    email =models.EmailField( max_length=254)
    occupation = models.CharField(max_length=50)
    password = models.CharField(max_length=50,default="")
    img = models.ImageField(upload_to="users", height_field=None, width_field=None, max_length=None)
    updated_on = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name='Profile'
        verbose_name_plural='Profile'

    def __str__(self):
        return self.Full_Name

class Soil(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    img = models.ImageField(upload_to="soils", height_field=None, width_field=None, max_length=None)
    date = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name='Soil'
        verbose_name_plural='Soils'

    def __str__(self):
        return self.name

class Seed(models.Model):
    name = models.CharField(max_length=50)
    qty = models.CharField(max_length=50,default="")
    description = models.TextField()
    img = models.ImageField(upload_to="seeds", height_field=None, width_field=None, max_length=None)
    date = models.DateField(auto_now=True)
    price =  models.FloatField(default="")

    class Meta:
        verbose_name='Seed'
        verbose_name_plural='Seeds'

    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=50)
    sown = models.CharField( max_length=100)
    harvest = models.CharField(max_length=100)
    description = models.TextField()
    img = models.ImageField(upload_to="seasons", height_field=None, width_field=None, max_length=None)
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name='Season'
        verbose_name_plural='Seasons'

    def __str__(self):
        return self.name

class Fertilizer(models.Model):
    name = models.CharField(max_length=50)
    type_of = models.CharField(max_length=50)
    madeof = models.CharField(max_length=100)
    description = models.TextField()
    img = models.ImageField(upload_to="fertilzers", height_field=None, width_field=None, max_length=None)
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name='Fertilizer'
        verbose_name_plural='Fertilizers'
    def __str__(self):
        return self.name

class Crop(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    sown =models.CharField( max_length=50)
    harvest = models.CharField(max_length=50)
    soil = models.ForeignKey(Soil,on_delete=CASCADE)
    season = models.ForeignKey(Season,on_delete=CASCADE)
    fertilizer = models.ForeignKey(Fertilizer,on_delete=CASCADE)
    instruction = models.TextField()
    problem = models.TextField()
    img = models.ImageField(upload_to="crops", height_field=None, width_field=None, max_length=None)
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name='Crop'
        verbose_name_plural='Crops'
    def __str__(self):
        return self.name



class Contact(models.Model):
    name = models.CharField(max_length=25)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be of 10 digits.")
    mobile = models.CharField(max_length=15,validators=[phone_regex])
    
    email =models.EmailField( max_length=254)
    occupation = models.CharField(max_length=50)
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Contact'
        verbose_name_plural='Contacts'
    def __str__(self):
        return self.name

class Query(models.Model):
    name = models.CharField(max_length=25)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be of 10 digits.")
    mobile = models.CharField(max_length=15,validators=[phone_regex])
    email = models.EmailField( max_length=254)
    occupation = models.CharField(max_length=50)

    message = models.TextField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Query'
        verbose_name_plural='Queries'
    def __str__(self):
        return self.name

class TrainingRegistration(models.Model):
    name = models.CharField(max_length=25)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be of 10 digits.")
    mobile = models.CharField(max_length=15,validators=[phone_regex])
    email = models.EmailField(max_length=254)
    age = models.PositiveIntegerField()
    college = models.CharField( max_length=50)
    gender = models.CharField(max_length=50)
    address =  models.CharField(max_length=50)
    occupation = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Training Registration'
        verbose_name_plural='Training Registrations'
    def __str__(self):
        return self.name


class Purchase(models.Model):
   
    user = ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(default='Lucknow',max_length=32)
    country = models.CharField(max_length=32,default='India')
    pincode = models.CharField(max_length=6)
    date_ordered = models.DateTimeField(auto_now=True)
    total_amt = models.IntegerField(default=0.00)
    is_delivered =  models.BooleanField(default=False)
    product_details = models.TextField()
   

    class Meta:
        verbose_name='purchase'
        verbose_name_plural='purchases'
    def __str__(self):
        return f'{self.user.username} purchase #{self.pk}'

class Addseed(models.Model):
    name = models.CharField( max_length=50)
    price =  models.FloatField(default=25.00)
    qty = models.CharField(max_length=50, default="1 kg")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be of 10 digits.")
    mobile = models.CharField(max_length=15,validators=[phone_regex])
    address = fields.CharField(max_length=500, default='No address specified')
    date_ordered = models.DateTimeField(auto_now=True)
    total_amt = models.FloatField(default=0.00)
    product_detail = models.CharField( max_length=500,default="No Details")
    img = models.ImageField(upload_to="addseeds", height_field=None, width_field=None, max_length=None)

    class Meta:
        verbose_name='addseed'
        verbose_name_plural='addseeds'
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = ForeignKey(User,on_delete=CASCADE)
    seed = ForeignKey(Seed,on_delete=CASCADE)
    qty = models.PositiveIntegerField(verbose_name='quantity',default=1)
    added_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='cart'
        verbose_name_plural='cart'
    
    def __str__(self):
        return self.seed.name

