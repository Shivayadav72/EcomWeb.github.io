from shop.models import Product,Profile

class Cart():
    def __init__(self,request):
        self.session=request.session        
        #get request
        self.request= request
        # get the current session key if it is exist
        
        cart=self.session.get('session_key')
        
        #if the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart=self.session['session_key']={}
            
        # make sure cart is available on all pages of site
        
        self.cart=cart
        
    def db_add (self, product, quantity):
        product_id=str(product)
        product_qty=str(quantity)
            #logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id]={'price':str(product.price)}
                self.cart[product_id]= int(product_qty) 
                self.session.modified=True   
        
        #deal with logged in user
                if self.request.user.is_authenticated:
                # get the current user profile
                    current_user=Profile.objects.filter(user__id=self.request.user.id)
            #convert {'3':1,'2':4} to {"3":1,"2":4}
                    carty=str(self.cart)
                    carty=carty.replace("\'", "\"")
            #save carty to Profile Model
                    current_user.update(old_cart=str(carty))
            
        
    def add(self,product,quantity):
        product_id=str(product.id)
        product_qty=str(quantity)
        #logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id]={'price':str(product.price)}
            self.cart[product_id]= int(product_qty)
        self.session.modified=True   
        
        #deal with logged in user
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user=Profile.objects.filter(user__id=self.request.user.id)
            #convert {'3':1,'2':4} to {"3":1,"2":4}
            carty=str(self.cart)
            carty=carty.replace("\'","\"")
            #save carty to Profile Model
            current_user.update(old_cart=str(carty))
        
        
    def cart_total(self):
        #get products IDS
        product_ids= self.cart.keys()    
        #lookup those keys in our products database
        products=Product.objects.filter( id__in = product_ids)
        #get quantities
        quantities=self.cart 
        #start counting at 0
        total = 0
        for key,value in quantities.items():
            key=int(key)
            for prodcut in products:
                if Product.id == key:
                    total= total + (Product.price * value)
        
        return total
        
   
    def __len__(self):
        return len(self.cart)    
    
    
    def get_prods(self):
        product_ids=self.cart.keys()

        products= Product.objects.filter( id__in =product_ids)
        
        return products
    
    def get_quants(self):
        quantities= self.cart
        return quantities
    
    def update(self, product, quantity):
        
        product_id= str(product)
        product_qty=  int(quantity)

        #get cart 
        ourcart = self.cart
        
        # update Dictionary/cart
        
        ourcart[product_id]= product_qty
        
        self.session.modified = True 
  
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user=Profile.objects.filter(user__id=self.request.user.id)
            #convert {'3':1,'2':4} to {"3":1,"2":4}
            carty=str(self.cart)
            carty=carty.replace("\'", "\"")
            #save carty to Profile Model
            current_user.update(old_cart=str(carty))
            
            thing= self.cart
        return thing
    
    def delete(self, product):
        product_id=str(product)
        #Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified=True    
        
        if self.request.user.is_authenticated:
            # get the current user profile
            current_user=Profile.objects.filter(user__id=self.request.user.id)
            #convert {'3':1,'2':4} to {"3":1,"2":4}
            carty=str(self.cart)
            carty=carty.replace("\'", "\"")
            #save carty to Profile Model
            current_user.update(old_cart=str(carty))
        