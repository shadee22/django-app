from Core.views import HomeView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import AboutView, DetailView, HomeView, OrderSummeryView , remove , add, adding_single_item_to_cart ,removing_single_item_from_cart
# , add_to_order_summery

app_name = 'store'

urlpatterns = [
    path ( '' , HomeView.as_view() , name = 'home' ),
    path ( 'detail/<slug>/' , DetailView.as_view() , name = 'detail' ),
    path ('add-to-cart/<slug>' , add , name = 'add') , 
    path ('remove-from-cart/<slug>' , remove , name = 'remove') , 
    path ( 'order_summery/' , OrderSummeryView.as_view() , name = 'order-summery' ),
    path ( 'about/' , AboutView.as_view() , name =  'about'),
    path ( 'adding-single-item-to-cart/<slug>/' , adding_single_item_to_cart , name = 'adding-single-item-to-cart' ) , 
    path ( 'removing-single-item-from-cart/<slug>/' , removing_single_item_from_cart , name = 'removing-single-item-from-cart' ) , 
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)