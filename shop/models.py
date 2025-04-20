from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    date_modified=models.DateTimeField(User,auto_now=True)
    phone=models.CharField(max_length=20,blank=True)
    address1=models.CharField(max_length=200,blank=True)
    address2=models.CharField(max_length=200,blank=True)
    city=models.CharField(max_length=200,blank=True)
    state=models.CharField(max_length=200,blank=True)
    zipcode=models.CharField(max_length=200,blank=True)
    Country=models.CharField(max_length=200,blank=True)
    old_cart=models.CharField(max_length=200,blank=True,null=True)
    
    
    def __str__(self):
        return self.user.username
    
# create a user Profile by default when user sign up

def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile=Profile(user=instance)
        user_profile.save()
        
# Automate the profile thing 

post_save.connect(create_profile,sender=User)        
        
#categories of Products
class Category(models.Model):
    name=models.CharField( max_length=50)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='categories'
    
    
#Details of Customers
class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=12)
    email=models.EmailField(max_length=254)
    password=models.CharField(max_length=30)
    
    def __str__(self):
        return f'{self.first_name}{self.last_name}'
    
 
 # Details of all products
 
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(decimal_places=3,default=0,max_digits=7)
    description=models.CharField(max_length=800,default='',blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1,null=True)
    image=models.ImageField(upload_to='uploads/product/')
    
    #add sale stuff
    
    is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(decimal_places=2,default=0,max_digits=7)
    
    def __str__(self):
        return self.name



# Details of Orders
class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,default=1,)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=400,default='',blank=True)
    phone=models.CharField(max_length=10)
    date=models.DateTimeField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.product


