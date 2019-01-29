from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render,HttpResponseRedirect,HttpResponse,render_to_response
from Buyer.models import Buyer,EmailValid,BuyCar,Address,Order,OrderGoods
from Seller.views import setPassword
from Seller.models import Goods,Image
import hashlib,os,random,time,datetime
from django.http import JsonResponse

# Create your views here.
'''设置cookie和session'''
def cookieValid(fun):
    def inner(request,*args,**kwargs):
        cookie = request.COOKIES
        username = cookie.get("user_name")
        session = request.session.get("username") #获取session
        user = Buyer.objects.filter(username = username).first()
        if user and session == username: #校验session
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/login/")
    return inner


'''移除cookie和session'''
def logout(request):
    response = HttpResponseRedirect("/login/")
    response.delete_cookie("user_name")
    response.delete_cookie("user_id")
    del request.session["username"]
    return response


'''主页'''
def index(request):
    data = []
    goods = Goods.objects.all()
    for good in goods:
        goods_img = good.image_set.first()
        img = goods_img.img_adress.url
        data.append(
            {"id": good.id, "img": img.replace("media", "static"), "name": good.goods_name,"price": good.goods_now_price}
        )
    return render(request,"buyer/index.html",{"datas": data})


'''默认登录页'''
def login(request):
    result = {"statue": "error","data": ""}
    if request.method == "POST" and request.POST:
        username = request.POST.get("username")
        user = Buyer.objects.filter(username = username).first()
        if user:
            password = setPassword(request.POST.get("userpass"))
            db_password = user.password
            if password == db_password:
                response = HttpResponseRedirect("/")
                response.set_cookie('user_id',user.id)
                response.set_cookie('user_name', user.username)
                request.session["username"] = user.username
                return response
            else:
                result["data"] = "密码错误"
        else:
            result["data"] = "用户名不存在"
    return render(request,'buyer/login.html',{"result":result})


'''注册页'''
def register(request):
    if request.method == "POST" and request.POST:
        username = request.POST.get("username")
        password = request.POST.get("userpass")
        buyer = Buyer()
        buyer.username = username
        buyer.password = setPassword(password)
        buyer.save()
        return HttpResponseRedirect("/login/")
    return render(request,'buyer/register.html')


'''随机数验证码'''
def getRandomData():
    result = str(random.randint(1000,9999))
    return result


'''发送邮箱验证'''
def sendMessage(request):
    result = {"staue": "error","data":""}
    if request.method == "GET" and request.GET:
        recver = request.GET.get("email")
        try:
            subject = "全球生鲜"
            text_content = "hello"
            value = getRandomData()
            html_content = """
            <div>
                <p>
                    尊敬的用户，您的用户验证码是:%s,请不要告诉别人！
                </p>
            </div>
            """%value
            message = EmailMultiAlternatives(subject,text_content,"lixi125066648@163.com",[recver])
            message.attach_alternative(html_content,"text/html")  #内容+类型
            message.send()
        except Exception as e:
            result["data"] = str(e)
        else:
            result["staue"] = "success"
            result["data"] = "success"
            email = EmailValid()
            email.value = value
            email.times = datetime.datetime.now()
            email.email_address = recver
            email.save()
        finally:
            return JsonResponse(result)


'''邮箱登录页'''
def register_email(request):
    result = {"statu": "error", "data": ""}
    if request.method == "POST" and request.POST:
        username = request.POST.get("username")
        code = request.POST.get("code")
        userpass = request.POST.get("userpass")
        email = EmailValid.objects.filter(email_address=username).first()
        if email:
            if code == email.value:
                now = time.mktime(
                    datetime.datetime.now().timetuple()
                )
                db_now = time.mktime(email.times.timetuple())
                if now - db_now >= 86400:
                    result["data"] = "验证码过期"
                    email.delelt()
                else:
                    buyer = Buyer()
                    buyer.username = username
                    buyer.email = username
                    buyer.password = setPassword(userpass)
                    buyer.save()
                    result["statu"] = "success"
                    result["data"] = "恭喜！注册成功"
                    email.delete()
                    return HttpResponseRedirect("/login/")
            else:
                result["data"] = "验证码错误"
        else:
            result["data"] = "验证码不存在"
    return render(request, 'buyer/register_mail.html', locals())


