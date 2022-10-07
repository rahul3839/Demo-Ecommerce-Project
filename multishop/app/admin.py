from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class Admincustomeruser(admin.ModelAdmin):
    list_display = ['id' ,'username']

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['id' ,'user','product','fname','lname','email','phone','address','city','state','country','pincode','total_price','Status','date']

admin.site.register(Cart)
# class CartModelAdmin(admin.ModelAdmin):
#     list_display = ['id','user','product','quantity']

admin.site.register(Contacts)

admin.site.register(Product)
    
admin.site.register(Main_Product_Cate)




