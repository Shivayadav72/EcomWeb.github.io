from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from shop.models import Product,Profile
import datetime

def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order=Order.objects.get(id=pk)
        items=OrderItem.objects.filter(order=pk)
        
        if request.POST:
            status=request.POST['shipping_status']
        # Check if true or false
        if status=="true":
            #get the order
            order=Order.objects.filter(id=pk)
        # update the status 
            now=datetime.datetime.now()
            order.update(shipped=True,date_shipped=now)
        else:
            #get the order
            order=Order.objects.filter(id=pk)
        # update the status 
            order.update(shipped=False)
            
            messages.success(request,"Shipping Status Updated")
            return redirect('home')
        return render(request,'payment/orders.html',{"order":order,"items":items})

    
    else:
        messages.success(request,"Item not Shippped Yet")
        return redirect('home')
        


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        order=Order.objects.filter(shipped=False)
        if request.POST:
            status=request.POST['shipping_status']
            num=request.POST['num']
            order=Order.objects.filter(id=num)
            # grab date and time
            now=datetime.datetime.now()
            # Update Order
            order.update(shipped=True,date_shipped=now)   
            #redirect 
            messages.success(request,"Shipping Status Updated")
            return redirect('home')
        
        return render(request,"payment/not_shipped_dash.html",{"order":order})
    else:
        messages.success(request,"Item not Shippped Yet")
        return redirect('home')

def shipped_dash(request):
    
    if request.user.is_authenticated and request.user.is_superuser:
        order=Order.objects.filter(shipped=True)
        if request.POST:
            status=request.POST['shipping_status']
            num=request.POST['num']
            order=Order.objects.filter(id=num)
            # grab date and time
            now=datetime.datetime.now()
            # Update Order
            order.update(shipped=False)   
            #redirect 
            messages.success(request,"Shipping Status Updated")
            return redirect('home')
        return render(request,"payment/shipped_dash.html",{"order":order})
    else:
        messages.success(request,"Item  Shippped Yet")
        return redirect('home')


def process_order(request):
    if request.POST:
        cart=Cart(request)
        cart_prodcuts=cart.get_prods
        quantities=cart.get_quants
        totals=cart.cart_total()
        # get billing info from the last page 
        payment_form=PaymentForm(request.POST or None)
        #get shipping Session data
        my_shipping=request.session.get('my_shipping')
        
        #gather order info
        full_name=my_shipping['shipping_full_name']
        email=my_shipping['shipping_email']
        #create shipping address from session info
        shipping_address=f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_country']}"
        amount_paid= totals
        
        #create an Order
        if request.user.is_authenticated:
            #logged in
            user=request.user
            #create order
            create_order=Order(user=user,full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()
            
            #add Order Item
            #get the order ID
            order_id=create_order.pk
            
            #get product info
            for product in cart_prodcuts():
            # Get Product id    
                product_id=product.id
                # Get product price
                
                if product.is_sale:
                    price=product.sale_price
                else:
                    price=product.price
                # get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        #create Order item
                        create_order_item=OrderItem(order_id=order_id,product_id=product_id, user=user,quantity=value,price=price,)
                        create_order_item.save()
                        

            # Delete Cart
            for key in list(request.session.keys()):
                if key=="session_key":
                    # Delete Key
                    del request.session[key]    
                    
                    # Delete cart from databse (old_cart field)
                    current_user=Profile.objects.filter(user__id=request.user.id)
                    #delete shopping cart in database(old_cart field)
                    current_user.update(old_cart="")

            
            messages.success(request,("Order Placrd!!"))
            return redirect('home')
        else:    
            
            #not logged in
            #create order
            create_order=Order(full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()
            
            #add Order Item
            #get the order ID
            order_id=create_order.pk
            
            #get product info
            for product in cart_prodcuts():
            # Get Product id    
                product_id=product.id
                # Get product price
                
                if product.is_sale:
                    price=product.sale_price
                else:
                    price=product.price
                # get quantity
                for key,value in quantities().items():
                    if int(key)==product.id:
                        #create Order item
                        create_order_item=OrderItem(order_id=order_id,product_id=product_id,quantity=value,price=price,)
                        create_order_item.save()
            # Delete Cart
            for key in list(request.session.keys()):
                if key=="session_key":
                    # Delete Key
                    del request.session[key]
                
            messages.success(request,("Order Placrd!!"))
            return redirect('home')
        
    else:
        messages.success(request,("Access Denied"))
        return redirect('home')
    

def billing_info(request):
    if request.POST:
        cart=Cart(request)
        cart_prodcuts=cart.get_prods
        quantities=cart.get_quants
        totals=cart.cart_total()
        
        #create a session with Shipping Info
        my_shipping=request.POST
        request.session['my_shipping']=my_shipping
        
        #check if the user is logged in 
        if request.user.is_authenticated:
            #get the billing form
            billing_form=PaymentForm()
            
            return render(request,"payment/billing_info.html",{"cart_prodcuts":cart_prodcuts,"quantities":quantities,"totals":totals,"shipping_info":request.POST,"billing_form":billing_form})
        else:
            # not logged in 
            billing_form=PaymentForm()
            return render(request,"payment/billing_info.html",{"cart_prodcuts":cart_prodcuts,"quantities":quantities,"totals":totals,"shipping_info":request.POST,"billing_form":billing_form})
            shipping_form=request.POST
            return render(request,"payment/billing_info.html",{"cart_prodcuts":cart_prodcuts,"quantities":quantities,"totals":totals,"shipping_form":shipping_form})
    else:
        messages.success(request,("Access Denied"))
        return redirect('home')
    
        
        

def checkout_cart(request):
    cart=Cart(request)
    cart_prodcuts=cart.get_prods
    quantities=cart.get_quants
    totals=cart.cart_total()
    
    if request.user.is_authenticated:
        shipping_user= ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form= ShippingForm(request.POST or None, instance=shipping_user)
        return render(request,"payment/checkout_cart.html",{"cart_prodcuts":cart_prodcuts,"quantities":quantities,"totals":totals,"shipping_form":shipping_form})
    else:
        shipping_form= ShippingForm(request.POST or None)
        return render(request,"payment/checkout_cart.html",{"cart_prodcuts":cart_prodcuts,"quantities":quantities,"totals":totals,"shipping_form":shipping_form})
    

def payment_success(request):
    return render(request, "payment/payment_success.html",{})