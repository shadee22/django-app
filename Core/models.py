from django.db import models
from django.db.models.deletion import CASCADE
from django.shortcuts import reverse

# Create your models here.

class Item (models.Model) :
    name = models.CharField (max_length=20)
    price = models.FloatField()
    discription = models.CharField ( max_length = 200 ,  blank=True , null= True)
    image = models.ImageField(upload_to='users/%Y/%m/%d/')
    slug = models.SlugField()

    def __str__(self) :
        return self.name
    
#slug use panna pokala idha parunga 
    def get_absolute_url ( self ) :
        return reverse ( "store:detail" , kwargs = {
            'slug' : self.slug  
        } )
    
    def add_to_cart_url ( self ) :
        return reverse ( "store:add" , kwargs = {
            'slug' : self.slug
        } )
    def remove_from_cart ( self  ) :
        return reverse  ("store:remove" , kwargs = {
            'slug' : self.slug
        })

class OrderItem (models.Model) : 
    item = models.ForeignKey ( Item , on_delete=models.CASCADE )
    quantity = models.IntegerField (default=0)
    ordered = models.BooleanField (default=False)
    # slug = models.ManyToManyField ()

    def __str__(self) :
        return str(self.item)

    def total ( self ) :
        return self.quantity * self.item.price 