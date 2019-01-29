#coding=utf-8
from django.shortcuts import render,HttpResponseRedirect,render_to_response
import hashlib,os,datetime
from Seller.models import Seller,Goods,Types,Image
from django.http import JsonResponse


# Create your views here.
'''设置cookie+session'''
def cookieValid(fun):
    def inner(request,*args,**kwargs):
        cookie = request.COOKIES
        session = request.session.get("nickname")
        user = Seller.objects.filter(username= cookie.get("username")).first()
        if user and user.nickname ==session:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/seller/login/")
    return inner


'''移除cookie+session'''
def logout(request):
    username = request.COOKIES.get("username")
    if username:
        response = HttpResponseRedirect("/seller/login/")
        response.delete_cookie("username")
        del request.session["nickname"]
        return response
    else:
        return HttpResponseRedirect("/seller/login")


'''密码加密'''
def setPassword(password):
    md5=hashlib.md5()
    md5.update(password.encode()) #py3加密针对的是字节
    result = md5.hexdigest()
    return result


'''登录'''
def login(request):
    result = {"error":""}
    if request.method == "POST" and request.POST:
        login_valid = request.POST.get("login_valid")
        froms = request.COOKIES.get("from")
        if login_valid == "login_valid" and froms == "http://127.0.0.1:8000/seller/login/":
            username = request.POST.get("username")
            user = Seller.objects.filter(username = username).first()
            if user:
                db_password = user.password
                password = setPassword(request.POST.get("password"))
                if db_password == password:
                    response = HttpResponseRedirect("/seller/")
                    response.set_cookie("username",user.username)
                    response.set_cookie("id", user.id)
                    request.session["nickname"] = user.nickname
                    return response
                else:
                    result["error"] = "密码错误"
            else:
                result["error"] = "用户不存在"

    response = render(request,"seller/login.html",{"result":result})
    response.set_cookie("from","http://127.0.0.1:8000/seller/login/")
    return response


'''添加商品数据'''
from Fresh_Store.settings import MEDIA_ROOT
@cookieValid
def goods_add(request):
    doType = ""
    if request.method == "POST" and request.POST:
        #获取前端表单数据
        postData = request.POST
        goods_id = postData.get("goods_num")
        goods_name = postData.get("goods_name")
        goods_price = postData.get("goods_oprice")  # 原价
        goods_now_price = postData.get("goods_xprice")  # 当前价格
        goods_num = postData.get("goods_count")  # 库存
        goods_description = postData.get("goods_description")  # 描述
        goods_content = postData.get("goods_content")  # 详情
        types = postData.get("goods_type")
        goods_show_time = datetime.datetime.now()  # 发布时间
        #存入数据库
        #先保存商品
        goods = Goods()
        goods.goods_id = goods_id
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_now_price = goods_now_price
        goods.goods_num = goods_num
        goods.goods_description = goods_description
        goods.goods_content = goods_content
        goods.goods_show_time = goods_show_time

        goods.types = Types.objects.get(id = int(types))
        id = request.COOKIES.get("id")
        if id:
            goods.seller = Seller.objects.get(id = int(id))
        else:
            return HttpResponseRedirect("/seller/login/")
        goods.save()

        imgs = request.FILES.getlist("userfiles")
        #保存图片
        for index,img in enumerate(imgs):
            #保存图片到服务器
            file_name = img.name
            file_path = "seller/images/%s_%s.%s"%(goods_name,index,file_name.rsplit(".",1)[1])
            save_path = os.path.join(MEDIA_ROOT,file_path).replace("/","\\")
            try:
                with open(save_path,"wb") as f:
                    for chunk in img.chunks(chunk_size=1024):
                        f.write(chunk)
                #保存路径到数据库
                i = Image()
                i.img_adress = file_path
                i.img_label = "%s_%s"%(index,goods_name)
                i.img_description = "this is description"
                i.goods = goods
                i.save()
            except Exception as e:
                print(e)
    return render(request,"seller/goods_add.html")


'''index页'''
@cookieValid
def index(request):
    return  render(request,"seller/index.html")


'''商品列表页'''
@cookieValid
def goods_list(request):
    goods_list = Goods.objects.order_by()
    return render_to_response("seller/goods_list.html",locals())


'''商品详情页'''
@cookieValid
def goods_list_all(request,num):
    num = int(num)
    onegoods = Goods.objects.get(id = num )
    return render_to_response("seller/goods_list_all.html",locals())


'''测试账号'''
def example(request):
    # s=Seller()
    # s.username="admin"
    # s.password = setPassword("admin")
    # s.nickname="RainSeason旗舰店"
    # s.photo="image/1.jpg"
    # s.phone="15533377777"
    # s.address="北京"
    # s.email="111111@qq.com"
    # s.id_number="411000199999990000"
    # s.save()
    return render(request,"seller/iframeExample.html")


