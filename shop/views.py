from django.shortcuts import render,redirect
from .models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
import json
from cart.cart import Cart


def search(request):
    if request.method =='POST':
        searched=request.POST['searched']
        #Query The Product DB model
        searched= Product.objects.filter(name__icontains=searched) 
        # test for null
        if not searched:
            messages.success(request,("Sorry Entered Product doesn't Exist"))
            return render(request,"search.html",{})
        else:
            return render(request,"search.html",{'searched':searched})
        
    else:    
        return render(request,"search.html",{})


def update_info(request):
    if request.user.is_authenticated:
        # Get current user
        current_user = Profile.objects.get(user__id=request.user.id)
        
        #get current userinfo
        shipping_user= ShippingAddress.objects.get(user__id=request.user.id)
        
        #get original user form 
        form= UserInfoForm(request.POST or None, instance=current_user)
        #get user's Shipping form
        
        shipping_form= ShippingForm(request.POST or None, instance=shipping_user)
        
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            login(request,current_user)
            messages.success(request,"Your Info has been Updated!!!")
            return redirect('home')
        return render(request,"update_info.html",{'form':form,'shipping_form':shipping_form})    
    else:
        messages.success(request,("You must be logged in"))
        return redirect('home')
    



def update_password(request):
    if request.user.is_authenticated:
        current_user=request.user
        
        if request.method=='POST':
            form=ChangePasswordForm(current_user,request.POST)
            
            if form.is_valid():
                form.save()
                messages.success(request,"Your password has been updated you can LogIn ")
                login(request,current_user)
                return redirect('update_user')
                
            else:
                for error in list(form.errors.values()):
                        messages.error(request,error)
                        return redirect('update_password')
        else:
            form=ChangePasswordForm(current_user)
            return render(request,"update_password.html",{'form':form})

    else:
        messages.success(request,("You must have been logged in"))
        return redirect('home')

def update_user(request):
    
    
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form= UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            
            login(request,current_user)
            messages.success(request,"User has been Updated!!!")
            return redirect('home')
        return render(request,"update_user.html",{'user_form':user_form})    
    else:
        messages.success(request,("You must be logged in"))
        return redirect('home')
    

def category_summary(request):
    categories=Category.objects.all()
    return render(request,'category_summary.html',{"categories":categories})
 
def category(request,foo):
    foo= foo.replace('-',' ')
    try:
        
        category=Category.objects.get(name=foo)
        products=Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products,'category':category})
        
    except:
        messages.success(request,("That Category Doesn't Exist"))
        return redirect('home')



def product(request,pk):
    product=Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})
    

def home(request):
    products=Product.objects.all()
    return render(request,'home.html',{'products':products})
    
    
def about(request):
    return render(request,'about.html',{})

def login_user(request):
    if request.method =="POST":
        username=request.POST['username']
        password=request.POST['password']
        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            # do some shopping cart stuff
            
            current_user= Profile.objects.get(user__id=request.user.id)
            # get theri saved cart from database

            saved_cart= current_user.old_cart
            #convert database string to python dictionary

            if saved_cart:
                #convert to dictionary using JSON
                converted_cart= json.loads(saved_cart)
                #Add the loaded cart dictionary to our session
                #get the cart
                cart= Cart(request)
                #loop thru the cart and add the items from the database
                   
                for key,value in converted_cart.items():
                    cart.db_add( product=key, quantity=value)
                    
                    messages.success(request,("You have been Logged In"))
            return redirect('home')
        else:
            messages.success(request,("There was an error try again"))
            return redirect('login')
            
        
    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("You logged Out!!!..."))
    return redirect('home')


def register_user(request):
    form=SignUpForm()
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            #User Login
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("Welcome...! You have Registerd Successfully"))
            return redirect('home')
        else: 
            messages.success(request,("Whoopss...! There was problem in Registering, Please Try Again...."))
            return redirect('register')
            
    else:
        return render(request,'register.html',{'form':form})
            
        
    
        
    
    
