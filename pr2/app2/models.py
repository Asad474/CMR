from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=10,null=True)
    email=models.EmailField(unique=True,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    profile_pic=models.ImageField(null=True,blank=True,default="logo.png")

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name=models.CharField(max_length=200,null=True)
    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    CATEGORY=(('Indoor','Indoor'),
              ('Outdoor','Outdoor')  
             )

    name=models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)
    description=models.CharField(max_length=200,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True)
    tags=models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    STATUS=(('Pending','Pending'),
            ('Out for delievery','Out for delievery'),
            ('Delieverd','Delieverd') 
           )

    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)        
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)        
    date_created=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    note=models.CharField(max_length=200,null=True)

    def __str__(self) -> str:
        return self.product.name