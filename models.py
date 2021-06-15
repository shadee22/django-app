from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField

cato_choices = (
    ('S' ,'Shirt'),
    ('SW' , 'Sport Wear'),
    ('OW' , 'Out Wear'),
)
  
label_choices = (
    ('N' ,'New'),
    ('B' , 'Best Selling'),
    ('T' , 'Trendy'),
)
class Item ( models.Model ) :
    title = models.CharField(max_length=100)
    price = models.FloatField ()
    discount_price = models.FloatField ( blank=True , null=True )
    catogary= models.CharField ( choices=cato_choices , max_length=2 )
    description = models.TextField()
    label = models.CharField ( choices=label_choices , max_length=1 , blank=True , null=True  )
    slug = models.SlugField ()
    image = models.ImageField()

    def __str__(self):
        return self.title
    

#reverse problem wandha idhu ulluka thaan solution ( reverse with no argument found  )
    
    def get_absolute_url(self):
        return reverse ( 'core:product' , kwargs = {
            'slug' : self.slug
        } )

    def get_add_to_cart_url ( self ) :
        return reverse( 'core:add-to-cart' , kwargs = {
            'slug' : self.slug
        } )
        
    def get_remove_from_cart_url ( self ) :
        return reverse( 'core:remove-from-cart' , kwargs = {
            'slug' : self.slug
        } )
        
        

class OrderItem ( models.Model ) :
    user = models.ForeignKey ( settings.AUTH_USER_MODEL , on_delete=models.CASCADE , blank=True , null=True)
    item = models.ForeignKey ( Item , on_delete=models.CASCADE )
    quantity = models.IntegerField ( default =   1 )
    ordered = models.BooleanField ( default=False )

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
        
    def get_total_price ( self ) : 
        return self.quantity * self.item.price
        
    def get_total_discount_price ( self ) : 
        return self.quantity * self.item.discount_price

    def get_saved_amount ( self ) :
        return self.get_total_price() - self.get_total_discount_price()

    def get_final_price (self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_price()


class Order( models.Model ) :
    user = models.ForeignKey ( settings.AUTH_USER_MODEL , on_delete=models.CASCADE )
    ordered = models.BooleanField ( default=False )
    items = models.ManyToManyField ( OrderItem )
    ordered_date = models.DateTimeField ()
    # billing_address = models.ForeignKey( 
    #     "BillingAddress" , on_delete=models.SET_NULL , blank=True , null=True)
    # payment = models.ForeignKey(
    #     'Payment' , on_delete=models  .SET_NULL , blank=True , null=True
    # )
    coupen = models.ForeignKey(
        'Coupen' , on_delete=models.SET_NULL , blank=True , null=True 
    )
    
    def __str__(self):
        return self.user.username   

    def get_total(self) :
        total = 0 
        for order_item in self.items.all():
            total += order_item.get_final_price()
        total -= self.coupen.amount 
        return total

class BillingAddress( models.Model ):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    street_address = models.CharField(max_length=50)
    appartment_address = models.CharField(max_length=50)
    country = CountryField()
    zip = models.CharField(max_length=50)


class Coupen ( models.Model ) :
    code = models.CharField( max_length=15)
    amount = models.FloatField()

    
    def __str__ (self) :
        return self.code 

# class Payment ( models.Model ) :
#     # user = models.ForeignKey( settings.AUTH_USER_MODEL , on_delete=models.SET_NULL , blank=True , null=True )
#     # amount = models.FloatField()
#     # timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__ (self) :
#         self.user.username


    