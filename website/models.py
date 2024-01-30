from django.db import models
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class products(models.Model):
    sdate = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=1000000000,null=True)
    price = models.CharField(max_length=1000000000,null=True)
    ads = models.CharField(max_length=1000000000,null=True)
    revenue = models.CharField(max_length=1000000000,null=True)
    rank = models.CharField(max_length=1000000000,null=True)
    velocity = models.CharField(max_length=1000000000,null=True)
    created = models.CharField(max_length=1000000000,null=True)
    product_link = models.CharField(max_length=1000000000,null=True)
    status = models.CharField(max_length=1000000000,null=True)
    image_file = models.ImageField(upload_to='product_images',null=True,default="None")

    def __str__(self):
        return (self.title)
    

class store_detail(models.Model):
    sdate = models.DateField(auto_now_add=True)
    total_sale = models.CharField(max_length=1000000000,null=True)
    sale_growth_rate = models.CharField(max_length=1000000000,null=True)
    total_order = models.CharField(max_length=1000000000,null=True)
    order_growth_rate = models.CharField(max_length=1000000000,null=True)
    aov = models.CharField(max_length=1000000000,null=True)
    skus = models.CharField(max_length=1000000000,null=True)
    status = models.CharField(max_length=1000000000,null=True)
    image_file = models.ImageField(upload_to='graph_images',null=True,default="None")







