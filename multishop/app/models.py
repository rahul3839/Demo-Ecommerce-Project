
from xml.dom.pulldom import default_bufsize
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator ,MinValueValidator



class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=12)



class Contacts(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=200)

    def __str__(self):
        return self.name


#-----------------PRODUCT-----------------------------

CHOOSE_CATEGORIES = (
    ('Shirts','SHRITS'),
    ('Jeans', 'JEANS'),
    ('Blazers','BLEAZERS'),
    ('Jackets','JAKETS'),
    ('Shoes','SHOES'),
)

class Main_Product_Cate(models.Model):
    cate = models.CharField(max_length=100, choices=CHOOSE_CATEGORIES, default='shrits')

    def __str__(self):
        return self.cate

    
class Product(models.Model):
    category = models.ForeignKey(Main_Product_Cate,on_delete=models.CASCADE)
    product_id = models.AutoField
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    delete_price = models.IntegerField()
    rating = models.IntegerField(default=0,
        validators = [
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )
    image = models.ImageField(upload_to='app/static/img', default="")
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
         return str(self.id)

class Order(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    product = models.ForeignKey(Cart, on_delete=models.CASCADE)
    fname =models.CharField(max_length=100)
    lname =models.CharField(max_length=100)
    email =models.EmailField(max_length=100)
    phone =models.CharField(max_length=100)
    address =models.TextField(max_length=100)
    city =models.CharField(max_length=100)
    state =models.CharField(max_length=100)
    country =models.CharField(max_length=100)
    pincode =models.IntegerField()
    total_price = models.FloatField(max_length=100,default='1000')
    orderstatuses = (
        ('Pending','Pending'),
        ('Out Of Shipping','Out Of Shipping'),
        ('Completed','Completed'),
    )
    Status= models.CharField(max_length=100,choices=orderstatuses,default='Pending')
    date = models.DateTimeField(auto_now_add=True)