'''分页'''
@cookieValid
def page_goods_list(request,page):
    try:
        db_Goods = Goods.objects.order_by()
    except Exception as e:
        print(e)
    page = int(page)
    print(page)
    start_num = (page-1)*10
    end_num = page*10

    Goods_count = db_Goods.count() #返回查询的条数

    #判断页码的范围
    pageEnd = Goods_count/10
    if pageEnd != int(pageEnd):
        pageEnd += 1

    if page < 3:
        page_start = 1
        page_end = 5
    else:
        page_start = page-1
        page_end = page+2
        if page_end >= pageEnd:
            page_end = pageEnd

    page_range = range(page_start, int(page_end)+1)
    #page_range = range(1,int(page_end)+1 ) #获取分页列表

    goods_list = db_Goods[start_num:end_num]
    print(page_range)
    if not goods_list:
        goods = db_Goods[0:10]
    return render_to_response("seller/goods_list.html",locals())


'''更改数据'''
@cookieValid
def goods_change(request,id):
    doType = "change"
    goods = Goods.objects.get(id = int(id))
    if request.method == "POST" and request.POST:
        #获取前端表单数据

        postData = request.POST
        goods_id = postData.get("goods_num")
        goods_name = postData.get("goods_name")
        goods_price = postData.get("goods_oprice")  # 原价
        goods_now_price = postData.get("goods_xprice")  # 当前价格
        goods_num = postData.get("goods_count")  # 库存
        goods_description = postData.get("goods_description")  # 描述
        goods_content = postData.get("goods_content")  # 详情
        types = postData.get("goods_type")
        goods_show_time = datetime.datetime.now()  # 发布时间
        #存入数据库
        #先保存商品
        goods = Goods.objects.get(id = int(id))
        goods.goods_id = goods_id
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_now_price = goods_now_price
        goods.goods_num = goods_num
        goods.goods_description = goods_description
        goods.goods_content = goods_content
        goods.goods_show_time = goods_show_time
        #Goods.objects.create(goods_id = goods_id) #增加，参数写在括号里,不需要save
        #Goods.objects.update(goods_id = goods_id) #修改，参数写在括号里,不需要save
        goods.types = Types.objects.get(id = int(types))
        id = request.COOKIES.get("id")
        if id:
            goods.seller = Seller.objects.get(id = int(id))
        else:
            return HttpResponseRedirect("/seller/login/")
        goods.save()

        imgs = request.FILES.getlist("userfiles")
        #保存图片
        for index,img in enumerate(imgs):
            #保存图片到服务器
            file_name = img.name
            file_path = "seller/images/%s_%s.%s"%(goods_name,index,file_name.rsplit(".",1)[1])
            save_path = os.path.join(MEDIA_ROOT,file_path).replace("/","\\")
            try:
                with open(save_path,"wb") as f:
                    for chunk in img.chunks(chunk_size=1024):
                        f.write(chunk)
                #保存路径到数据库
                i = Image()
                i.img_adress = file_path
                i.img_label = "%s_%s"%(index,goods_name)
                i.img_description = "this is description"
                i.goods = goods
                i.save()
                return HttpResponseRedirect("/seller/goods_list")
            except Exception as e:
                print(e)
    return render(request,"seller/goods_add.html",locals())


'''删除数据'''
@cookieValid
def goods_del(request,id):
    #删除部分
    goods = Goods.objects.get(id=int(id))
    imgs = goods.image_set.all()
    imgs.delete() #先删除外键表
    goods.delete()  # 再删除主键表数据
    return HttpResponseRedirect("/seller/page_goods_list/1")


'''GOOdApi'''
from django.views.generic import View
class GoodsApi(View):
    def __init__(self,**kwargs):
        View.__init__(self,**kwargs)
        self.response = {
            "statue": "error",
            "data": ""
        }
    def get(self,request):
        if request.GET:
            data = request.GET
            types = data.get("Type")
            order = data.get("order")
            all = data.get("all")
            if order and all == "true":
                self.response["data"] = "all参数和order参数冲突，请参照手册修改"
            if all == "true":
                goods_list = []
                goods = Goods.objects.all()
                for good in goods:
                    goods_list.append(
                        {
                            "name": good.goods_name,
                            "price": good.goods_now_price
                        }
                    )
                self.response["statue"] = "success"
                self.response["data"] = goods_list
            if order:
                goods = Types.objects.get(label = order).goods_set.all()
                goods_list = []
                for good in goods:
                    goods_list.append(
                        {
                            "name": good.goods_name,
                            "price": good.goods_now_price
                        }
                    )
                self.response["statue"] = "success"
                self.response["data"] = goods_list
        return JsonResponse(self.response)

