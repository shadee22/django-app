from django.shortcuts import get_object_or_404, render , redirect
from django.views.generic import View ,   ListView , DetailView
from .models import Item , OrderItem
from django.core.mail import send_mail

#####for item in object_list { ListView }
############template accessing "object.name" {DetailView ""}

class HomeView(ListView) : 
    # def get(self , *args, **kwargs) : 
    #     return render (self.request , "home.html")

    model = Item 
    template_name = "home.html"

class DetailView(View) : 
    def get(self , *args ,   slug) : 
        items = get_object_or_404 ( Item , slug = slug) 
        # items = Item.objects.get_or_create ( slug = slug )



        product_count = get_object_or_404 ( OrderItem , item = items  )

        context = {
            'item' : items ,
            'count' : product_count,
        }
        
        return render (self.request , "detail.html" , context )
    # model = Item 
    # template_name = "detail.html"

def add (request ,slug):
    item = get_object_or_404 ( Item ,  slug= slug )

    order_item  = OrderItem.objects.get_or_create ( 
        item = item 
    )
    order_item[0].ordered = True
    order_item[0].quantity = order_item[0].quantity +  1
    order_item[0].save()

    return redirect (  'store:detail' , slug = slug ) 

def remove (request ,slug):
    item = get_object_or_404 ( Item ,  slug= slug )


    order_items = OrderItem.objects.filter ( item = item , ordered= True)

    
    if order_items.exists():
        order_item = order_items[0]


        if order_item.quantity >= 1 :

            order_item.quantity = order_item.quantity -  1
            order_item.save()

            if order_item.quantity == 0 :
                    order_item.quantity = 0 
                    order_item.ordered = False 
                    order_item.save()
                
    
    return redirect (  'store:detail' , slug = slug ) 

def adding_single_item_to_cart ( request , slug) :
    items = get_object_or_404 ( Item , slug = slug  )

    order_item = OrderItem.objects.get ( item = items )
    
    print ( order_item.quantity )

    order_item.quantity += 1
    order_item.save()

    return redirect (  'store:order-summery'  )
    
    

    def adding_single_item_to_cart ( request , slug) :
        items = get_object_or_404 ( Item , slug = slug  )

    order_item = OrderItem.objects.get ( item = items )
    
    print ( order_item.quantity )

    order_item.quantity += 1
    order_item.save()

    return redirect (  'store:order-summery'  )
    
    def adding_single_item_to_cart ( request , slug) :
        items = get_object_or_404 ( Item , slug = slug  )

    order_item = OrderItem.objects.get ( item = items )
    
    print ( order_item.quantity )

    order_item.quantity += 1
    order_item.save()

    return redirect (  'store:order-summery'  )
    
    def adding_single_item_to_cart ( request , slug) :
        items = get_object_or_404 ( Item , slug = slug  )

    order_item = OrderItem.objects.get ( item = items )
    
    print ( order_item.quantity )

    order_item.quantity += 1
    order_item.save()

    return redirect (  'store:order-summery'  )
    
    def adding_single_item_to_cart ( request , slug) :
        items = get_object_or_404 ( Item , slug = slug  )

    order_item = OrderItem.objects.get ( item = items )
    
    print ( order_item.quantity )

    order_item.quantity += 1
    order_item.save()

    return redirect (  'store:order-summery'  )
    
def removing_single_item_from_cart ( request , slug) :
    items = get_object_or_404 ( Item , slug = slug  )
    order_item = OrderItem.objects.get ( item = items )

    order_item.quantity -= 1
    order_item.save()

    return redirect (  'store:order-summery'  )
    
    
    
class OrderSummeryView (ListView ):
    #  def get(self , *args, **kwargs) : 
        # return render (self.request , "order-summery.html")
    model = OrderItem
    template_name = "order-summery.html"




    
class AboutView ( View ):
     def get(self , *args, **kwargs) : 
        return render (self.request , "about.html")