from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Category(models.TextChoices):
    ELECTRONICS = 'Electronics'
    LAPTOPS = 'Laptop'
    ARTS = 'Arts'
    FOOD = 'Food'
    HOME = 'Home'
    KITCHEN = 'Kitchen'


class Product(models.Model):
    name = models.CharField(max_length=100,default="",blank=False)
    description = models.TextField(max_length=1000,default="",blank=False)
    price = models.DecimalField(max_digits=7,decimal_places=3,default=0)
    brand = models.CharField(max_length=100,default="",blank=False)
    category = models.CharField(max_length=30,choices=Category.choices)
    ratings = models.DecimalField(max_digits=3,decimal_places=2,default=0)
    srock = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class ProductImages(models.Model):

    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image =  models.ImageField(upload_to="products")


@receiver(post_delete,sender=ProductImages)
def auto_delete(sender,instance,**kwargs):
    if instance.image:
        instance.image.delete(save=False)



class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,related_name="reviews")
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    ratings = models.IntegerField(default=0)
    comment = models.TextField(default="",blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
    
