from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

'''
商家Seller:                            商品Goods:
Username                               goods_id
Password                               goods_name
nickname                               goods_price
Photo                                  goods_now_price
Phone                                  goods_img 一个商品多张图片
Address                                goods_num 库存
Email                                  goods_description 描述
Id_number                              goods_content 详情
Bank_card 一个卖家多张银行卡             goods_show_time 发布时间
BankCard                                
Number
bankAddress          商家 和 商品 一对多 seller = models.ForeignKey(Seller, on_delete=True) 
Username             类型 和 商品 一对多 types = models.ForeignKey(Types,on_delete = True)  
idCard
phone

图片Image:            银行卡BankCard:          分类Types:        
Img_adress            number                  Label
Img_label             bankAddress             Parent_id
Img_description       username                Description
                      idCard
                      phone  
                      商家 和 银行卡 一对多 seller = models.ForeignKey(Seller,on_delete=Ture)
商品 和 图片 一对多 goods = models.ForeignKey(Goods, on_delete=True) 
'''

'''类型'''
class Types(models.Model):
    label =  models.CharField(max_length = 32)
    parent_id = models.IntegerField()
    description = models.TextField()

'''卖家'''
class Seller(models.Model):
    username = models.CharField(max_length = 32)
    password = models.CharField(max_length = 32)
    nickname = models.CharField(max_length = 32)
    photo = models.ImageField(upload_to = "image")
    phone = models.CharField(max_length = 32)
    address = models.CharField(max_length = 32)
    email = models.EmailField()
    id_number = models.CharField(max_length = 32)

'''商品'''
class Goods(models.Model):
    goods_id = models.CharField(max_length=32) #id
    goods_name = models.CharField(max_length=32) #名字
    goods_price = models.FloatField()  # 原价
    goods_now_price = models.FloatField()  # 当前价格
    goods_num = models.IntegerField()  # 库存
    # goods_description = models.TextField()  # 描述
    # goods_content = models.TextField()  # 详情
    goods_description = RichTextUploadingField()  # 描述
    goods_content = RichTextUploadingField()  # 详情

    goods_show_time = models.DateField()  # 发布时间

    types = models.ForeignKey(Types, on_delete=True) #一类型多商品
    seller = models.ForeignKey(Seller, on_delete=True) #一卖家多商品
    def __str__(self):
        return self.goods_name
'''图片'''
class Image(models.Model):
    img_adress = models.ImageField(upload_to = "image") #图片地址
    img_label = models.CharField(max_length = 32)  #图片标签
    img_description= models.TextField()  #图片描述
    goods = models.ForeignKey(Goods, on_delete=True)  # 一个商品多张图片

'''银行卡'''
class BankCard(models.Model):
    number = models.CharField(max_length=32)
    bankAddress = models.CharField(max_length=32)
    username = models.CharField(max_length=32)  # 持卡人姓名
    idCard = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)

    seller = models.ForeignKey(Seller, on_delete=True)







# Create your models here.
