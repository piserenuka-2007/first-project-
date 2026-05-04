from django.db import models

from django.contrib.auth.models import User



class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    description=models.TextField()
    image=models.ImageField(upload_to='products/')

def __str__(self):
    return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)


class Order(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     total=models.IntegerField()
     created_at=models.DateTimeField(auto_now_add=True)
     razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
     status=models.CharField(max_length=50,default='pending')

   

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()