def phone_zhuce(request):
    return render(request, "buyer/phone_zhuce.html", locals())


'''认证清除'''
# def emailValid(request):
#     if request.method == "GET" and request.GET:
#         value = request.GET.get("value")
#         email = EmailValid.objects.filter(value = value).first()
#         if email:
#             now = datetime.datetime.now()
#             db_now = email.times
#             if now - db_now >= 86400:
#                 "超时"
#             else:
#                 return HttpResponseRedirect("/register/?valid=True")
#         return JsonResponse({"value":value})


'''商品详情页'''
def goods_details(request, id):
    good = Goods.objects.get(id=int(id))  # 一个商品
    good_img = good.image_set.first().img_adress.url.replace("media", "static")

    seller = good.seller  # 商品对应的商铺 外键 --> 主
    goods = seller.goods_set.all()[:7]  # 主 --> 外
    data = []
    for g in goods:
        goods_img = g.image_set.first()
        img = goods_img.img_adress.url
        data.append(
            {"id": g.id, "img": img.replace("media", "static"), "name": g.goods_name, "price": g.goods_now_price}
        )
    return render(request, "buyer/goods_details.html", locals())


'''购物车跳转页'''
def carJump(request,goods_id):
    goods = Goods.objects.get(id = int(goods_id))
    id = request.COOKIES.get("user_id")  # 获取用户身份
    if request.method == "POST" and request.POST:
        count = request.POST.get("count")
        img = request.POST.get("good_img")
        # try:
        buyCar = BuyCar.objects.filter(user = int(id),goods_id = int(goods_id)).first() #查询是否存在在购物车当中
        # except Exception as  e:
        #     print(e)

        if not buyCar: #不存在
            buyCar = BuyCar() #实例化模型
            buyCar.goods_num = int(count) #添加数量
            buyCar.goods_id = goods.id
            buyCar.goods_name = goods.goods_name
            buyCar.goods_price = goods.goods_now_price
            buyCar.user = Buyer.objects.get(id=request.COOKIES.get("user_id"))
            buyCar.save()
        else: #存在
            buyCar.goods_num += int(count) #数量相加
            buyCar.save()
        all_price = float(buyCar.goods_price) * int(count)
        return render(request,"buyer/buyCar_jump.html",locals())
    else:
        return HttpResponse("404 not fond")


'''购物车'''
@cookieValid
def carList(request):
    id=request.COOKIES.get("user_id") #获取用户身份
    goodList = BuyCar.objects.filter(user = int(id)) #查询指定用户的购物车商品信息
    address_list = Address.objects.filter(buyer=int(id))
    price_list = []
    for goods in goodList:
        g=Goods.objects.get(id=goods.goods_id)
        img = g.image_set.all().first().img_adress.url.replace("media","static")
        all_price = float(goods.goods_price) * int(goods.goods_num)
        price_list.append({"price": all_price,"goods":goods,"img":img}) #添加总数

    return render(request,"buyer/car_list.html",locals())


'''删除购物车数据'''
@cookieValid
def delete_goods(request,goods_id):
    """
    删除一条
    """
    id = request.COOKIES.get("user_id")
    goods = BuyCar.objects.filter(user = int(id),goods_id = int(goods_id))
        #对应用户id
        #对应商品id
    goods.delete()
    return HttpResponseRedirect("http://127.0.0.1:8000/buyer/carList/")


'''清空购物车'''
@cookieValid
def clear_goods(request):
    """
    删除一条
    """
    id = request.COOKIES.get("user_id")
    goods = BuyCar.objects.filter(user = int(id))
    goods.delete()
    return HttpResponseRedirect("http://127.0.0.1:8000/buyer/carList/")


