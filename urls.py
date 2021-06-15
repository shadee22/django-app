from django.urls import path
from .views import ( Checkout, HomeView , ItemDetailView, LoginView, OrderSummery, PaymentView,
                     add_to_cart, adding_single_item_to_cart,
                     remove_from_cart , remove_single_item_from_cart , remove_from_cart_chekout  )

app_name = "core"


urlpatterns = [
    path ( '' , HomeView.as_view()  , name='home') ,
    path ( 'product/<slug>/' , ItemDetailView.as_view()  , name='product') ,
    path ( 'checkout/' , OrderSummery.as_view()  , name='order-summery') ,
    path ( 'add-to-cart/<slug>' , add_to_cart , name = 'add-to-cart' ) ,
    path ( 'remove-from-cart/<slug>' , remove_from_cart ,  name = 'remove-from-cart' ) , 
    path ( 'accounts/login/' , LoginView.as_view() ,  name = 'email' ) , 
    path ( 'removing-single-item/<slug>/' , remove_single_item_from_cart ,  name = 'remove-single-item' ) , 
    path ( 'adding-single-item/<slug>/' , adding_single_item_to_cart ,  name = 'adding-single-item' ) , 
    path ( 'remove-from-cart-checkout/<slug>/' , remove_from_cart_chekout ,  name = 'remove-from-cart-checkout' ) , 
    path ( 'checkout-form/', Checkout.as_view() , name = 'checkout-form' ) , 
    path ( 'payment/<payment_option>/', PaymentView.as_view() , name = 'payment' ) , 
]
