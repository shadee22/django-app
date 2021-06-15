from django.forms.fields import CharField
from django.shortcuts import render , get_object_or_404, redirect 
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, Order, OrderItem
from django.views.generic import ListView , DetailView , View
from django.utils import timezone
from django.contrib import messages
from .forms import CheckoutForm , ShadeerForm
from django.conf import settings
# import stripe

class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = "Home-page.html"


class ItemDetailView(DetailView):
    model = Item 
    template_name = "detail-page.html"


def add_to_cart( request , slug ) :
    item = get_object_or_404 ( Item , slug = slug )


    order_item , created  = OrderItem.objects.get_or_create ( 
        item = item ,
        user = request.user ,
        ordered = False
    )


    order_qs = Order.objects.filter (user = request.user , ordered=False)

    if order_qs.exists() :
        order = order_qs[0]
        if order.items.filter ( item__slug=item.slug ).exists() :
             order_item.quantity += 1
             order_item.save()
             messages.info ( request , "Item addad to the cart " )
             return redirect ( "core:product" , slug= slug ) 

        else :
            order.items.add (order_item)
            messages.info ( request , "Item addad to the cart " )
            return redirect ( "core:product" , slug= slug ) 

    else :
        ordered_date = timezone.now()
        order = Order.objects.create ( 
            user = request.user , ordered_date = ordered_date
         )
        order.items.add ( order_item )

    return redirect ( "core:product" , slug= slug ) 

def remove_from_cart ( request , slug ) :
    item = get_object_or_404 ( Item , slug = slug )
    order_qs = Order.objects.filter (
        user = request.user , 
        ordered=False
    )

    if order_qs.exists() :
        order = order_qs[0]
        #check order item in the order
        if order.items.filter ( item__slug=item.slug ).exists() :
            order_item = OrderItem.objects.filter(
                item=item , 
                user = request.user ,
                ordered = False
            )[0]
            order.items.remove(order_item)
            messages.info ( request , "Item romoved from cart " )
        else :
            messages.info ( request , " There is no items in your order  ")
            return redirect ( "core:product" , slug= slug ) 
    else : 
        return redirect ( "core:product" , slug= slug ) 

    return redirect ( "core:product" , slug= slug ) 

class LoginView ( DetailView ) :
    template_name = "account/email.html"

class OrderSummery ( View ):
    def get( self , *args, **kwargs ) :
        try :
            order = Order.objects.get ( user=self.request.user , ordered=False  )
            context = {
                'object' : order
            }
            return render ( self.request , 'order-summery.html' , context )
        except ObjectDoesNotExist:
            messages.error (self.request , " Do not have Active Order " )
            return redirect("/")
        # return render( self.request , 'checkout.html' )

def remove_single_item_from_cart ( request , slug) :
    item = get_object_or_404 ( Item , slug= slug)
    order_qs = Order.objects.filter (
        user = request.user , 
        ordered=False
    )

    if order_qs.exists() :
        order = order_qs[0]
        #check order item in the order
        if order.items.filter ( item__slug=item.slug ).exists() :
            order_item = OrderItem.objects.filter(
                item=item , 
                user = request.user ,
                ordered = False
            )[0]
            if order_item.quantity > 1 :
                order_item.quantity -= 1
                order_item.save()   
            else :
                order.items.remove(order_item)
            messages.info ( request , " Cart is Updated")
            return redirect ( "core:order-summery")
        else :
            messages.info ( request , " There is no items in your order  ")
            return redirect ( "core:order-summery"   ) 
    else : 
        return redirect ( "core:order-summery"  , slug= slug   ) 

    return redirect ( "core:order-summery" , slug= slug) 

def adding_single_item_to_cart( request , slug ) :
    item = get_object_or_404 ( Item , slug = slug )
    order_item , created  = OrderItem.objects.get_or_create ( 
        item = item ,
        user = request.user ,
        ordered = False
    )
    order_qs = Order.objects.filter (user = request.user , ordered=False)

    if order_qs.exists() :
        order = order_qs[0]
        if order.items.filter ( item__slug=item.slug ).exists() :
             order_item.quantity += 1
             order_item.save()
             messages.info ( request , "Item addad to the cart " )
             return redirect ( "core:order-summery" ) 

        else :
            order.items.add (order_item)
            messages.info ( request , "Item addad to the cart " )
            return redirect ( "core:order-summery") 

    else :
        ordered_date = timezone.now()
        order = Order.objects.create ( 
            user = request.user , ordered_date = ordered_date
         )
        order.items.add ( order_item )

    return redirect ( "core:order-summery"  ) 
        
def remove_from_cart_chekout ( request , slug ) :
    
    item = get_object_or_404 ( Item , slug = slug )
    print (item)
    order_qs = Order.objects.filter (
        user = request.user , 
        ordered=False
    )

    if order_qs.exists() :
        order = order_qs[0]
        #check order item in the order
        if order.items.filter ( item__slug=item.slug ).exists() :
            order_item = OrderItem.objects.filter(
                item=item , 
                user = request.user ,
                ordered = False
            )[0]
            order.items.remove(order_item)
            messages.info ( request , "Item romoved from cart " )
        else :
            messages.info ( request , " There is no items in your order  ")
            return redirect ( "core:order-summery" , slug= slug ) 
    else : 
        return redirect ( "core:order-summery" , slug= slug ) 

    return redirect ( "core:order-summery" , slug= slug ) 

class Checkout (View) :
    
    def get (self , *args , **kwargs) :
        form = CheckoutForm()
        second_form = ShadeerForm()
        context = {
            'form' : form , 
            'second'  : second_form 
        }

        return render ( self.request , 'checkout.html' ,context)
    
    def post ( self , *args, **kwargs ):
        form = CheckoutForm( self.request.POST or None )
        if form.is_valid() :
            messages.warning ( self.request , "Failed Checkout-form")
            return redirect ( 'core:checkout-form' )
        messages.warning ( self.request , "Failed Checkout-form")
        print ( form )
        return redirect ( 'core:checkout-form' )

class PaymentView (View) :
    def get ( self , *args , **kwargs ) :
        return render ( self.request , 'payment.html'  )

                    