'''增加订单'''
@cookieValid
def add_order(request):
    buyer_id = request.COOKIES.get("user_id")
    goods_list = []
    if request.method == "POST"  and request.POST:
        requestDate = request.POST
        addr = requestDate.get("address")  #寄送地址的id
        pay_method = requestDate.get("pay_Method")

        all_price=0   #总价
        for key,value in requestDate.items():  #遍历出所有输出
            if  key.startswith("name"):   #判断是不是商品信息id
                buyCar = BuyCar.objects.get(id=int(value))

                g = Goods.objects.get(id=buyCar.goods_id)
                img = g.image_set.all().first().img_adress.url.replace("media", "static")

                price = float(buyCar.goods_num) * float(buyCar.goods_price)
                all_price+=price
                goods_list.append({"price":price,"buyCar":buyCar,"img":img})
        Addr = Address.objects.get(id = int(addr))
        order = Order() #保存到订单


        now = datetime.datetime.now()  # 订单编号 日期 + 随机 + 订单 + id
        nowdata = now.strftime("%Y-%m-%d")
        order.order_num = now.strftime("%Y-%m-%d") + "-" +str(random.randint(10000, 99999)) +str(order.id)
        order.order_time = now

        order.order_statue = 1        # 状态 未支付 1 支付成功 2 配送中 3 交易完成 4 已取消 0
        order.total = all_price
        order.user = Buyer.objects.get(id=int(buyer_id))
        order.order_address = Addr
        order.save()
        for good in goods_list:  # 循环保存订单当中的商品
            g = good["buyCar"]
            print(g.id)
            g_o = OrderGoods()
            g_o.goods_id = g.id
            g_o.goods_name = g.goods_name
            g_o.goods_price = g.goods_price
            g_o.goods_num = g.goods_num
            g_o.goods_picture = g.goods_picture
            g_o.order = order
            g_o.save()

        return render(request,"buyer/enterOrder.html",locals())
    else:
        return HttpResponseRedirect("/buyer/carList/")


'''收货地址'''
@cookieValid
def address(request):
    buyer_id = request.COOKIES.get("user_id")
    address_list = Address.objects.filter(buyer=int(buyer_id))
    return render(request,"buyer/address.html",locals())


'''增加地址'''
@cookieValid
def addAddress(request):
    if request.method == "POST" and request.POST:
        buyer_id = request.COOKIES.get("user_id")
        buyer_name = request.POST.get("buyer")
        buyer_phone = request.POST.get("buyer_phone")
        buyer_address = request.POST.get("buyer_address")
        db_buyer = Buyer.objects.get(id = int(buyer_id))

        addr = Address()
        addr.recver = buyer_name
        addr.phone = buyer_phone
        addr.address = buyer_address
        addr.buyer = db_buyer
        addr.save()
        return HttpResponseRedirect("/buyer/address/")
    return render(request,"buyer/addAddress.html")


'''更改地址'''
@cookieValid
def changeAddress(request,address_id):
    addr=Address.objects.get(id=int(address_id))
    if request.method == "POST" and request.POST:
        buyer_name = request.POST.get("buyer")
        buyer_phone = request.POST.get("buyer_phone")
        buyer_address = request.POST.get("buyer_address")

        addr.recver = buyer_name
        addr.phone = buyer_phone
        addr.address = buyer_address
        addr.save()
        return HttpResponseRedirect("/buyer/address/")
    return render(request,"buyer/addAddress.html",locals())


'''删除地址'''
@cookieValid
def delAddress(request,address_id):
    addr = Address.objects.get(id = int(address_id))
    addr.delete()
    return HttpResponseRedirect("/buyer/address/")


'''开店'''
@cookieValid
def openstore(request):
    return render(request, "buyer/openstore.html", locals())


'''商品分类'''
def goods_type(request):
        return render(request, "buyer/goods_type.html", locals())






def store_detail(request):
    return render(request, "buyer/store_detail.html", locals())


def all_store(request):
    return render(request, "buyer/all_store.html", locals())


def conment(request):
    return render(request, "buyer/conment.html", locals())


def order_list(request):
    return render(request, "buyer/order_list.html", locals())

def orderdetail(request):
    return render(request, "buyer/orderdetail.html", locals())



def user_center(request):
    return render(request, "buyer/user_center.html", locals())


