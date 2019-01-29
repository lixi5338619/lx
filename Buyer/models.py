from django.db import models
# Create your models here.


'''买家'''
class Buyer(models.Model):
    username = models.CharField(max_length = 32)
    password = models.CharField(max_length = 32)
    email = models.EmailField(blank = True,null = True)
    phone = models.CharField(max_length = 32,blank = True,null = True)
    photo = models.ImageField(upload_to = "buyer/images",blank = True,null = True)
    vip = models.CharField(max_length = 32,blank = True,null = True)


'''邮箱验证'''
class EmailValid(models.Model):
    value = models.CharField(max_length = 32)
    email_address = models.EmailField()
    times = models.DateTimeField()


'''买家购物车'''
class BuyCar(models.Model):
    goods_id = models.CharField(max_length=32)
    goods_name = models.CharField(max_length=32)
    goods_price = models.FloatField()
    goods_picture = models.ImageField(upload_to="image")
    goods_num = models.IntegerField()
    user = models.ForeignKey(Buyer,on_delete = True)


'''收货地址'''
class Address(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length = 32)
    recver = models.CharField(max_length = 32)
    buyer = models.ForeignKey(Buyer,on_delete = True)


'''订单'''
class Order(models.Model):
    order_num = models.CharField(max_length=32)
    order_time = models.DateTimeField(auto_now=True)
    order_statue = models.CharField(max_length=32)
    total = models.FloatField()

    user = models.ForeignKey(Buyer,on_delete=True)
    order_address= models.ForeignKey(Address,on_delete=True)


'''商品-订单关联表'''
class OrderGoods(models.Model):
    goods_id = models.IntegerField()
    goods_name = models.CharField(max_length=32)
    goods_price = models.FloatField()
    goods_num = models.IntegerField()
    goods_picture = models.ImageField(upload_to="images")
    order = models.ForeignKey(Order,on_delete=True)



