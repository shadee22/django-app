from django.contrib import admin
from .models import Item, OrderItem

# Register your models here.

class OrderAdmin ( admin.ModelAdmin ) :
    list_display = [ 'item' , 'quantity' , 'ordered']

admin.site.register ( Item  )
admin.site.register ( OrderItem  , OrderAdmin)