def welcome(request):
    return render(request, "buyer/welcome.html", locals())

def base(request):
    return render(request, "buyer/base.html", locals())

def tiaozhuan(request):
    return render(request,"buyer/tiaozhuan.html",locals())


def page_not_found(request):
    return render_to_response('buyer/found404.html')
def page_error(request):
    return render_to_response('buyer/page500.html')



'''支付宝支付'''
# from alipay import AliPay
# def Zhifubao_pay(request):
#
#     alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
#         MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6sQOnniaLJXnCkB48tbPOXP98KKiGGzOnixCeLxUdgGtZcZ49UKdYml4j9Kx4brg1ZyVm4eJ4nunTFJZp11xf0mMX9HPRMHGvgadj0Vhi/4gYw7r20MZd/hU1IxvTqvFsyuSsuvofe1xZf4YeOI3xidKQ1DYkbYNKVARfMKc2rzoW0iYpBR96xKna/Ye1eP70dPY1SqY2wFwUWU93uMc8FfzUjxmOtiJY8JSRo3bsLYWj96u1ivpe1DuyXNbcTvygo0p9EuSCtq8cUBOj1eTJm/L4d0xT7xef9n+3ZER156QCgjeMAB7pnkIHF2yySVSmVoR2VL9umYdMAZ/jsJe2QIDAQAB
#     -----END PUBLIC KEY-----'''
#
#     app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
#         MIIEpQIBAAKCAQEA6sQOnniaLJXnCkB48tbPOXP98KKiGGzOnixCeLxUdgGtZcZ49UKdYml4j9Kx4brg1ZyVm4eJ4nunTFJZp11xf0mMX9HPRMHGvgadj0Vhi/4gYw7r20MZd/hU1IxvTqvFsyuSsuvofe1xZf4YeOI3xidKQ1DYkbYNKVARfMKc2rzoW0iYpBR96xKna/Ye1eP70dPY1SqY2wFwUWU93uMc8FfzUjxmOtiJY8JSRo3bsLYWj96u1ivpe1DuyXNbcTvygo0p9EuSCtq8cUBOj1eTJm/L4d0xT7xef9n+3ZER156QCgjeMAB7pnkIHF2yySVSmVoR2VL9umYdMAZ/jsJe2QIDAQABAoIBAQDRz/SsxmYrkLESpXoyta4vz61VAVRS9fNWw4GIu+/UIz2f5tg1gZp82HwqNYhKkCTeY/oFLQYbBp4HBNYhUM7djpLJFA7kiTYgoHLyF3TNk4nIXg6GQBqj8KmH6BaWPcgLj9ak11dKLAobuBKQ/sQP8Q9ayAc1enmawXdPg/KBPXtHbU1fOYVKiDhCXLfkAMBZck7b1m1BU7KSS32zToOxFYqHV3sj2YsnqiUXaip5SoHmEqIQkmKoJ684HD8u//1ttXh9SZxUGFVF6OJyRAA7yGXm0tM4yt5Oiv449IlhfTEAP6smrAzY7diETG/YqHfTM+WojnMoQoC5qGwzhdwNAoGBAPe0oc/g2+MkaMHX37sdAXqmMap4DlK/dIEKy9CD/NzU2RL9YbXiA8TNgupu1nOkuc9C8S5CHfGrspDWOjdktTwtA6va6urGVfC02fbUzfzrCLzVtZTFmhn/RXWpww3ogv24mhDt/acln384G6FMCR9hiKSJQuBKOANwfgYAVyF7AoGBAPKggPBMV1eIFu5HMnP+60nL3yAuEREavN6JKVJL63yR5yfZzLscWZG11pdnIPlWdp6m7H8S6xsVx++JaMtBe0xdxIXzOGi5Ksqdr4wLybnCMJZbSwBY/1GK9r5glrFxyWLNNb1eXz9j85vXttUnfogJ3Fdmbpp5UiIauD5XaZ67AoGAHhzAWwQL1xYTAhWbJiUFjAJuIToNC7QolpNYaZXSBIp/hRZ2bWT3blJJavRkb5SD3hVWOnhhKYLk50STuS4t9g3G13p6emX4BpYFtULzc56i5knYlChdbnGg4QftJWCxo+RwHkTARDSHqjCI81fJ+B2kPdRN4/RB0PE48MPT08cCgYEAr7E8TUXqxW69tCQIS+jftpuT4jiZkTo8ZCUMsBRb3OPGcJwN3byEu7fiQdajEQrkcLRNcyNe7kkSc8mcAftT7pPD+H+MbIERlJElCpOKqyIMjwRixkir8f9f97H3zVypSQtyi8Nn035sbICDW8zymk4RqZR6KRALQrj4i+Q+jnsCgYEAliH3B06QG7ToxLx2YRKDkUPo/BS/kgJZsjfZMAOp6z8mpCiC4NoB7l8V4djBmENMK3M4/S0eLYnBiAlPa5GOGfTCfPqP9CncGlkaF6TTS0lzUJm7qcBydP59sUprJXJBtTyYUvmaRnXm8t/fdFJKndY//Ot3P+cLWDyP/2iQ7ZQ=
#     -----END RSA PRIVATE KEY-----'''
#     # 如果在Linux下，我们可以采用AliPay方法的app_private_key_path和alipay_public_key_path方法直接读取.emp文件来完成签证
#     # 在windows下，默认生成的txt文件，会有两个问题
#     # 1、格式不标准
#     # 2、编码不正确 windows 默认编码是gbk
#     # 实例化应用
#     alipay = AliPay(
#         appid="2016092400585696",  # 支付宝app的id
#         app_notify_url=None,  # 会掉视图
#         app_private_key_string=app_private_key_string,  # 私钥字符
#         alipay_public_key_string=alipay_public_key_string,  # 公钥字符
#         sign_type="RSA2",  # 加密方法
#     )
#     out_trade = random.randint(10000000,99999999)+random.randint(1000000,9999999)
#     # 发起支付
#     order_string = alipay.api_alipay_trade_page_pay(
#         out_trade_no=out_trade,
#         total_amount=str(1598.0),  # 将Decimal类型转换为字符串交给支付宝
#         subject="全球生鲜",
#         return_url=None,
#         notify_url=None  # 可选, 不填则使用默认notify url
#     )
#     # 让用户进行支付的支付宝页面网址
#     # print("https://openapi.alipaydev.com/gateway.do?" + order_string)
#     return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)

