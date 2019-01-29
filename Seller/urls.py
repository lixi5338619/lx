from django.urls import  path,re_path
from Seller.views import *

urlpatterns =[
    re_path('^$',index),  #无匹配进入index
    path('index/', index),
    path('logout/', logout),
    path('login/', login),
    re_path('goods_add/', goods_add,name="goods_add"),
    re_path('page_goods_list/(\d+)', page_goods_list),
    re_path('goods_list_all/(\d+)', goods_list_all),
    re_path('goods_change/(?P<id>\d+)/', goods_change, name="goods_change"),
    re_path('goods_del/(?P<id>\d+)/', goods_del, name="goods_del"),
    re_path('goods_list/', goods_list,name="goods_list"),
    path('example/',example),

]