from alipay import AliPay

def Pay(order_id,money):
    alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6sQOnniaLJXnCkB48tbPOXP98KKiGGzOnixCeLxUdgGtZcZ49UKdYml4j9Kx4brg1ZyVm4eJ4nunTFJZp11xf0mMX9HPRMHGvgadj0Vhi/4gYw7r20MZd/hU1IxvTqvFsyuSsuvofe1xZf4YeOI3xidKQ1DYkbYNKVARfMKc2rzoW0iYpBR96xKna/Ye1eP70dPY1SqY2wFwUWU93uMc8FfzUjxmOtiJY8JSRo3bsLYWj96u1ivpe1DuyXNbcTvygo0p9EuSCtq8cUBOj1eTJm/L4d0xT7xef9n+3ZER156QCgjeMAB7pnkIHF2yySVSmVoR2VL9umYdMAZ/jsJe2QIDAQAB
    -----END PUBLIC KEY-----'''

    app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
        MIIEpQIBAAKCAQEA6sQOnniaLJXnCkB48tbPOXP98KKiGGzOnixCeLxUdgGtZcZ49UKdYml4j9Kx4brg1ZyVm4eJ4nunTFJZp11xf0mMX9HPRMHGvgadj0Vhi/4gYw7r20MZd/hU1IxvTqvFsyuSsuvofe1xZf4YeOI3xidKQ1DYkbYNKVARfMKc2rzoW0iYpBR96xKna/Ye1eP70dPY1SqY2wFwUWU93uMc8FfzUjxmOtiJY8JSRo3bsLYWj96u1ivpe1DuyXNbcTvygo0p9EuSCtq8cUBOj1eTJm/L4d0xT7xef9n+3ZER156QCgjeMAB7pnkIHF2yySVSmVoR2VL9umYdMAZ/jsJe2QIDAQABAoIBAQDRz/SsxmYrkLESpXoyta4vz61VAVRS9fNWw4GIu+/UIz2f5tg1gZp82HwqNYhKkCTeY/oFLQYbBp4HBNYhUM7djpLJFA7kiTYgoHLyF3TNk4nIXg6GQBqj8KmH6BaWPcgLj9ak11dKLAobuBKQ/sQP8Q9ayAc1enmawXdPg/KBPXtHbU1fOYVKiDhCXLfkAMBZck7b1m1BU7KSS32zToOxFYqHV3sj2YsnqiUXaip5SoHmEqIQkmKoJ684HD8u//1ttXh9SZxUGFVF6OJyRAA7yGXm0tM4yt5Oiv449IlhfTEAP6smrAzY7diETG/YqHfTM+WojnMoQoC5qGwzhdwNAoGBAPe0oc/g2+MkaMHX37sdAXqmMap4DlK/dIEKy9CD/NzU2RL9YbXiA8TNgupu1nOkuc9C8S5CHfGrspDWOjdktTwtA6va6urGVfC02fbUzfzrCLzVtZTFmhn/RXWpww3ogv24mhDt/acln384G6FMCR9hiKSJQuBKOANwfgYAVyF7AoGBAPKggPBMV1eIFu5HMnP+60nL3yAuEREavN6JKVJL63yR5yfZzLscWZG11pdnIPlWdp6m7H8S6xsVx++JaMtBe0xdxIXzOGi5Ksqdr4wLybnCMJZbSwBY/1GK9r5glrFxyWLNNb1eXz9j85vXttUnfogJ3Fdmbpp5UiIauD5XaZ67AoGAHhzAWwQL1xYTAhWbJiUFjAJuIToNC7QolpNYaZXSBIp/hRZ2bWT3blJJavRkb5SD3hVWOnhhKYLk50STuS4t9g3G13p6emX4BpYFtULzc56i5knYlChdbnGg4QftJWCxo+RwHkTARDSHqjCI81fJ+B2kPdRN4/RB0PE48MPT08cCgYEAr7E8TUXqxW69tCQIS+jftpuT4jiZkTo8ZCUMsBRb3OPGcJwN3byEu7fiQdajEQrkcLRNcyNe7kkSc8mcAftT7pPD+H+MbIERlJElCpOKqyIMjwRixkir8f9f97H3zVypSQtyi8Nn035sbICDW8zymk4RqZR6KRALQrj4i+Q+jnsCgYEAliH3B06QG7ToxLx2YRKDkUPo/BS/kgJZsjfZMAOp6z8mpCiC4NoB7l8V4djBmENMK3M4/S0eLYnBiAlPa5GOGfTCfPqP9CncGlkaF6TTS0lzUJm7qcBydP59sUprJXJBtTyYUvmaRnXm8t/fdFJKndY//Ot3P+cLWDyP/2iQ7ZQ=
    -----END RSA PRIVATE KEY-----'''

    alipay = AliPay(
        appid="2016092400585696",  # 支付宝app的id
        app_notify_url=None,  # 会掉视图
        app_private_key_string=app_private_key_string,  # 私钥字符
        alipay_public_key_string=alipay_public_key_string,  # 公钥字符
        sign_type="RSA2",  # 加密方法
    )
    # 发起支付
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(money),  # 将Decimal类型转换为字符串交给支付宝
        subject="全球生鲜",
        return_url="http://127.0.0.1:8000/buyer/tiaozhuan", #完成之后返回
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 让用户进行支付的支付宝页面网址
    return "https://openapi.alipaydev.com/gateway.do?" + order_string

def callbackPay(request):
    return HttpResponse("支付成功")
from Buyer.models import Order
def paymethod(request,num):
    order = Order.objects.get(id=int(num))
    out_trade = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    o_m = order.total
    url = Pay(out_trade,o_m)
    return HttpResponseRedirect(url)



